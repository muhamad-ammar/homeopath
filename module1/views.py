from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json
from django.urls import reverse
from django.http import JsonResponse,HttpResponse
import numpy as np
# Create your views here.
import time
from .forms import LoginForm, RegisterForm, searchForm,patientForm,feedbackForm
from .models import patientData,updated_weights,userDocData,remidieAndRuubricsRecord
from datetime import datetime
from serpapi import GoogleSearch


User = get_user_model()
jsonData=[]
rubricsWithIds ={}
sliderNameList = []
feedSubmited = []
feedNotSubmited = []

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user_name = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            if password==password2:
                user = User.objects.create_user(user_name, email, password)
                user_doc_data = userDocData()
                user_doc_data.userCID = user_name+'%'+email
                usertemp = authenticate(request, username=user_name, password=password)
                user_doc_data.userDID = usertemp.id
                user_doc_data.save()
            else:
                user = None
                request.session['register_error'] = 1
        except:
            user = None
        if user != None:
            return redirect("/login")
        else:
            request.session['register_error'] = 1 # 1 == True
    return render(request, "signup.html", {"form": form})

def login_view(request):
    form = LoginForm(request.POST or None)
    error=""
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
            error="Username or Passwor not Correct"
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
    # setFeedbackStatusFalse()
    return render(request,'tab_remedy.html')

def table_view(request):
    sym=[]
    rubric=[]
    global rubricsWithIds
    
    if request.method=='GET':
        key_s=request.GET
        keyword=key_s['inputValue']
        response = requests.get(f'https://www.oorep.com/api/lookup_rep?symptom={keyword}&repertory=kent&page=0&remedyString=&minWeight=0&getRemedies=1')
        # print("table_view:",response.status_code)
        if response.status_code == 204:
            result = "noResults"
            try:
                params = {
                    "q": keyword,
                    "hl": "en",
                    "gl": "us",
                    "api_key": "6ca9b34d75c4e6827b58b4f9cd7669ec869a05b6588d6140de660bf88f32fa2a"
                }

                search = GoogleSearch(params)
                results = search.get_dict()
                # print(results["search_information"])
                if "spelling_fix" in results["search_information"].keys():
                    result += "-"+ results["search_information"]["spelling_fix"]

            except:
                pass

            return HttpResponse(result)

        res=response.text          
        jsondata=json.loads(res)
        global jsonData
        for i in jsondata[0]['results']:
            jsonData.append(i)
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
        # print(jsonData)
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
        # print("\n\n\n\n\nHelllllllllllllllllllllllllo\n\n\n\n\n")
        val_s=request.GET['values_text'].split(',')
        # print(f"VALS:{val_s}")
        # print(val_s)
        dbpatient=patientData()
        # print(dbpatient)
        pName = val_s.pop(0).split('?')[1]
        pName = pName if pName != "" else "NA"
        pAge = val_s.pop(0).split('?')[1]
        pDate = val_s.pop(0).split('?')[1]
        pGender = val_s.pop(0).split('?')[1]
        dbpatient.patientID = pName +'%'+ pDate +'%'+str(datetime.now().strftime("%H:%M:%S"))
        dbpatient.patientName = pName
        dbpatient.patientDate = pDate
        dbpatient.age = pAge if pAge != "" else "NA"
        dbpatient.gender = pGender
        result=''
        ridRem=[]
        gRem =''
        for x in val_s:
            # print(x)
            if x=="?":
                continue
            x=x.split('?')
            rid = int(x.pop(0))
            while('||' in x):
                x=x.replace('||','|')
            rem = x[0][1:]
            ridRem.append([rid,rem])
            if rem != '':
                gRem = rem

        for x,y in ridRem:
            if y != '':
                result+=str(x)+"|"+rubricsWithIds.get(x)+':'+y+'?'
            else:
                result+=str(x)+"|"+rubricsWithIds.get(x)+':'+gRem+'?'
        # print(f"RESUT:{result}")
     
        dbpatient.userDID = request.user.id
        dbpatient.remedies = result[:-1]
        dbpatient.save()
        # print("Data Saved Successfully")
        
        
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

