from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import os

from patient_management.models.auth_user import  MediAIUser

# Admin login view
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username and password match the ones stored in MongoDB
        try:
            # Query the AdminUser collection for matching username and password
            admin = MediAIUser.objects.get(username=username, password=password, deleted_on__isnull=True)
            
            # If credentials match, redirect to the admin dashboard
            return redirect('admin_dashboard')  # Replace with your admin dashboard URL name

        except MediAIUser.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('admin_login')  # Redirect back to login page

    return render(request, 'auth/admin_login.html')

def user_login(request):

    x = os.getenv('DB_NAME');
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username and password match the ones stored in MongoDB
        try:
            # Query the AdminUser collection for matching username and password
            admin = MediAIUser.objects.get(username=username, password=password, deleted_on__isnull=True)
            
            # If credentials match, redirect to the admin dashboard
            return redirect('admin_dashboard')  # Replace with your admin dashboard URL name

        except MediAIUser.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('user_login')  # Redirect back to login page

    return render(request, 'auth/user_login.html')
