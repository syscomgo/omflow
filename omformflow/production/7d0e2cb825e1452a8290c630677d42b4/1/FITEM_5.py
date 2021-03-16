c_summary_t = "變更主旨："
c_content_t = "變更內容："
c_group_t = "變更處理組："
c_person_t = "變更處理人員："
c_status_t = "狀態："
from omuser.models import OmUser,OmGroup
def status_format(status_id=None):
    if status_id == "0":
        final_status = "新建"
    elif status_id == "2":
        final_status = "計畫階段"
    elif status_id == "4":
        final_status = "已排程"
    elif status_id == "5":
        final_status = "變更完成"
    elif status_id == "7":
        final_status = "結案"
    else:
        final_status = "新建"
    return final_status

if c_group_name == None:
    c_group_name = ''
if c_assignee_name == None:
    c_assignee_name = ''
    
status_display = status_format(change_status_id)

AA = c_summary_t + change_summary + "\n" 
BB = c_content_t + change_content + "\n"
CC = c_group_t + c_group_name + "\n"
DD = c_person_t + c_assignee_name + "\n"
EE = c_status_t + status_display + "\n"
final = AA + BB + CC + DD + EE
summary_final = change_summary + "   變更單已經指派給您"