from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from patient_management.forms.patient.medical_history_form import MedicalHistoryForm
from patient_management.forms.patient.patient_form import PatientForm
from patient_management.models.auth_user_model import MediAIUser
from patient_management.models.medical_history_model import MedicalHistory
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
            form.save()
            messages.success(request, "Patient created successfully!")
            return redirect('patient_management')
        else:
            print("Form errors:", form.errors) 
    else:
        form = PatientForm()

    medical_history_form = MedicalHistoryForm()

    doctors = MediAIUser.objects.all()  # Fetch all doctors
    medical_histories = MedicalHistory.objects.all()
    insurances = Insurance.objects.all()  # Fetch all insurances
    medications = Medication.objects.all()
    allergies = Allergy.objects.all()

    return render(request, 'patient/create_patient.html', {
        'form': form,
        'medical_history_form': medical_history_form,
        'doctors': doctors,
        'medical_histories': medical_histories,
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

    # Construct patient details dictionary
    patient_details = {
        'First Name': patient.first_name,
        'Last Name': patient.last_name,
        'Date of Birth': patient.date_of_birth,
        'Gender': patient.gender,
        'Phone Number': patient.phone_number,
        'Email': patient.email,
        'Address': patient.address,
        'Medical History': ', '.join([str(history) for history in patient.medical_history.all()]) if patient.medical_history.exists() else 'None',
        'Doctor': patient.doctor.first_name + ' ' + patient.doctor.last_name if patient.doctor else 'None',
        'Insurance': patient.insurance.policy_name if patient.insurance else 'None',  # Use the correct field name
        'Medications': ', '.join([str(medication) for medication in patient.medications.all()]) if patient.medications.exists() else 'None',
        'Allergies': ', '.join([str(allergy) for allergy in patient.allergies.all()]) if patient.allergies.exists() else 'None',
        'Is Active': patient.is_active,
    }

    return render(request, 'patient/view_patient.html', {
        'view_patient': patient,
        'patient_details': patient_details,
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


@login_required
def create_medical_history(request):
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save()
            return JsonResponse({'id': medical_history.id, 'condition': medical_history.condition})
        return JsonResponse({'error': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)