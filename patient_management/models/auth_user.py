from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class MediAIUser(AbstractUser):
    # Custom primary key field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Or for a custom string format:
    # id = models.CharField(primary_key=True, max_length=50, unique=True)
    
    phone_number = models.CharField(max_length=15, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    hospital_affiliation = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'medi_ai_user'