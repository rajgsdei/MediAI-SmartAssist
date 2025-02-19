from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from patient_management.models.auth_user import MediAIUser

# Admin login view
def home(request):

    return render(request, 'patient/home.html')


def patient_list(request):
    return render(request, 'patient/patient_list.html')