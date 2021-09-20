from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
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
def Home_View(request):
    global s_form
    s_form=searchForm(request.GET or None)
    return render(request,"home.html", {"s_form": s_form})

def search_view(request):
    sym=[]
    rubric=[]
    global s_form
    sym=[]
    rubric=[]
    pForm=patientForm(request.POST or None)
    if request.method == "POST":
            key_s=request.GET
            keyword=key_s['inputValue']
            response = requests.get(f'https://www.oorep.com/api/lookup?symptom={keyword}&repertory=kent&page=0&remedyString=&minWeight=0&getRemedies=1')
            res=response.text          
            jsondata=json.loads(res)
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
            print(sym)
    
                # print(word['remedy']['nameLong'])
                # print(jsondata[0]['results'][0]['weightedRemedies'][""]['remedy']['nameLong'])
            
               # print("Name =",x,"\n\tRemi =", sub_sym_rem[sub_sym.index(x)])
    
    return render(request,'tab_remedy.html',{"pForm": pForm})

def table_view(request):
    sym=[]
    rubric=[]
    print('Hi')
    if request.method=='GET':
        print('Hello')
        key_s=request.GET
        print('Hye')
        keyword=key_s['inputValue']
        print('Bye')
        response = requests.get(f'https://www.oorep.com/api/lookup?symptom={keyword}&repertory=kent&page=0&remedyString=&minWeight=0&getRemedies=1')
        res=response.text          
        jsondata=json.loads(res)
        
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
        result = ''
        for x in sym:
            result += "<tr id = "+str(x[2])+">"
            result += "<td class= 'col-lg-2'>" + x[0]+"</td>"
            result += "<td class= 'col-lg-3'>" + x[1]+"</td>"
            result += "<td class= 'col-lg-1'><div class='abc'>"
            result += "<button type = 'submit' value='Add This' id = "+str(x[2])+" class = 'btn btn-success'  >Add This</button></div></td>"
            result += '</tr>'
        return HttpResponse(result)
def repo_view(request):
    if request.method=='GET':
        id_s=request.GET
        ids=id_s['id_data']
        id_arr=ids.split(',')
        print(id_arr)
        # ids=id_s['ids']
        print(ids)
        print('Call working')
        idsss='abc'
        return HttpResponse(idsss)
def submit_view(request):
    if request.method == "POST":
        Remedies = request.POST.get("remedy_given")
        print(Remedies)
        Date = request.POST.get("date")
        print(Date)
        patient_name= request.POST.get("patient_name")
        print(patient_name)
        patientid=patient_name+"%"+str(Date)
    return redirect(Home_View)

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