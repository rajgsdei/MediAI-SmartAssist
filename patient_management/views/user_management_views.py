from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..forms.admin.create_user_form import CreateUserForm
from ..forms.admin.edit_user_form import EditUserForm
from django.core.paginator import Paginator
from django.db.models import Q
from functools import wraps

from patient_management.models.auth_user_model import  MediAIUser
from django.contrib.auth.decorators import login_required




@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_base.html')

def clear_messages(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Clear existing messages before view execution
        messages.get_messages(request).used = True
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@clear_messages
def user_management(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')
    
    # Get search parameter
    search_query = request.GET.get('search', '')
    sort_field = request.GET.get('sort', 'username')
    sort_order = request.GET.get('order', 'asc')
    is_ajax = request.GET.get('ajax', False)

    # Start with all users
    users = MediAIUser.objects.filter(
        is_deleted=False
    ).exclude(id=request.user.id)

    # Apply search if provided
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Apply sorting
    sort_prefix = '-' if sort_order == 'desc' else ''
    if sort_field in ['username', 'full_name', 'created_on']:
        if sort_field == 'full_name':
            users = users.order_by(f'{sort_prefix}first_name', f'{sort_prefix}last_name')
        else:
            users = users.order_by(f'{sort_prefix}{sort_field}')

    # Pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page = request.GET.get('page', 1)
    users = paginator.get_page(page)

    context = {
        'users': users,
        'sort': sort_field,
        'order': sort_order
    }

    if is_ajax:
        return render(request, 'partials/user_table.html', context)
    return render(request, 'admin/user_management.html', context)


@login_required
@clear_messages
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
@clear_messages
def edit_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')
    
    user = get_object_or_404(MediAIUser, id=user_id)
    
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user.username} updated successfully!")
            return redirect('view_user', user_id=user.id)
    else:
        form = EditUserForm(instance=user)
    
    return render(request, 'admin/edit_user.html', {
        'form': form,
        'edit_user': user
    })

@login_required
@clear_messages
def view_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')
    
    user = get_object_or_404(MediAIUser, id=user_id)
    context = {
        'view_user': user,
        'user_details': {
            'Username': user.username,
            'Email': user.email,
            'First Name': user.first_name,
            'Last Name': user.last_name,
            'Is Active': user.is_active,
            'Is Staff': user.is_staff,
            'Is Superuser': user.is_superuser,
            'Date Joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            'Last Login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else 'Never',
        }
    }
    return render(request, 'admin/view_user.html', context)

@login_required
@clear_messages
def delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superuser privileges required.")
        return redirect('admin_dashboard')
    
    user = get_object_or_404(MediAIUser, id=user_id)
    user.soft_delete()
    messages.success(request, f"User {user.username} has been deleted successfully.")
    return redirect('user_management')


@login_required
def load_sidebar(request):
    return render(request, 'partials/sidebar_nav.html')