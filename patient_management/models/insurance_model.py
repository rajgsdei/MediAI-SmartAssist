import uuid
from django.db import models

class Insurance(models.Model):
    id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    patient_id = models.CharField(max_length=255)  
    provider_name = models.CharField(max_length=255) 
    policy_number = models.CharField(max_length=255)  
    coverage_type = models.CharField(max_length=50, choices=[
        ('Full', 'Full'),   
        ('Partial', 'Partial'),
        ('None', 'None')
    ]) 
    effective_date = models.DateField() 
    expiry_date = models.DateField() 
    premium = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'insurance'

    def __str__(self):
        return f"{self.provider_name} - {self.policy_number}"
