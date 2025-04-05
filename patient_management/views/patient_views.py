from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from patient_management.forms.patient.patient_form import PatientForm
from patient_management.models.auth_user_model import MediAIUser
from ..models.patient_model import Patient
from ..models.insurance_model import Insurance
from ..models.medication_model import Medication
from ..models.allergy_model import Allergy


# Admin login view
@login_required
def home(request):
    return render(request, 'patient/patient_base.html')


@login_required
def patient_management(request):
    search_query = request.GET.get('search', '')
    sort = request.GET.get('sort', 'created_at')
    order = request.GET.get('order', 'desc')
    
    patients = Patient.objects.filter(is_active=True)
    
    if search_query:
        patients = patients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
  
    if sort == 'full_name':
        if order == 'desc':
            patients = patients.order_by('-first_name', '-last_name')
        else:
            patients = patients.order_by('first_name', 'last_name')
    else:
        if order == 'desc':
            sort = f'-{sort}'
        patients = patients.order_by(sort)
    
    paginator = Paginator(patients, 10)
    page = request.GET.get('page', 1)
    patients = paginator.get_page(page)
    
    context = {
        'patients': patients,
        'sort': sort.replace('-', ''),
        'order': order
    }
    
    if request.GET.get('ajax'):
        return render(request, 'partials/patient_table.html', context)
    
    return render(request, 'patient/patient_management.html', context)

def dashboard(request):
    return render(request, 'patient/dashboard.html')

@login_required
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.is_active = True 
            patient.save()

            form.save_m2m()

            messages.success(request, 'Patient created successfully.')
            return redirect('patient_management')
    else:
        form = PatientForm()

    doctors = MediAIUser.objects.all()
    insurances = Insurance.objects.all()
    medications = Medication.objects.all()
    allergies = Allergy.objects.all()

    return render(request, 'patient/create_patient.html', {
        'form': form,
        'doctors': doctors,
        'insurances': insurances,
        'medications': medications, 
        'allergies': allergies, 
    })

@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully.')
            return redirect('view_patient', patient_id=patient_id)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patient/edit_patient.html', {
        'form': form,
        'edit_patient': patient
    })

@login_required
def view_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient_details = {
        'Full Name': patient.full_name,
        'Date of Birth': patient.date_of_birth,
        'Gender': patient.get_gender_display(),
        'Phone': patient.phone_number,
        'Email': patient.email,
        'Address': patient.address,
        'Medical History': patient.medical_history,
        'Created At': patient.created_at,
        'Last Updated': patient.updated_at,
        'Active': patient.is_active,
    }
    
    return render(request, 'patient/view_patient.html', {
        'view_patient': patient,
        'patient_details': patient_details
    })

@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.is_active = False
        patient.deleted_on = timezone.now()
        patient.save()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('patient_management')
    
    return redirect('patient_management')