from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=12, widget=forms.TextInput(
        attrs={
            "placeholder":"Username",
            'class':'form-control'
            }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder":"Password",
            'class':'form-control'
        }
    ))

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=12, widget=forms.TextInput(
        attrs={
            "placeholder":"Username",
            'class':'form-control'
            }
    ))
    email = forms.EmailField(required=False,widget=forms.EmailInput(
        attrs={
            "placeholder":"Username",
            'class':'form-control'
            }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder":"Password",
            'class':'form-control'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder":"Repeat Password",
            'class':'form-control'
        }
    ))