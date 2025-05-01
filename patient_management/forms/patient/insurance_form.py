from django import forms
from patient_management.models.insurance_model import Insurance

class InsuranceForm(forms.ModelForm):
    COVERAGE_CHOICES = [
        ('Full', 'Full'),
        ('Partial', 'Partial'),
        ('None', 'None')
    ]

    coverage_type = forms.ChoiceField(
        choices=COVERAGE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Insurance
        fields = [
            'provider_name',
            'policy_number',
            'coverage_type',
            'effective_date',
            'expiry_date',
            'premium',
            'is_active'
        ]
        widgets = {
            'provider_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter provider name'
            }),
            'policy_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter policy number'
            }),
            'effective_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select effective date'
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select expiry date'
            }),
            'premium': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter premium amount',
                'step': '0.01'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['provider_name'].required = True
        self.fields['policy_number'].required = True
        self.fields['coverage_type'].required = True
        self.fields['effective_date'].required = True
        self.fields['expiry_date'].required = True
        self.fields['premium'].required = True
        self.fields['is_active'].required = False
        
        # Set labels
        self.fields['provider_name'].label = 'Provider Name'
        self.fields['policy_number'].label = 'Policy Number'
        self.fields['coverage_type'].label = 'Coverage Type'
        self.fields['effective_date'].label = 'Effective Date'
        self.fields['expiry_date'].label = 'Expiry Date'
        self.fields['premium'].label = 'Premium'
        self.fields['is_active'].label = 'Active'