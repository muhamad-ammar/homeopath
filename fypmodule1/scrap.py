import requests
from bs4 import BeautifulSoup
chaps=[]
url='http://homeoint.org/books/kentrep/'
response=requests.get(url).text
soup = BeautifulSoup(response, 'html.parser')
stg=soup.select('strong > a')
for s in stg:
    chaps.append(s['href'])
for chap in chaps:
    chap_url=url+chap
    print(chap_url)
    response=requests.get(chap_url).text
    soup = BeautifulSoup(response, 'html.parser')
    anchor=soup.find_all('a')
    for a in anchor[1:]:
        #this is page number
        page_number=a.text.split()[1]
        page_link=url+a['href']
        print(page_number,page_link)
        resp=requests.get(page_link).text
        soup = BeautifulSoup(resp, 'html.parser')
        #this is text that will be stored in the file
        file_text=soup.text
        file = open(str(page_number)+'.txt', 'w')
        file.write(file_text)
        file.close()