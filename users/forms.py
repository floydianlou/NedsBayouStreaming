from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from music.models import Artist
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
            "phone_number", "favorite_artist"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone_number'].widget.attrs.update({
            'id': 'phoneInput',
            'placeholder': 'Your phone number',
        })

        self.fields['favorite_artist'].queryset = Artist.objects.all()
        self.fields['favorite_artist'].empty_label = "Select your favorite artist"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if BayouUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

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
            'phone_number', 'favorite_artist'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'readonly-field'
            }),
            'email': forms.EmailInput(attrs={
                'readonly': 'readonly',
                'class': 'readonly-field'
            }),
            'short_bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['favorite_artist'].queryset = Artist.objects.all()
        self.fields['favorite_artist'].empty_label = "Select your favorite artist"
        self.fields['phone_number'].widget.attrs.update({
            'id': 'phoneInput',
            'placeholder': 'Your phone number',
        })