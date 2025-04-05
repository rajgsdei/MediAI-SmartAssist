from django.db import models
import uuid


class MedicalHistory(models.Model):
    id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    condition = models.CharField(max_length=255)
    diagnosis_date = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),   
        ('Resolved', 'Resolved'),
        ('Inactive', 'Inactive')
    ])  
    treatment = models.CharField(max_length=500)
    patient_id = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.condition} - {self.status}"
