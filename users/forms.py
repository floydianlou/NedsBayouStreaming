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

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Your username'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Your password'
        })