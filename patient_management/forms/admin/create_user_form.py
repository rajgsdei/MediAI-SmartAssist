from django import forms
from django.contrib.auth.forms import UserCreationForm
from ...models.auth_user_model import MediAIUser

class CreateUserForm(UserCreationForm):
    # Override phone_number field to make it not required
    phone_number = forms.CharField(
        max_length=15,
        required=False,  # This makes the field optional
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter phone number',
            'class': 'form-control'
        })
    )

    class Meta:
        model = MediAIUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role', 
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Add placeholders
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter username'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter email'
        })
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter first name'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter last name'
        })
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter phone number'
        })
        self.fields['role'].widget.attrs.update({
            'placeholder': 'Select role'
        })