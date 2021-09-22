from django import forms
from django.contrib.auth import get_user_model
from bootstrap_datepicker_plus import DatePickerInput


non_allowed_usernames = ['abc']
# check for unique email & username

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username"
            }
        ))
    email = forms.EmailField(label='Email',
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "email"
            }
        ))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password"
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if username in non_allowed_usernames:
            raise forms.ValidationError("This is an invalid username, please pick another.")
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
        "class": "form-control"
    }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username) # thisIsMyUsername == thisismyusername
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        if qs.count() != 1:
            raise forms.ValidationError("This is an invalid user.")
        return username
class patientForm(forms.Form):
    symptom=forms.CharField(
        label='Symptoms',
        widget=forms.Textarea(
        attrs={
        "class": "form-control",
        "Placeholder":"e.g. Mind, Abrupt",
        "id":"symp"
    }))
    remedy_given=forms.CharField(
        label='remedy',
        widget=forms.TextInput(
        attrs={
        "class": "form-control",
        "Placeholder":"e.g. Remedies",
        "id":"search-input"
    }))
    patient_name=forms.CharField(
        label='Patient Name',
        widget=forms.TextInput(
        attrs={
        "class": "form-control",
        "Placeholder":"Enter Patient Name" 
    }))
    date = forms.DateField(input_formats=['%d/%m/%Y'])
class searchForm(forms.Form):
    keyword = forms.CharField(
        label='Symptom',
        widget=forms.TextInput(
        attrs={
        "class": "form-control",
        "Placeholder":"e.g. Abrupt",
        "id":"user-input"
        
    }))  
class feedbackForm(forms.Form):
    keyword = forms.CharField(
        label='Symptom',
        widget=forms.TextInput(
        attrs={
        "class": "form-control",
        "Placeholder":"e.g. Abrupt"
        
    }))  
