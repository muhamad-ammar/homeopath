from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json
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
sym=[]
def search_view(request):
    if request.method == "POST":
            keyword=request.POST.get("keyword")
            response = requests.get(f'https://www.oorep.com/api/lookup?symptom={keyword}&repertory=kent&page=0&remedyString=&minWeight=0&getRemedies=1')
            res=response.text          
            jsondata=json.loads(res)
            global sym 
            sym=[]       
            # print(jsondata[0]['results'][0]['rubric']['fullPath'])
            sub_sym = []
            sub_sym_rem = []
            # sym=jsondata[0]['results'][0]['weightedRemedies']
            # print(jsondata[0]['results'][0]['weightedRemedies'].keys())
            for x in jsondata[0]['results']:
                sub_sym.append(x["rubric"]["fullPath"])
                crr_sub_sym_rem = ''
                for y in x['weightedRemedies']:
                    crr_sub_sym_rem += ', ' + y["remedy"]["nameAbbrev"]
                sub_sym_rem.append(crr_sub_sym_rem[2:])
                
                # print(word['remedy']['nameLong'])
                # print(jsondata[0]['results'][0]['weightedRemedies'][""]['remedy']['nameLong'])
            
            symIndex = 0
            for x in sub_sym:
                sym.append([])
                sym[symIndex].append(x)
                sym[symIndex].append(sub_sym_rem[symIndex])
                symIndex+=1
                # print("Name =",x,"\n\tRemi =", sub_sym_rem[sub_sym.index(x)])
    return render(request,'tab_remedy.html',{'sym':sym})

def table_view(request):
    global sym
    
    if request.method == 'POST':         
        pair = [key for key in request.POST.keys()][1].split("|")
        # if '+' in request.POST.values():
        #     pair = [key for key in request.POST.keys()][1].split("|")
        #     #pair will be a list containing x and y
        #     object.create(thing1=pair[0], thing2=pair[1])
        #     object.save()
    return render(request,'tableform.html',{'pair':pair,'sym':sym})
    