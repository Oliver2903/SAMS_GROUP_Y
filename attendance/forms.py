from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Form inscription
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form connexion
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SearchForm(forms.Form):
    query = forms.CharField(label='Recherche', max_length=100, required=False)
    date = forms.DateField(label='Date', required=False, widget=forms.SelectDateWidget)
