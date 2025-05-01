from django.db import models
import uuid

class Medication(models.Model):
    id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    prescribed_by = models.CharField(max_length=255) 
    taken_for = models.CharField(max_length=255) 
    strength = models.CharField(max_length=255) 
    form_of_medication = models.CharField(max_length=50, choices=[
        ('Tablet', 'Tablet'),   
        ('Capsule', 'Capsule'),
        ('Injection', 'Injection'),
        ('Cream', 'Cream'),
        ('Ointment', 'Ointment'),
        ('Suspension', 'Suspension'),
        ('Other', 'Other')
    ]) 
    instructions = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'medications'  # This sets the collection name in MongoDB

    def __str__(self):
        return f"{self.name} ({self.dosage})"
