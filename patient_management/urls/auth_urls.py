from django.urls import path
from ..views import auth_views

urlpatterns = [
    path('admin/login/', auth_views.admin_login, name='admin_login'),
    path('user/', auth_views.user_login, name='user_login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('', auth_views.user_login, name='user_login'), 
]
