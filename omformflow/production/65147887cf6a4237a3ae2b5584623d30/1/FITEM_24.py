a = "事故主旨："
b = "事故內容："
c = "組織："
d = "受派人："
e = "狀態："
f = "解決內容："
g = "解決時間："
from omuser.models import OmUser,OmGroup
from datetime import datetime as dt
def find_user_mail(user_id=None):
    user_email = OmUser.objects.get(id=user_id)
    email = user_email.email
    return email
def status_format(status_id=None):
    if status_id == "0":
        final_status = "新建"
    elif status_id == "1":
        final_status = "指派"
    elif status_id == "2":
        final_status = "解決"
    return final_status

if assignee_group == None:
    assignee_group = ''
if assignee == None:
    assignee = ''
    
EEE = status_format(incident_status)
user_name = find_user_mail(TTT)
nowtime = dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')
AA = a + incident_summary + "\n" 
BB = b + incident_note + "\n"
CC = c + assignee_group + "\n"
DD = d + assignee + "\n"
EE = e + EEE + "\n"
FF = f + resolution_text + "\n"
GG = g + nowtime + "\n"
final = AA + BB + CC + DD + EE + FF + GG