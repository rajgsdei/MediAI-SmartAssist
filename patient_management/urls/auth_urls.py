from django.urls import path
from ..views import auth_views  

urlpatterns = [
    path('admin/', auth_views.admin_login, name='admin_login'),
    path('', auth_views.user_login, name='user_login'),
    path('user/', auth_views.user_login, name='user_login'),
]
