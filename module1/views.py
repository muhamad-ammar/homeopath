from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json
from django.urls import reverse

# Create your views here.
from .forms import LoginForm, RegisterForm, searchForm,patientForm,feedbackForm

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


s_form=''
key=[]
def Home_View(request):
    global s_form
    global key
    key=[]
    s_form=searchForm(request.GET or None)
    return render(request,"home.html", {"s_form": s_form})
def search_view(request):
    form = patientForm(request.POST or None)
    global s_form
    sym=[] 
    rubric=[]
    sym.clear() 
    print(sym)
    jsondata=None
    if request.method == "GET":
            jsondata=None
            response=None
            res=None
            key_s=request.GET
            keyword=key_s['keyword']
            global keys
            key.append(keyword)
            print(key)
                  
            for val in key:
               
                response = requests.get(f'https://www.oorep.com/api/lookup?symptom={val}&repertory=kent&page=0&remedyString=&minWeight=0&getRemedies=1')
                res=response.text     
                
                jsondata=json.loads(res)
                response=None
                print(response)
                res=None
            
                # print(jsondata[0]['results'][0]['rubric']['fullPath'])
                # sym=jsondata[0]['results'][0]['weightedRemedies']
                # print(jsondata[0]['results'][0]['weightedRemedies'].keys())
                symIndex = 0
                for x in jsondata[0]['results']:
                    sym.append([])
                    sym[symIndex].append(x["rubric"]["fullPath"])
                    crr_sub_sym_rem = ''
                    for y in x['weightedRemedies']:
                        crr_sub_sym_rem += ', ' + y["remedy"]["nameAbbrev"]
                    sym[symIndex].append(crr_sub_sym_rem[2:])
                    sym[symIndex].append(x["rubric"]["id"])
                    symIndex+=1
                    # print(word['remedy']['nameLong'])
                    # print(jsondata[0]['results'][0]['weightedRemedies'][""]['remedy']['nameLong'])
                
                # print("Name =",x,"\n\tRemi =", sub_sym_rem[sub_sym.index(x)])
    jsondata=None
    return render(request,'tab_remedy.html',{'sym':sym,'form':form,"s_form": s_form})

def table_view(request):
    
    if request.method == 'POST':         
        symptoms = request.POST.get("symptoms")
        print(symptoms)
        symptom=symptoms.split('\n')
        print('____________')
        print(symptom)
        Remedies = request.POST.get("remedy_given")
        print(Remedies)
        Date = request.POST.get("date")
        print(Date)
        patient_name= request.POST.get("patient_name")
        print(patient_name)
        patientid=patient_name+"%"+str(Date)
        print(patientid)
        
    return redirect('home')


  
def feedback_view(request):
    # Dummy Data it will be extracted from Database using patient Id
    patientid="Ammar%13/09/2021"
    splitid=patientid.split('%')
    remdies="Nat-m., Gaph., Gur."
    remedy=remdies.split(',')
    date=splitid[1]
    patient_name=splitid[0]
    form=feedbackForm(request.POST)   
    return render(request,'feedback.html',{'form':form,'remedy':remedy,'patient_name':patient_name,'date':date})