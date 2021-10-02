from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
# Create your views here.
from .forms import LoginForm, RegisterForm, searchForm,patientForm,feedbackForm
from .models import patientData,updatedWeights
from datetime import datetime

User = get_user_model()
rubricsWithIds ={}
sliderNameList = []

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
@login_required(login_url='login/')
def logout_view(request):
    request.session.flush()
    logout(request)
    # request.user == Anon User
    return redirect("/login")

def Home_View(request):
    return render(request,"home.html")
@login_required(login_url='login/')
def search_view(request):
    sym=[]
    rubric=[]
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
                rubricName = x["rubric"]["fullPath"]
                sym[symIndex].append(rubricName)
                crr_sub_sym_rem = ''
                for y in x['weightedRemedies']:
                    crr_sub_sym_rem += ', ' + y["remedy"]["nameAbbrev"]
                sym[symIndex].append(crr_sub_sym_rem[2:])
                rubricId = x["rubric"]["id"]
                sym[symIndex].append(rubricId)
                symIndex+=1
                
                
    
                # print(word['remedy']['nameLong'])
                # print(jsondata[0]['results'][0]['weightedRemedies'][""]['remedy']['nameLong'])
            
               # print("Name =",x,"\n\tRemi =", sub_sym_rem[sub_sym.index(x)])
    
    return render(request,'tab_remedy.html',{"pForm": pForm})

def table_view(request):
    sym=[]
    rubric=[]
    global rubricsWithIds
    
    if request.method=='GET':
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
            rubricName = x["rubric"]["fullPath"]
            sym[symIndex].append(rubricName)
            crr_sub_sym_rem = ''
            for y in x['weightedRemedies']:
                crr_sub_sym_rem += ', ' + y["remedy"]["nameAbbrev"]
            sym[symIndex].append(crr_sub_sym_rem[2:])
            rubricId = x["rubric"]["id"]
            sym[symIndex].append(rubricId)
            symIndex+=1
            
            rubricsWithIds[rubricId]=rubricName
            
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
        # ids=id_s['ids']
        idsss='abc'
        return HttpResponse(idsss)
    
def submit_view(request):
    global rubricsWithIds
        
    if request.method == "GET":
        val_s=request.GET['values_text'].split(',')[:-1]
        
        dbpatient=patientData()
        pName = val_s.pop(0).split('?')[1]
        dbpatient.patientID = pName +'%'+ val_s.pop(0).split('?')[1]+'%'+str(datetime.now().strftime("%H:%M:%S"))
        remies=''
        for x in val_s:
            x=x.split('?')
            rid = int(x.pop(0))
            remies+=str(rid)+"|"+rubricsWithIds.get(rid)+':'+x[0][1:].replace('||','|')+'?'
            
        dbpatient.remedies = remies[:-1]
        dbpatient.save()
        
        
        # printAllDB()
        
        # dbpatient.remedies = request.POST.get("remedies")
        # print(request.POST.get("remedies"))
        # dbpatient.rubrics = request.POST.get("symptom")
        # print(request.POST.get("symptom"))
        # Date = request.POST.get("date")
        # patient_name= request.POST.get("patient_name")
        # dbpatient.patientID=patient_name+"%"+str(Date)
        # print(patient_name+"%"+str(Date))
       
    return HttpResponse('Success')

def saveFeedbackForm(request):
    if request.method == 'GET':
        pid=request.GET
        print(pid)
        patientID = sliderNameList.pop(0)
        for x in sliderNameList:
            feedback = updatedWeights()
            feedback.patientID = patientID
            feedback.rubricRemedies = x
            print(x)
            feedback.weight = pid[x.replace(', ','_')]
            feedback.save()
            
        dbpatient=patientData.objects.get(patientID=patientID)
        dbpatient.feedback = True
        dbpatient.save(update_fields=["feedback"])        
        
    return redirect(feedback_view)

def patientFeedbackForm(request):
    result = ''
    global sliderNameList
    if request.method == 'GET':
        pid=request.GET['inputValue']
        sliderNameList = [pid]
        patient = patientData.objects.get(patientID=pid)
        name,date,time = pid.split('%')
        remiesRubrics = []
        for x in patient.remedies.split('?'):
            x=x.split(':')
            temp = [x.pop(0).split("|")[1]]
            for y in x[0].split('|'):
                if y != '':
                    temp.append(y)
            remiesRubrics.append(temp)
        
        result += "<h2 align = 'center'>"+name+" </h2>"
        result += "<h2 align = 'center'>"+date+"</h2>"
        result += "<br><br><br>"
        for x in remiesRubrics:
            z=x.pop(0)
            zx=z.replace(', ','_')
            result += "<h3>"+z+"</h3><br>"
            for y in x:
                sliderName = zx+'?'+y
                sliderNameList.append(sliderName.replace('_',', '))
                result += "<p>"+y+"</p>"
                if patient.feedback == False:
                    result += "<div id="+zx+">0 <input type='range' min='0' max='5' value='3' class='slider' name='"+sliderName+"'> 5 <div><br>"
                else:
                    givenWeight = str(updatedWeights.objects.get(patientID=pid, rubricRemedies=sliderName.replace('_',', ')).weight)
                    result += "<div id="+zx+"><input type='range' min='0' max='5' value='"+givenWeight+"' class='slider' name='"+sliderName+"' disabled> "+givenWeight+" <div><br>"
            result += "<br><br>"
        
        if patient.feedback == False:
            result += "<button type='submit' class='btn btn-primary' id='saveFeedback' >SAVE FEEDBACK</button>"
            
    return HttpResponse(result)
@login_required(login_url='login/')
def feedback_view(request):
    
    patient=patientData.objects.all()
    result=[]
    
    feedSubmited = []
    feedNotSubmited = []
    for dat in patient:
        patientarr=[]
        pid=dat.patientID
        flag=dat.feedback
        patient_name,date,time=pid.split('%')
        patientarr.append(patient_name)
        patientarr.append(date)
        patientarr.append(flag)
        patientarr.append(pid)
        patientarr.append(formateTime(time))
        print(dat.feedback," ",type(dat.feedback))
        if dat.feedback == False:
            feedNotSubmited.append(patientarr)
        if dat.feedback == True:
            feedSubmited.append(patientarr)
            
    return render(request,'feedback.html',{"feedSubmited":feedSubmited,"feedNotSubmited":feedNotSubmited})


def printAllDB():
    print('\n\n\n')
    for x in patientData.objects.all():
        print(x)
        print(x.patientID)
        print(x.remedies)
        
def formateTime(time):
    time = time[:5]
    if int(time[:2]) > 11:
        h = str(int(time[:2])-12)
        if h == '0':
            h = '12'
        if len(h) == 1:
            h = '0' + h
        time = h+time[2:]+" PM"
    else:
        time += " AM"
        
    return time