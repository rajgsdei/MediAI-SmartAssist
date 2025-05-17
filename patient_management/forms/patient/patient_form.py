from django import forms
from patient_management.models.patient_model import Patient
from patient_management.models.auth_user_model import MediAIUser

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'gender', 
            'phone_number', 
            'email', 
            'address', 
            'doctor', 
            'insurance', 
            'medical_history', 
            'medications',
            'allergies',
            'is_active',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the doctor field to include only users with the role of "Doctor"
        self.fields['doctor'].queryset = MediAIUser.objects.filter(role='Doctor')
        
        # Add form-control class to all fields except checkbox
        for field in self.fields:
            if field != 'is_active' and 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs['class'] = 'form-control'
        
        # Set default value for is_active to True for new patients
        if not kwargs.get('instance'):  # If this is a new patient
            self.fields['is_active'].initial = True
