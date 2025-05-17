from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from patient_management.forms.patient.appointment_form import AppointmentForm
from patient_management.models.appointment_model import Appointment
from patient_management.models.auth_user_model import MediAIUser
from patient_management.models.patient_model import Patient
import json

class AppointmentView(View):
    template_name = 'patient/appointment.html'

    def get(self, request, appointment_id=None):
        if appointment_id:
            if 'detail' in request.path:
                appointment = get_object_or_404(Appointment, id=appointment_id)
                data = self.appointment_to_dict(appointment)
                return JsonResponse({'success': True, 'data': data})
            else:
                appointment = get_object_or_404(Appointment, id=appointment_id)
                return render(request, self.template_name, {'appointment': appointment})

   
        context = self.get_list_context()

        context['patients'] = Patient.objects.all()
        context['doctors'] = MediAIUser.objects.filter(role='Doctor') 

        # If it's an AJAX request, it will return only the table content
        if request.GET.get('ajax'):
            return render(request, 'shared/common_table.html', {
                'items': context['appointments'],
                'columns': context['columns']
            })

        # For full page load, include all context
        context['columns_json'] = json.dumps(context['columns'])
        return render(request, self.template_name, context)

    def post(self, request, appointment_id=None):
        if appointment_id:
            # Handle update
            appointment = get_object_or_404(Appointment, id=appointment_id)
            form = AppointmentForm(request.POST, instance=appointment)
        else:
            # Handle create
            form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save()
            return JsonResponse({'success': True, 'id': appointment.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    def delete(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return JsonResponse({'success': True})

    def get_list_context(self):
        appointments = Appointment.objects.all()

        # Handle search
        search_term = self.request.GET.get('search', '')
        if search_term and search_term.strip() and len(search_term.strip()) >= 3:
            search_term = search_term.strip()
            appointments = appointments.filter(
                Q(patient__first_name__icontains=search_term) |
                Q(patient__last_name__icontains=search_term) |
                Q(reason__icontains=search_term)
            )

        # Handle sorting
        sort_field = self.request.GET.get('sort')
        sort_order = self.request.GET.get('order', 'asc')

        if sort_field:
            order_prefix = '-' if sort_order == 'desc' else ''
            appointments = appointments.order_by(f"{order_prefix}{sort_field}")

        return {
            'appointments': [
                {
                    'id': appointment.id,
                    'patient': appointment.patient.full_name if appointment.patient else 'N/A',
                    'doctor': f"{appointment.doctor.first_name} {appointment.doctor.last_name}" if appointment.doctor else 'N/A',
                    'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d %H:%M'),  # Include both date and time
                    'reason': appointment.reason,
                    'status': appointment.status,
                }
                for appointment in appointments
            ],
            'columns': [
                {'field': 'patient', 'label': 'Patient', 'sortable': True},
                {'field': 'doctor', 'label': 'Doctor', 'sortable': True},
                {'field': 'appointment_date', 'label': 'Appointment Date', 'sortable': True},
                {'field': 'reason', 'label': 'Reason', 'sortable': False},
                {'field': 'status', 'label': 'Status', 'sortable': True},
            ]
        }

    def appointment_to_dict(self, appointment):
        return {
            'id': appointment.id,
            'patient': appointment.patient.id if appointment.patient else None,
            'doctor': appointment.doctor.id if appointment.doctor else None,
            'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d %H:%M'),  # Include both date and time
            'reason': appointment.reason,
            'status': appointment.status,
        }