def case_analysis(request):
    rubric_ids=[]
    rubric_data=[]
    rem_weights=[]
    rem_names=[]
    localRemflag=False
    htmlStr=''
    global jsonData
    if request.method=='GET':
        key_s=request.GET
        ids=key_s['inputValue']
        for i in ids.split(","):
            rubric_ids.append(i[1:])
        # print(rubric_ids)
        # print(jsonData)
        for i in range(len(rubric_ids)):#no of rubrics added
            for j in range(len(jsonData)):#no of searches done by the user
                if str(rubric_ids[i])==str(jsonData[j]['rubric']['id']):
                    rubric_data.append(jsonData[j])
                    break
        for i in rubric_data:
            for j in i['weightedRemedies']:
                name=j['remedy']['nameAbbrev']
                weight=j['weight']
                if name in rem_names:
                    ind=rem_names.index(name)
                    rem_weights[ind]+=weight
                else:
                    rem_names.append(name)
                    rem_weights.append(weight)
        # print(rem_names,rem_weights)
        sorted_weights=np.flip(np.argsort(rem_weights))
        htmlStr+='<thead class="thead-dark"><tr></tr><th>Rubric</th>'
        for i in range(len(rem_names)):
            htmlStr+=f'<th style="white-space: nowrap;overflow:hidden;">{rem_names[sorted_weights[i]]}({rem_weights[sorted_weights[i]]})</th>'
        htmlStr+='</tr></thead><tbody>'
        for i in range(len(rubric_data)):
            htmlStr+=f"<tr><td style='white-space: nowrap;overflow:hidden;'>{rubric_data[i]['rubric']['fullPath']}</td>"
            for j in range(len(rem_names)):
                localRemflag=False
                remIndex=sorted_weights[j]
                remName=rem_names[remIndex]
                for k in rubric_data[i]['weightedRemedies']:
                    if remName == k['remedy']['nameAbbrev']:
                        localRemflag=True
                        break
                if localRemflag:
                    localrowWeight=k['weight']
                    # print(localrowWeight,remName)
                    htmlStr+=f'<td>{localrowWeight}</td>'
                else:
                    htmlStr+=f'<td></td>'
                        
            htmlStr+='</tr></tbody>'
        f=''
        return HttpResponse(htmlStr)

def saveFeedbackForm(request):
    global sliderNameList
    if request.method == 'GET':
        pid=request.GET
        print(sliderNameList)
        # print(pid)
        patientID = sliderNameList.pop(0)
        # print(patientID)
        for x in sliderNameList:
            feedback = updated_weights()
            feedback.patientID = patientID
            feedback.rubricRemedies = x
            feedback.age = patientData.objects.get(patientID=patientID).age
            feedback.gender = patientData.objects.get(patientID=patientID).gender
            weight = pid[x]
            feedback.weight = weight
            feedback.userDID = request.user.id
            feedback.save()

            updateWheight(x.split('?')[1],x.split('|')[0],x.split('|')[1].split('?')[0],weight)
            
        dbpatient=patientData.objects.get(patientID=patientID)
        dbpatient.feedback = True
        dbpatient.save(update_fields=["feedback"])
        
    return redirect(feedback_view)

