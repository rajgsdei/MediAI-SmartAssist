from django.urls import path

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
]
