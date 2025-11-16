from django.urls import path

from patient_management.views import ai_chat_views
from patient_management.views.allergy_views import AllergyView
from patient_management.views.appointment_views import AppointmentView
from patient_management.views.insurance_view import InsuranceView
from patient_management.views.medication_views import MedicationView
from patient_management.views.user_management_views import load_sidebar
from ..views import patient_views, staff_views

urlpatterns = [
    path('', staff_views.home, name='home'),
    path('patients/', patient_views.patient_management, name='patient_management'),
    path('patients/create/', patient_views.create_patient, name='create_patient'),
    path('patients/edit/<uuid:patient_id>/', patient_views.edit_patient, name='edit_patient'),
    path('patients/view/<uuid:patient_id>/', patient_views.view_patient, name='view_patient'),
    path('patients/<uuid:patient_id>/delete/', patient_views.delete_patient, name='delete_patient'),
    path('load_sidebar/', load_sidebar, name='load_sidebar'),
    path('dashboard/', patient_views.dashboard, name='dashboard'),
    path('create-medical-history/', patient_views.create_medical_history, name='create_medical_history'),
  
    path('medications/', MedicationView.as_view(), name='medication'),
    path('medications/<uuid:medication_id>/detail/', MedicationView.as_view(), name='medication_detail'),
    path('medications/<uuid:medication_id>/update/', MedicationView.as_view(), name='medication_update'),
    path('medications/<uuid:medication_id>/delete/', MedicationView.as_view(), name='medication_delete'),

    path('allergies/', AllergyView.as_view(), name='allergies'),
    path('allergies/<uuid:allergy_id>/detail/', AllergyView.as_view(), name='allergy_detail'),
    path('allergies/<uuid:allergy_id>/update/', AllergyView.as_view(), name='allergy_update'),
    path('allergies/<uuid:allergy_id>/delete/', AllergyView.as_view(), name='allergy_delete'),

    path('insurance/', InsuranceView.as_view(), name='insurance'),
    path('insurance/<uuid:insurance_id>/detail/', InsuranceView.as_view(), name='insurance_detail'),
    path('insurance/<uuid:insurance_id>/update/', InsuranceView.as_view(), name='insurance_update'),
    path('insurance/<uuid:insurance_id>/delete/', InsuranceView.as_view(), name='insurance_delete'),

    path('appointments/', AppointmentView.as_view(), name='appointment'),
    path('appointments/<uuid:appointment_id>/detail/', AppointmentView.as_view(), name='appointment_update'),
    path('appointments/<uuid:appointment_id>/delete/', AppointmentView.as_view(), name='appointment_delete'),

    path('ai-chat/', ai_chat_views.AIChatView.as_view(), name='ai_chat'),
]
