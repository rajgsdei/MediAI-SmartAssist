from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.insurance_model import Insurance
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from django.db.models import Q
from ..forms.patient.insurance_form import InsuranceForm
from ..views.shared_views import GenericCRUDView

class InsuranceCRUDView(GenericCRUDView):
    model = Insurance
    form_class = InsuranceForm
    columns = [
        {'field': 'provider_name', 'label': 'Provider', 'sortable': True},
        {'field': 'policy_number', 'label': 'Policy Number', 'sortable': True},
        {'field': 'coverage_type', 'label': 'Coverage', 'sortable': True},
        {'field': 'effective_date', 'label': 'Start Date', 'sortable': True},
        {'field': 'expiry_date', 'label': 'End Date', 'sortable': True},
        {'field': 'premium', 'label': 'Premium', 'sortable': True},
    ]
    search_fields = ['provider_name', 'policy_number', 'coverage_type']

class InsuranceView(LoginRequiredMixin, View):
    template_name = 'patient/insurance.html'
    
    def dispatch(self, request, *args, **kwargs):
        if 'delete' in request.path:
            return self.delete(request, kwargs.get('insurance_id'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, insurance_id=None):
        if insurance_id:
            # Handle single insurance retrieval
            if 'detail' in request.path:
                insurance = get_object_or_404(Insurance, id=insurance_id)
                data = self.insurance_to_dict(insurance)
                return JsonResponse({'success': True, 'data': data})
            else:
                insurance = get_object_or_404(Insurance, id=insurance_id)
                return render(request, self.template_name, {'insurance': insurance})
        
        # Handle list view
        context = self.get_list_context()
        
        # If it's an AJAX request, return only the table content
        if request.GET.get('ajax'):
            return render(request, 'shared/common_table.html', {
                'items': context['items'],
                'columns': context['columns']
            })
            
        # For full page load, include all context
        context['columns_json'] = json.dumps(context['columns'])
        return render(request, self.template_name, context)
    
    def post(self, request, insurance_id=None):

        if insurance_id:
            # Handle update
            insurance = get_object_or_404(Insurance, id=insurance_id)
            form = InsuranceForm(request.POST, instance=insurance)
        else:
            # Handle create
            form = InsuranceForm(request.POST)
            
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.is_active = True
            insurance.save()
            return JsonResponse({'success': True, 'id': insurance.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    def delete(self, request, insurance_id):
        insurance = get_object_or_404(Insurance, id=insurance_id)
        insurance.is_active = False
        insurance.save()
        return JsonResponse({'success': True})
    
    def get_list_context(self):
        insurances = Insurance.objects.filter(is_active=True)
        
        # Handle search
        search_term = self.request.GET.get('search', '')
        if search_term and search_term.strip() and len(search_term.strip()) >= 3:  
            search_term = search_term.strip()
            insurances = insurances.filter(
                Q(provider_name__icontains=search_term) |
                Q(policy_number__icontains=search_term) |
                Q(coverage_type__icontains=search_term)
            )
            
        # Handle sorting
        sort_field = self.request.GET.get('sort')
        sort_order = self.request.GET.get('order', 'asc')
        
        if sort_field:
            order_prefix = '-' if sort_order == 'desc' else ''
            insurances = insurances.order_by(f"{order_prefix}{sort_field}")
            
        return {
            'items': insurances,
            'columns': self.get_columns()
        }
    
    def get_columns(self):
        return [
            {'field': 'provider_name', 'label': 'Provider', 'sortable': True},
            {'field': 'policy_number', 'label': 'Policy Number', 'sortable': True},
            {'field': 'coverage_type', 'label': 'Coverage', 'sortable': True},
            {'field': 'effective_date', 'label': 'Start Date', 'sortable': True},
            {'field': 'expiry_date', 'label': 'End Date', 'sortable': True},
            {'field': 'premium', 'label': 'Premium', 'sortable': True},
        ]
    
    def insurance_to_dict(self, insurance):
        return {
            'id': insurance.id,
            'provider_name': insurance.provider_name,
            'policy_number': insurance.policy_number,
            'coverage_type': insurance.coverage_type,
            'effective_date': insurance.effective_date,
            'expiry_date': insurance.expiry_date,
            'premium': str(insurance.premium),
            'is_active': insurance.is_active,
        }