c_summary_t = "變更主旨："
c_content_t = "變更內容："
c_deploy_start_date_t = "部署開始時間："
c_deploy_end_date_t = "部署結束時間："
c_group_t = "變更處理組："
c_person_t = "變更處理人員："
c_status_t = "狀態："
c_complete_time_t = "完成日期："
from omuser.models import OmUser,OmGroup
from datetime import datetime as dt
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
        final_status = "結案"
    return final_status
status_display = status_format(change_status_id)

if c_group == None:
    c_group = ''
if c_name == None:
    c_name = ''
    
nowtime = dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')
AA = c_summary_t + change_summary + "\n" 
BB = c_content_t + change_content + "\n"
FF = c_deploy_start_date_t + change_deploy_start_date + "\n"
GG = c_deploy_end_date_t + change_deploy_end_date + "\n"
CC = c_group_t + c_group + "\n"
DD = c_person_t + c_name + "\n"
EE = c_status_t + status_display + "\n"
HH = c_complete_time_t + nowtime + "\n"
final = AA + BB + FF + GG + CC + DD + EE + HH
summary_final = "變更單已經結案"