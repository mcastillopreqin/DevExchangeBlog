from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms    
from django.core.exceptions import ValidationError

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Introduce una dirección de correo electrónico válida.')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("Este correo electrónico ya está en uso.")
    #     return email

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user