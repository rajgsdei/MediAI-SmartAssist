from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.allergy_model import Allergy
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from django.db.models import Q
from ..forms.patient.allergy_form import AllergyForm
from ..views.shared_views import GenericCRUDView

class AllergyCRUDView(GenericCRUDView):
    model = Allergy
    form_class = AllergyForm
    columns = [
        {'field': 'allergy', 'label': 'Allergy', 'sortable': True},
        {'field': 'reaction', 'label': 'Reaction', 'sortable': True},
    ]
    search_fields = ['allergy', 'reaction']

class AllergyView(LoginRequiredMixin, View):
    template_name = 'patient/allergy.html'
    
    def dispatch(self, request, *args, **kwargs):
        if 'delete' in request.path:
            return self.delete(request, kwargs.get('allergy_id'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, allergy_id=None):
        if allergy_id:
            # Handle single allergy retrieval
            if 'detail' in request.path:
                allergy = get_object_or_404(Allergy, id=allergy_id)
                data = self.allergy_to_dict(allergy)
                return JsonResponse({'success': True, 'data': data})
            else:
                allergy = get_object_or_404(Allergy, id=allergy_id)
                return render(request, self.template_name, {'allergy': allergy})
        
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
    
    def post(self, request, allergy_id=None):
        if allergy_id:
            # Handle update
            allergy = get_object_or_404(Allergy, id=allergy_id)
            form = AllergyForm(request.POST, instance=allergy)
        else:
            # Handle create
            form = AllergyForm(request.POST)
            
        if form.is_valid():
            allergy = form.save(commit=False)
            allergy.is_active = True
            allergy.save()
            return JsonResponse({'success': True, 'id': allergy.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    def delete(self, request, allergy_id):
        allergy = get_object_or_404(Allergy, id=allergy_id)
        allergy.is_active = False
        allergy.save()
        return JsonResponse({'success': True})
    
    def get_list_context(self):
        allergies = Allergy.objects.filter(is_active=True)
        
        # Handle search
        search_term = self.request.GET.get('search', '')
        if search_term and search_term.strip() and len(search_term.strip()) >= 3:  
            search_term = search_term.strip()
            allergies = allergies.filter(
                Q(allergen__icontains=search_term) |
                Q(reaction__icontains=search_term)
            )
            
        # Handle sorting
        sort_field = self.request.GET.get('sort')
        sort_order = self.request.GET.get('order', 'asc')
        
        if sort_field:
            order_prefix = '-' if sort_order == 'desc' else ''
            allergies = allergies.order_by(f"{order_prefix}{sort_field}")
            
        return {
            'items': allergies,
            'columns': self.get_columns()
        }
    
    def get_columns(self):
        return [
            {'field': 'allergy', 'label': 'Allergy', 'sortable': True},
            {'field': 'reaction', 'label': 'Reaction', 'sortable': True},
        ]
    
    def allergy_to_dict(self, allergy):
        return {
            'id': allergy.id,
            'allergy': allergy.allergy,
            'reaction': allergy.reaction,
            'is_active': allergy.is_active,
        }