from django.utils import timezone 
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class MediAIUser(AbstractUser):
    id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    deleted_on = models.DateTimeField(null=True, blank=True)
    
    is_deleted = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'medi_ai_users'
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        self.updated_on = timezone.now()
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.deleted_on = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.is_active = True
        self.deleted_on = None
        self.save()

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username