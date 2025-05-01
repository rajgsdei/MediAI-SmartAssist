from django import forms

from patient_management.models.medication_model import Medication

class MedicationForm(forms.ModelForm):
    FORM_CHOICES = [
        ('Tablet', 'Tablet'),
        ('Capsule', 'Capsule'),
        ('Injection', 'Injection'),
        ('Cream', 'Cream'),
        ('Ointment', 'Ointment'),
        ('Suspension', 'Suspension'),
        ('Other', 'Other')
    ]

    form_of_medication = forms.ChoiceField(
        choices=FORM_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Medication
        fields = [
            'name',
            'dosage',
            'start_date',
            'end_date',
            'prescribed_by',
            'taken_for',
            'strength',
            'form_of_medication',
            'instructions',
            'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter medication name'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter dosage'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select start date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select end date (optional)'
            }),
            'prescribed_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter prescriber name'
            }),
            'taken_for': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter taken for'
            }),
            'strength': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter strength'
            }),
            'instructions': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter instructions'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['name'].required = True
        self.fields['dosage'].required = False
        self.fields['start_date'].required = False
        self.fields['prescribed_by'].required = False
        self.fields['end_date'].required = False
        self.fields['strength'].required = False
        self.fields['form_of_medication'].required = True
        self.fields['instructions'].required = False
        self.fields['is_active'].required = False
        # Set initial value for is_active
        if not kwargs.get('instance'):  # If this is a new medication
            self.fields['is_active'].initial = True
