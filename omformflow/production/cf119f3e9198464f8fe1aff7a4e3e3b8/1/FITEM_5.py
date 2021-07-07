# -*- coding: utf-8 -*-
import imaplib
import email,json
from email.parser import BytesParser
from email.utils import parseaddr 
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
mail_directory = 'INBOX' 
conn = imaplib.IMAP4_SSL(host) 
conn.login(smtp_user,passwd) 
conn.select(mail_directory)
status, data = conn.search(None,'unseen')
email_list = list(reversed(data[0].split()))
def decode_str(message,types):
    try:
        subject = email.header.decode_header(message)
    except:
        return None 
    if types == "Subject" or types == "File" :
        sub_bytes = subject[0][0] 
        sub_charset = subject[0][1]
        if None == sub_charset:
            subject = sub_bytes
        elif 'unknown-8bit' == sub_charset:
            subject = sub_bytes.decode('utf-8')
        else:
            subject = sub_bytes.decode(sub_charset)
        text = subject
    elif types == "From":
        format_list = []
        for m in subject:
            sub_bytes = m[0] 
            sub_charset = m[1]
            if None == sub_charset:
                if isinstance(sub_bytes, str):
                    texts =sub_bytes
                else:
                    texts = sub_bytes.decode('utf-8').strip().strip('<>')
            elif 'unknown-8bit' == sub_charset:
                texts  = sub_bytes.decode('utf-8')
            else:
                texts = sub_bytes.decode(sub_charset)
            format_list.append(texts)
        text =",".join(format_list)
    return text 
 
def get_email(num, conn):
    result = {}
    typ, content = conn.fetch(num, '(RFC822)')
    msg = BytesParser().parsebytes(content[0][1])
    sub = msg.get('Subject')
    from_ = msg.get("From")
    # Body details
    result["From"] = decode_str(from_,"From")
    result["Subject"] = decode_str(sub,"Subject")
    result["File"] = []
    for part in msg.walk(): 
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            charsets =  part.get_charsets()
            result["Body"] = body.decode(charsets[0])
        fileName = part.get_filename()  
        if None != fileName:
            file_dict = {}
            file_dict["name"] =decode_str(fileName,"File")
            file_dict["attachment"] = part.get_payload(decode=True)
            file_dict["content_type"] = part.get_content_type()
            new_file = ContentFile(file_dict["attachment"])
            file_obj = UploadedFile(new_file, file_dict["name"],file_dict["content_type"],new_file.size, None, None)
            result["File"].append(file_obj)
#                 fileName_str = decode_str(fileName,"File")
#                 att_path = os.path.join(settings.LOG_DIR,fileName_str)
            #result["File"] = part.get_payload(decode=True)
#                 fp = open(att_path, 'wb') 
#                 fp.write(part.get_payload(decode=True)) 
#                 fp.close() 
    return result
unseen_mails = []
for num in email_list:#email_list:
    mail_info = get_email(num, conn)
    mail_from = mail_info["From"]
    mail_subject = mail_info["Subject"]
    mail_content = mail_info["Body"]
    unseen_mails.append(mail_info)
#         print(mail_from)
#         print(mail_subject)
#         print(mail_content)
conn.close() 
conn.logout()


#-----------------------------------------Submit Ticket--------------------------------------------#
from omformflow.views import createOmData
from omflow.global_obj import FlowActiveGlobalObject
try:
    fa = FlowActiveGlobalObject.NameSearch("事故管理", None, "服務管理")
    event_uuid = fa.flow_uuid.hex
    para_list = receive_keyword.split(',')
    for mail_info in unseen_mails:
        param = {}
        mail_from = mail_info["From"]
        mail_subject = mail_info["Subject"]
        mail_content = mail_info["Body"]
        #如果type = ['h_group','h_title','h_status','h_level']
        #{"id":"title","value":mail_subject,"type":"titile"}
        #{"id":"status","value":<text>,"type":"status"}
        #---------------------------------------------------
        #{"id":"FORMITM_4","value":0,"type":"h_status"},\
        #{"id":"status","value":'new',"type":"status"},\
        if [item for item in para_list if item in mail_subject] and not ("Re:" in mail_subject  or "RE:" in mail_subject) :
            formdata = [
                {"id": "FORMITM_3","type": "h_status","value": "0"},\
                {"id": "FORMITM_4","type": "h_group","value": {"group": 1,"user": ""}},\
                {"id": "FORMITM_25","type": "inputbox","value": mail_from},\
                {"id": "FORMITM_28","type": "h_title","value": mail_subject},\
                {"id": "FORMITM_2","type": "areabox","value":mail_content}]
            formdata_str = json.dumps(formdata)
            param['flow_uuid'] = event_uuid
            param['formdata'] = formdata_str
            files_list = mail_info["File"]
            a = createOmData(param,user='system',files=files_list)
            result_status = a
except Exception as e:
    result_status = e