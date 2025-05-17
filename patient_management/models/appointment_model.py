from django.db import models
import uuid
from patient_management.models.patient_model import Patient
from patient_management.models.auth_user_model import MediAIUser

class Appointment(models.Model):
    id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(MediAIUser, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ], default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointment'
        ordering = ['-appointment_date']

    def __str__(self):
        return f"Appointment for {self.patient.full_name} with {self.doctor.first_name} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
