from django.db import models
import uuid

class Allergy(models.Model):
    id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    allergen = models.CharField(max_length=255)
    reaction = models.CharField(max_length=255)  # e.g., 'rash', 'anaphylaxis'
    patient_id = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.allergen} - {self.reaction}"
