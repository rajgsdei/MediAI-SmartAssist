from django.urls import path
from ..views import auth_views
from ..views import user_management_views

urlpatterns = [
    path('login/', auth_views.user_login, name='auth_login'),
    path('admin/', auth_views.admin_login, name='admin_login'),
    path('logout/', auth_views.logout_view, name='logout'),
]
