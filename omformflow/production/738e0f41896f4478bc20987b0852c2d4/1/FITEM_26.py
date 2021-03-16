a = "問題主旨："
b = "問題內容："
c = "受派組織："
d = "受派人："
e = "狀態："
from omuser.models import OmUser,OmGroup
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
status_name = status_format(problem_status)

if group_name == None:
    group_name = ''
if assignee_name == None:
    assignee_name = ''

AA = a + problem_summary + "\n" 
BB = b + problem_note + "\n"
CC = c + group_name + "\n"
DD = d + assignee_name + "\n"
EE = e + status_name + "\n"
final = AA + BB + CC + DD + EE