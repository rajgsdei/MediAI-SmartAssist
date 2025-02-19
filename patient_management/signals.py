from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
import os

User = get_user_model()

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    try:
        # Check if admin user exists
        admin_exists = User.objects.filter(username=os.getenv('ADMIN_USERNAME')).exists()
        
        if not admin_exists:
            # Create admin user
            admin_user = User.objects.create_superuser(
                username=os.getenv('ADMIN_USERNAME'),
                email=os.getenv('ADMIN_EMAIL'),
                password=os.getenv('ADMIN_PASSWORD'),  # You should change this in production
                is_staff=True,
                is_superuser=True
            )
            
            # Add additional fields
            admin_user.phone_number = os.getenv('ADMIN_PHONE')
            admin_user.specialization = 'System Administrator'
            admin_user.save()
            
            print('Default admin user created successfully!')
    except Exception as e:
        print(f'Error creating admin user: {str(e)}')