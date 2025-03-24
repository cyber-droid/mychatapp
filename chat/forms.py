from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from .encryption import generate_keys

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        private_key, public_key = generate_keys()
        user.private_key = private_key.decode()
        user.public_key = public_key.decode()
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User