# import time
# import requests
# import json
from .models import remidieAndRuubricsRecord

# pName = ""
# a = pName if pName != "" else "NA"
# time.sleep(100)
# a=[]
# a.append(['a','b'])
# a.append(['c','d'])
# remedy_string='Bar-c.'
# url = f"https://www.oorep.com/api/lookup_mm?mmAbbrev=clarke&symptom=&page=0&remedyString={remedy_string}"
# resp = requests.get(url)
# res=requests.get(url).text
# jsondata=json.loads(requests.get(f"https://www.oorep.com/api/lookup_mm?mmAbbrev=clarke&symptom=&page=0&remedyString={remedy_string}").text)['results'][0]['remedy_id']
print(ratedData=remidieAndRuubricsRecord.objects.filter(remidieID = 823, rubricID = 58707))
