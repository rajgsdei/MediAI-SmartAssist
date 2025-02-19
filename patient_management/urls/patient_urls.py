from django.urls import path
from ..views import patient_views  # Import patient views here

urlpatterns = [
   path('', patient_views.home, name='home'),
   path('patients/', patient_views.patient_list, name='patients'),
  #  path('create/', patient_views.create_patient, name='create_patient'), 
]
