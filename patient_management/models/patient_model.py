from django.db import models
import uuid
from jsonfield import JSONField

from patient_management.models.allergy_model import Allergy
from patient_management.models.auth_user_model import MediAIUser
from patient_management.models.insurance_model import Insurance
from patient_management.models.medical_history_model import MedicalHistory
from patient_management.models.medication_model import Medication

class Patient(models.Model):
    id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ])
    
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    doctor = models.ForeignKey(MediAIUser, on_delete=models.SET_NULL, null=True, blank=True)  # Single doctor selection
    medications = models.ManyToManyField(Medication, default=list)  
    medical_history = models.ManyToManyField(MedicalHistory, default=list) 
    allergies = models.ManyToManyField(Allergy, default=list)  
    insurance = models.ForeignKey(Insurance, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'patient'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