def patientFeedbackForm(request):
    result = ''
    global sliderNameList
    if request.method == 'GET':
        pid=request.GET['inputValue']
        # print("PUD ====== ",pid)
        sliderNameList = [pid]
        patient = patientData.objects.get(patientID=pid)
        name,date,ptime = pid.split('%')
        remiesRubrics = []
        for x in patient.remedies.split('?'):
            x=x.split(':')
            temp = [x.pop(0)]
            # temp = [x.pop(0).split("|")[1]] #Old code till MD1
            for y in x[0].split('|'):
                if y != '':
                    temp.append(y)
            remiesRubrics.append(temp)
        
        result += "<h3 align = 'center'>Patient Name     : "+name+" </h3>"
        result += "<h4 align = 'center'>Date             : "+date+"</h4>"
        result += "<h4 align = 'center'>Gender           : "+patient.gender+"</h4>"
        result += "<h4 align = 'center'>Age              : "+patient.age+"</h4><hr>"
        result += "<br><br><br>"
        # print(remiesRubrics)
        for x in remiesRubrics:
            z=x.pop(0)
            zx=z.replace(', ','_')
            result += "<h4>"+z.split("|")[1]+"</h4><br>"
            for y in x:
                sliderName = (zx+'?'+y).replace('_',', ')
                sliderNameList.append(sliderName)
                result += "<p>"+y+"</p>"
                if patient.feedback == False:
                    result += "<div id="+zx+">0 <input type='range' min='0' max='5' value='3' class='slider' name='"+sliderName+"'> 5 <div><br>"
                else:
                    # print(sliderName)
                    givenWeight = str(updated_weights.objects.get(patientID=pid, rubricRemedies=sliderName).weight)
                    result += "<div id="+zx+"><input type='range' min='0' max='5' value='"+givenWeight+"' class='slider' name='"+sliderName+"' disabled> "+givenWeight+" <div><br>"
            result += "<br><hr><br>"
        
        if patient.feedback == False:
            result += "<button type='submit' class='btn btn-primary' id='saveFeedback' >SAVE FEEDBACK</button>"
            
    return HttpResponse(result)

def feedback_filter_view(request):
    if request.method == 'GET':
        feedSubmited = ""
        feedNotSubmited = ""
        inputData=[]
        patient=patientData.objects.all()
        for x in request.GET['inputValue'].split(','):
            inputData.append(x.split('?')[1])
            
        if inputData[0] == '' and inputData[1] == '' and inputData[2] == '':
            patient=patientData.objects.filter(userDID = str(request.user.id))
        elif inputData[0] == '' and inputData[1] != '' and inputData[2] != '':
            patient=patientData.objects.filter(userDID = str(request.user.id), age = inputData[1], patientDate = inputData[2])
        elif inputData[0] != '' and inputData[1] == '' and inputData[2] != '':
            patient=patientData.objects.filter(userDID = str(request.user.id), patientName = inputData[0], patientDate = inputData[2])
        elif inputData[0] != '' and inputData[1] != '' and inputData[2] == '':
            patient=patientData.objects.filter(userDID = str(request.user.id), patientName = inputData[0], age = inputData[1])
        elif inputData[0] != '' and inputData[1] != '' and inputData[2] != '':
            patient=patientData.objects.filter(userDID = str(request.user.id), patientName = inputData[0], age = inputData[1], patientDate = inputData[2])
        elif inputData[0] == '' and inputData[1] == '' and inputData[2] != '':
            patient=patientData.objects.filter(userDID = str(request.user.id), patientDate = inputData[2])
        elif inputData[0] == '' and inputData[1] != '' and inputData[2] == '':
            patient=patientData.objects.filter(userDID = str(request.user.id), age = inputData[1])
        elif inputData[0] != '' and inputData[1] == '' and inputData[2] == '':
            patient=patientData.objects.filter(userDID = str(request.user.id), patientName = inputData[0])
        
        # print(str(request.user.id))
        
        for dat in patient:
            pid=dat.patientID
            page=dat.age
            pFlag = dat.feedback
            patient_name,date,ptime=pid.split('%')
            if pFlag:
                feedSubmited += f"<tr><td >{patient_name}</td><td >{date}</td><td >{formateTime(ptime)}</td><td >{page}</td><td id='useless'><div class='abc'>"
                feedSubmited += f"<input type='submit' class='btn btn-danger'  id='{pid}' value='Add feedback' name='Hello'></div></td></tr>"
            else:
                feedNotSubmited += f"<tr><td >{patient_name}</td><td >{date}</td><td >{formateTime(ptime)}</td><td >{page}</td><td id='useless'><div class='abc'>"
                feedNotSubmited += f"<input type='submit' class='btn btn-danger'  id='{pid}' value='Add feedback' name='Hello'></div></td></tr>"
        
        # print("pleas4",feedNotSubmited)
        json_data = '{"feedSubmited":"'+feedSubmited+'","feedNotSubmited":"'+feedNotSubmited+'"}'
        return HttpResponse(json_data, content_type="application/json")

