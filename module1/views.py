from typing import ContextManager
from django.shortcuts import render,redirect
from .forms import LoginForm,SignupForm
from django.contrib.auth import authenticate,login
# Create your views here.
def login(request):
    form = LoginForm()
    msg=None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile')
            else:
                msg = "Invalid Credential"
        else:
            msg = "Invalid Form"
    context = {
    'form':form,
    'msg':msg
    }
    return render(request,'login.html',context)

def signup(request):
    form = SignupForm()
    msg=None
    context = {
        'form':form,
        'msg':msg
    }
    if request.method == "POST":
        form = SignupForm(request.POST)
        if (form.is_valid()):
            form.save()
            return redirect("/login")
        else:
            msg = "Form is not valid"
    else:
        msg="Error submitting the form"
        return render(request,'signup.html',context)

    return render(request,'signup.html',context)
