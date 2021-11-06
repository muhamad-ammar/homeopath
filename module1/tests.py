import time

# now = datetime.now().strftime("%H:%M:%S")

# current_time = now
# print("Current Time =", current_time)
a='Cough, barking, loud:Alo|Bura||bere|'
x="pnameFilter?,pageFilter?,date?,?"
inputData=[]
for y in x.split(','):
    inputData.append(y.split('?')[1])
time.sleep(10)
print(inputData)