@login_required(login_url='login/')
def feedback_view(request):
    global feedSubmited
    global feedNotSubmited

    # print(str(request.user.id))
    # patient=patientData.objects.all()
    # global time
    time.sleep(1)
    patient=patientData.objects.filter(userDID = str(request.user.id))
    # print('some       ',feedback_filter,'hm')
    # print(feedNotSubmited)
    
    feedSubmited = []
    feedNotSubmited = []
    for dat in patient:
        # print(str(request.user.id) == dat.userDID)
        # print(dat.userDID)
        patientarr=[]
        pid=dat.patientID
        flag=dat.feedback
        page=dat.age
        patient_name,date,ptime=pid.split('%')
        patientarr.append(patient_name)
        patientarr.append(date)
        patientarr.append(flag)
        patientarr.append(pid)
        patientarr.append(formateTime(ptime))
        patientarr.append(page)
        # print(dat.feedback," ",type(dat.feedback))
        if dat.feedback == False:
            feedNotSubmited.append(patientarr)
        if dat.feedback == True:
            feedSubmited.append(patientarr)
        
    # print('some   ok    ',feedback_filter,'hm')
    # print(feedNotSubmited)
    # print(feedSubmited)
    return render(request,'feedback.html',{"feedSubmited":feedSubmited,"feedNotSubmited":feedNotSubmited,"feedSubmitedLength":len(feedSubmited),"feedNotSubmitedLength":len(feedNotSubmited)})

def printAllDB():
    print('\n\n\n')
    for x in patientData.objects.all():
        print(x)
        print(x.patientID)
        print(x.remedies)
        
def formateTime(ptime):
    ptime = ptime[:5]
    if int(ptime[:2]) > 11:
        h = str(int(ptime[:2])-12)
        if h == '0':
            h = '12'
        if len(h) == 1:
            h = '0' + h
        ptime = h+ptime[2:]+" PM"
    else:
        ptime += " AM"
        
    return ptime

def updateWheight(remide,rubID,rubric,weight):

    remID = getRemedyID(remide)
    if(remID == False):
        return

    ratedData=remidieAndRuubricsRecord.objects.filter(remidieID = remID, rubricID = rubID)
    if ratedData.count() == 1:
        ratedData=remidieAndRuubricsRecord.objects.get(remidieID = remID, rubricID = rubID)
        rating = float(ratedData.rating)
        timesUsed = ratedData.timesUsed
        ratedData.timesUsed = 1 + timesUsed
        ratedData.rating = str((timesUsed / (timesUsed + 1)) * (rating + (int(weight) / timesUsed)))
        ratedData.save()
    elif ratedData.count() == 0:
        ratedData = remidieAndRuubricsRecord()
        ratedData.rubric = rubric
        ratedData.remidieID = remID
        ratedData.rubricID = rubID
        ratedData.remidie = remide
        ratedData.rating = weight
        ratedData.timesUsed = 1
        ratedData.save()

def getRemedyID(remedy_string):
    response =requests.get(f"https://www.oorep.com/api/lookup_mm?mmAbbrev=clarke&symptom=&page=0&remedyString={remedy_string}")
    if response.status_code == 204:
        return False
    return response.json()['results'][0]['remedy_id']

def getRating(request):
    result=''
    if request.method == 'GET':
        rubID=request.GET['rubricID']
        ratedData=remidieAndRuubricsRecord.objects.filter(rubricID = rubID).order_by('-rating')
        if ratedData.count() > 0:
            result += '<thead class="thead-dark"><tr></tr><th>Rubric</th><th style="white-space: nowrap;overflow:hidden;">Rating</th><th style="white-space: nowrap;overflow:hidden;">Times Used</th></tr></thead><tbody>'
            for object in ratedData:
                rating = float(object.rating)
                timesUsed = object.timesUsed
                remedy = object.remedy
                result += f"<tr><td style='white-space: nowrap;overflow:hidden;'>{remedy}</td><td>{round(rating, 4)}</td><td>{timesUsed}</td>"
        else:
            result = "No data Found" 
        return HttpResponse(result)

def setFeedbackStatusFalse():
    patientdata = patientData.objects.all()
    for object in patientdata:
        dbpatient=patientData.objects.get(patientID=object.patientID)
        dbpatient.feedback = False
        dbpatient.save(update_fields=["feedback"])