from django import forms
from patient_management.models.allergy_model import Allergy

class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = [
            'allergy',
            'reaction',
            'is_active'
        ]
        widgets = {
            'allergy': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter allergy name'
            }),
            'reaction': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter reaction'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['allergy'].required = True
        self.fields['reaction'].required = True
        self.fields['is_active'].required = False
        
        # Set labels
        self.fields['allergy'].label = 'Allergy'
        self.fields['reaction'].label = 'Reaction'
        self.fields['is_active'].label = 'Active'