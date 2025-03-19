from django import forms
from .models import User
from .encryption import generate_keys

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        private_key, public_key = generate_keys()
        user.private_key = private_key.decode()
        user.public_key = public_key.decode()
        if commit:
            user.save()
        return user