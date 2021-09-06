from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import LoginForm, RegisterForm, searchForm

User = get_user_model()

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            if password==password2:
                user = User.objects.create_user(username, email, password)
            else:
                request.session['register_error'] = 1
        except:
            user = None
        if user != None:
            login(request, user)
            return redirect("/login")
        else:
            request.session['register_error'] = 1 # 1 == True
    return render(request, "signup.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            # user is valid and active -> is_active
            # request.user == user
            login(request, user)
            return redirect("../home")
        else:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] = attempt + 1
            # return redirect("/invalid-password")
            request.session['invalid_user'] = 1 # 1 == True
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    # request.user == Anon User
    return redirect("/login")

@login_required(login_url='login')
def Home_View(request):
    return render(request, 'home.html')

def Home_View(request):
    form=searchForm(request.GET or None)
    return render(request,"home.html", {"form": form})

def search_view(request):
    if request.method == "POST":
            keyword=request.POST.get("keyword")
            print(keyword)
    return render(request,'tab_remedy.html')

# def remedy_view(request,keyword):
#     return render(request, "tab_remedy.html") 
    