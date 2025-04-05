from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q

class GenericCRUDView:
    model = None
    form_class = None
    template_name = 'partials/generic_table.html'
    columns = []
    search_fields = []
    items_per_page = 10

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)
        search_query = self.request.GET.get('search', '')
        
        if search_query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q_objects)
            
        sort = self.request.GET.get('sort', 'created_at')
        order = self.request.GET.get('order', 'desc')
        
        if order == 'desc':
            sort = f'-{sort}'
        return queryset.order_by(sort)

    def get_context_data(self):
        queryset = self.get_queryset()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, self.items_per_page)
        items = paginator.get_page(page)
        
        return {
            'items': items,
            'columns': self.columns,
            'sort': self.request.GET.get('sort', 'created_at'),
            'order': self.request.GET.get('order', 'desc')
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.GET.get('ajax'):
            html = render_to_string(self.template_name, context)
            return JsonResponse({'html': html})
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save()
            return JsonResponse({'success': True, 'id': instance.id})
        return JsonResponse({'success': False, 'errors': form.errors})