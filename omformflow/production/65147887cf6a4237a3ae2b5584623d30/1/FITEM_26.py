a = "事故主旨："
b = "事故內容："
c = "組織："
d = "受派人："
e = "狀態："
from omuser.models import OmUser,OmGroup
def status_format(status_id=None):
    if status_id == "0":
        final_status = "新建"
    elif status_id == "1":
        final_status = "指派"
    elif status_id == "2":
        final_status = "解決"
    return final_status
EEE = status_format(incident_status)

if group_name == None:
    group_name = ''
if assignee_name == None:
    assignee_name = ''

AA = a + incident_summary + "\n" 
BB = b + incident_note + "\n"
CC = c + group_name + "\n"
DD = d + assignee_name + "\n"
EE = e + EEE + "\n"
final = AA + BB + CC + DD + EE