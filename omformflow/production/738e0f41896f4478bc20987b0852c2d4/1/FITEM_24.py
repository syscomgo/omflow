a = "問題主旨："
b = "問題內容："
c = "受派組織："
d = "受派人："
e = "狀態："
f = "解決內容："
g = "解決時間："
from omuser.models import OmUser,OmGroup
from datetime import datetime as dt
def find_user_name(user_id=None):
    username_ = OmUser.objects.get(id=user_id)
    name = username_.username
    return name
def find_groups_name(group_id=None):
    group_obj = OmGroup.objects.get(id=group_id)
    name = group_obj.name
    return name
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
        final_status = "調查中"
    elif status_id == "3":
        final_status = "完成"
    elif status_id == "4":
        final_status = "取消"
    return final_status

if assignee_group == None:
    assignee_group = ''
if assignee == None:
    assignee = ''

EEE = status_format(problem_status)
user_name = find_user_mail(TTT)
nowtime = dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')
AA = a + problem_summary + "\n" 
BB = b + problem_note + "\n"
CC = c + assignee_group + "\n"
DD = d + assignee + "\n"
EE = e + EEE + "\n"
FF = f + resolution_text + "\n"
GG = g + nowtime + "\n"
final = AA + BB + CC + DD + EE + FF + GG