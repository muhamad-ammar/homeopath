# from datetime import datetime

# now = datetime.now().strftime("%H:%M:%S")

# current_time = now
# print("Current Time =", current_time)
a='Cough, barking, loud:Alo|Bura||bere|'
x=[a.split(':')[0]]
x.append(a.split(':')[1].split('|'))
print(x)