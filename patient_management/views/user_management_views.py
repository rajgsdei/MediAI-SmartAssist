from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..forms.admin.create_user_form import CreateUserForm

from patient_management.models.auth_user_model import  MediAIUser
from django.contrib.auth.decorators import login_required




@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')




@login_required
def user_management(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')
    
    # Filter out deleted users and current user
    users = MediAIUser.objects.filter(
        is_deleted=False
    ).exclude(id=request.user.id)
    
    return render(request, 'admin/user_management.html', {'users': users})


@login_required
def create_user(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} created successfully!")
            return redirect('user_management')
    else:
        form = CreateUserForm()
    
    return render(request, 'admin/create_user.html', {'form': form})

@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')
    
    user = get_object_or_404(MediAIUser, id=user_id)
    if request.method == "POST":
        # Handle user editing
        pass
    return render(request, 'admin/edit_user.html', {'edit_user': user})

@login_required
def view_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')
    
    user = get_object_or_404(MediAIUser, id=user_id)
    return render(request, 'admin/view_user.html', {'view_user': user})

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')
    
    user = get_object_or_404(MediAIUser, id=user_id)
    user.soft_delete()  # Using our new soft_delete method
    messages.success(request, f"User {user.username} has been deleted successfully.")
    return redirect('user_management')