from django import forms
from patient_management.models.medical_history_model import MedicalHistory

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['condition', 'diagnosis_date', 'status', 'treatment']
        widgets = {
            'diagnosis_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }