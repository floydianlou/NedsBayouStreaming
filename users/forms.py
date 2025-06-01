from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import BayouUser


class BayouUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = BayouUser
        fields = (
            "username", "email",
            "password1", "password2",
            "first_name", "last_name",
            "profile_picture", "short_bio",
            "phone_number", "favorite_band"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone_number'].widget.attrs.update({
            'id': 'phoneInput',
            'placeholder': 'Your phone number',
        })

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Your username'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Your password'
        })

class BayouUserUpdateForm(forms.ModelForm):
    class Meta:
        model = BayouUser
        fields = [
            'username', 'email',
            'first_name', 'last_name',
            'profile_picture', 'short_bio',
            'phone_number', 'favorite_band'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'disabled': 'disabled',
                'class': 'readonly-field'
            }),
            'email': forms.EmailInput(attrs={
                'disabled': 'disabled',
                'class': 'readonly-field'
            }),
            'short_bio': forms.Textarea(attrs={'rows': 3}),
        }