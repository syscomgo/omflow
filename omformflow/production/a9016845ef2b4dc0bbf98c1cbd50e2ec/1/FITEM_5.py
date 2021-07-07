from email.mime.text import MIMEText
import smtplib
from datetime import datetime as dt
from omuser.models import OmUser,OmGroup

foot_content = "\n ***系統自動發送，請不要直接回覆***"
all_content = email_content + foot_content

def find_user_mail(user_id=None):
    user_email = OmUser.objects.get(id=user_id)
    email = user_email.email
    return email
def find_groups_mail(group_id=None):
    group_obj = OmGroup.objects.get(id=group_id)
    group_user_list = list(group_obj.user_set.all().values_list('username',flat=True))
    user_email_list = list(OmUser.objects.filter(username__in=group_user_list).values_list(("email"),flat=True))
    email_str = ";".join(user_email_list)
    return email_str
if org_id != None and person_id == None :
    get_group_id = find_groups_mail(org_id)
    a = (get_group_id)
elif (org_id == None and person_id == None) or (org_id == "" and person_id == ""):
    a = ""
else:
    get_user_id = find_user_mail(person_id)
    a = (get_user_id)
try:
    # Create message
    message = MIMEText(all_content, 'plain', 'utf-8')
    message['Subject'] = email_subject
    message['From'] = mail_from
    message['To'] = to_email_name + ";" +a
    message['Cc'] = cc_user
    message['Bcc'] = Bcc_user
    if str(email_port) == "587":
        # Set smtp
        smtp = smtplib.SMTP(email_server,email_port)
        #smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(send_user, send_password)
    elif str(email_port) == "465":
        smtp = smtplib.SMTP_SSL(email_server, email_port)
        #smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.login(send_user, send_password)
    else:
        smtp = smtplib.SMTP(email_server, email_port)
        #smtp.set_debuglevel(1)
        smtp.ehlo()
    nowtime = dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')
    # Send msil
    #smtp.sendmail(message['From'], message['To'].split(';')+message['Cc'].split(';')+message['Bcc'].split(';'),message.as_string())
    smtp.send_message(message)
    smtp.quit()
    status = "成功"
    NUMA = 'Send mails OK!'
    e = 'Send mails OK!'
except Exception as err:
    status = "失敗"
    e = str(err)