from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from django import forms 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail address")
    
    class Meta:
        model = User
        fields = ['username', 'email']