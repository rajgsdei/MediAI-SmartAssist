from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import os
from django.db import DatabaseError
from django.contrib.auth import logout
from django.db import connection

from patient_management.models.auth_user_model import  MediAIUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin_user = MediAIUser.objects.get(
                username=username,
                is_active=True,
                is_superuser=True
            )
            
            if check_password(password, admin_user.password):
                from django.contrib.auth import login
                login(request, admin_user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid password.")
                return redirect('admin_login')

        except MediAIUser.DoesNotExist:
            messages.error(request, "No admin user found with the given username.")
            return redirect('admin_login')
        
        except DatabaseError as e:
            messages.error(request, "Database connection error. Please try again later.\n" + str(e) + "\n" + str(connection.queries))
            return redirect('admin_login')

    return render(request, 'auth/admin_login.html')



def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = MediAIUser.objects.get(
                username=username,
                is_active=True,
                deleted_on__isnull=True
            )
            
            if check_password(password, user.password):
                from django.contrib.auth import login
                login(request, user)
                return redirect('root')
            else:
                messages.error(request, "Invalid password.")
                return redirect('auth_login')

        except MediAIUser.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('auth_login')
        
        except DatabaseError as e:
            messages.error(request, "Database connection error. Please try again later.")
            return redirect('auth_login')

    return render(request, 'auth/user_login.html')


@login_required
def logout_view(request):
    is_admin = request.user.is_superuser
    logout(request)
    return redirect('root')