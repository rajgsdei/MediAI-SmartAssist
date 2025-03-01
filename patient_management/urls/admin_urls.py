from django.urls import path
from ..views import user_management_views

urlpatterns = [
    path('dashboard/', user_management_views.admin_dashboard, name='admin_dashboard'),
    path('users/', user_management_views.user_management, name='user_management'),
    path('users/create/', user_management_views.create_user, name='create_user'),
    path('users/edit/<uuid:user_id>/', user_management_views.edit_user, name='edit_user'),
    path('users/<uuid:user_id>/', user_management_views.view_user, name='view_user'),
    path('users/<uuid:user_id>/delete/', user_management_views.delete_user, name='delete_user'),
    
]