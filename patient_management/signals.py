from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
import os

User = get_user_model()

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    try:
        # Check if admin user exists
        admin_exists = User.objects.filter(username=os.getenv('ADMIN_USERNAME')).exists()
        
        if not admin_exists:
            # Create admin user with all fields from your model
            admin_user = User.objects.create_superuser(
                username=os.getenv('ADMIN_USERNAME'),
                email=os.getenv('ADMIN_EMAIL'),
                password=os.getenv('ADMIN_PASSWORD'),
                first_name=os.getenv('ADMIN_FIRST_NAME', 'System'),
                last_name=os.getenv('ADMIN_LAST_NAME', 'Administrator'),
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            admin_user.address = os.getenv('ADMIN_ADDRESS', 'Main Office')
            admin_user.role = os.getenv('ADMIN_ROLE', 'Admin')
            admin_user.created_on = timezone.now()
            admin_user.updated_on = timezone.now()
            admin_user.is_deleted = False
            admin_user.save()
            
            print('Default admin user created successfully!')
    except Exception as e:
        print(f'Error creating admin user: {str(e)}')