from patient_management.forms.patient.medication_form import MedicationForm
from patient_management.views.shared_views import GenericCRUDView

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.medication_model import Medication
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from django.db.models import Q

class MedicationCRUDView(GenericCRUDView):
    model = Medication
    form_class = MedicationForm
    columns = [
        {'field': 'name', 'label': 'Medication Name', 'sortable': True},
        {'field': 'dosage', 'label': 'Dosage', 'sortable': False},
        {'field': 'start_date', 'label': 'Start Date', 'sortable': True},
        {'field': 'end_date', 'label': 'End Date', 'sortable': True},
    ]
    search_fields = ['name', 'dosage'] 

class MedicationView(LoginRequiredMixin, View):
    template_name = 'patient/medication.html'
    
    def dispatch(self, request, *args, **kwargs):
        if 'delete' in request.path:
            return self.delete(request, kwargs.get('medication_id'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, medication_id=None):
        if medication_id:
            # Handle single medication retrieval
            if 'detail' in request.path:
                medication = get_object_or_404(Medication, id=medication_id)
                data = self.medication_to_dict(medication)
                return JsonResponse({'success': True, 'data': data})
            else:
                medication = get_object_or_404(Medication, id=medication_id)
                return render(request, self.template_name, {'medication': medication})
        
        # Handle list view
        context = self.get_list_context()
        
        # If it's an AJAX request, return only the table content
        if request.GET.get('ajax'):
            return render(request, 'shared/common_table.html', {
                'items': context['medications'],
                'columns': context['columns']
            })
            
        # For full page load, include all context
        context['columns_json'] = json.dumps(context['columns'])
        return render(request, self.template_name, context)
    
    def post(self, request, medication_id=None):
        if medication_id:
            # Handle update
            medication = get_object_or_404(Medication, id=medication_id)
            form = MedicationForm(request.POST, instance=medication)
        else:
            # Handle create
            form = MedicationForm(request.POST)
            
        if form.is_valid():
            medication = form.save(commit=False)
            medication.is_active = True
            medication.save()
            print(f"Created/Updated medication: {medication.id} - {medication.name}")
            return JsonResponse({'success': True, 'id': medication.id})
        else:
            print(f"Form errors: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    
    def delete(self, request, medication_id):
        medication = get_object_or_404(Medication, id=medication_id)
        medication.is_active = False
        medication.save()
        return JsonResponse({'success': True})
    
    def get_list_context(self):
        medications = Medication.objects.filter(is_active=True)
        
        # Handle search
        search_term = self.request.GET.get('search', '')
        if search_term and search_term.strip() and len(search_term.strip()) >= 3:  
            search_term = search_term.strip()
            medications = medications.filter(
                Q(name__icontains=search_term) |
                Q(dosage__icontains=search_term) |
                Q(prescribed_by__icontains=search_term)
            )
            
        # Handle sorting
        sort_field = self.request.GET.get('sort')
        sort_order = self.request.GET.get('order', 'asc')
        
        if sort_field:
            order_prefix = '-' if sort_order == 'desc' else ''
            medications = medications.order_by(f"{order_prefix}{sort_field}")
            
        print(f"Found {medications.count()} active medications")
        return {
            'medications': medications,  
            'columns': [
                {'field': 'name', 'label': 'Medication Name', 'sortable': True},
                {'field': 'dosage', 'label': 'Dosage', 'sortable': False},
                {'field': 'start_date', 'label': 'Start Date', 'sortable': True},
                {'field': 'end_date', 'label': 'End Date', 'sortable': True},
                {'field': 'prescribed_by', 'label': 'Prescribed By', 'sortable': False},
                {'field': 'taken_for', 'label': 'Taken For', 'sortable': False}
            ]
        }
    
    def medication_to_dict(self, medication):
        return {
            'id': medication.id,
            'name': medication.name,
            'dosage': medication.dosage,
            'start_date': medication.start_date.strftime('%Y-%m-%d'),
            'end_date': medication.end_date.strftime('%Y-%m-%d') if medication.end_date else '',
            'prescribed_by': medication.prescribed_by,
            'taken_for': medication.taken_for,
            'strength': medication.strength,
            'form_of_medication': medication.form_of_medication,
            'instructions': medication.instructions,
            'is_active': medication.is_active
        }