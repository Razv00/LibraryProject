from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Carte


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CarteForm(forms.ModelForm):
    class Meta:
        model = Carte
        fields = ['titlu', 'autor', 'descriere', 'disponibil', 'utilizator_imprumutat']