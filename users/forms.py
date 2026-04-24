from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adres e-mail")
    
    class Meta:
        model = User
        fields = ['username', 'email']