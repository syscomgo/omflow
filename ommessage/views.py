import os
from django.shortcuts import render
from omuser.models import OmUser
from django.contrib.auth.decorators import login_required
from omflow.syscom.common import DatatableBuilder, UserSearch, GroupSearch, try_except
from django.utils.translation import gettext as _
from omflow.syscom.message import ResponseAjax, statusEnum
from django.http.response import JsonResponse
from ommessage.models import Messages, MessageHistory, MessageBox, HistoryGroups, HistoryMembers, MessageHistoryFiles
from django.contrib.auth.models import Group
from ast import literal_eval
from django.conf import settings
from omflow.syscom.default_logger import info


@login_required
def message_index(request,url):
    '''
    message page
    input:request
    return: message.html
    author:Pen Lin
    '''
    mes_box = url.split('/')[0]
    return render(request, "messageManage.html",locals())


@login_required
def message_compose(request, mes_his_id):
    '''
    message page
    input:request
    return: message.html
    author:Pen Lin
    ''' 
    return render(request, "compose.html")


@login_required
@try_except
def listMessagesAjax(request):
    '''
    show all messages list
    input: request
    return: messages object
    author: Kolin Hsu
    '''
    mes_box = request.POST.get('mes_box','Inbox')
    field_list=['messages_id__subject__icontains']
    if mes_box == 'Inbox':
        display_field = ['messages_id','messages_id__subject','createtime','id','create_group__name','create_user__nick_name','messagebox__read','messagehistoryfiles__main_id','content']
        messages_query = MessageHistory.objects.filterformat(*display_field,messagebox__omuser_id=request.user.id,messagebox__delete=False).exclude(create_user_id=request.user.id).distinct()
    elif mes_box == 'Sent':
        display_field = ['messages_id','messages_id__subject','createtime','id','create_group__name','create_user__nick_name','messagebox__read','messagehistoryfiles__main_id','content']
        messages_query = MessageHistory.objects.filterformat(*display_field,messagebox__omuser_id=request.user.id,create_user_id=request.user.id,messagebox__delete=False).distinct()
    elif mes_box == 'Trash':
        display_field = ['messages_id','messages_id__subject','createtime','id','create_group__name','create_user__nick_name','messagebox__read','messagehistoryfiles__main_id','content']
        messages_query = MessageHistory.objects.filterformat(*display_field,messagebox__omuser_id=request.user.id,messagebox__delete=True).distinct()
    result = DatatableBuilder(request, messages_query, field_list)
    info(request ,'%s list message success.' % request.user.username)
    return JsonResponse(result)


@login_required
@try_except
def composeMessageDetailAjax(request):
    '''
    create messages
    input: request
    return: json
    author: Kolin Hsu
    '''
    result={}
    postdata = request.POST
    messagehistory_id = postdata.get('messagehsitory_id','')
    reply_history = []
    if messagehistory_id:
        display_field = ['messages_id__subject','content','createtime','messages_id','create_user_id','create_user__nick_name','create_group_id','create_group_name','delete_users_username','receive_groups_name']
        reply_history = list(MessageHistory.objects.filterformat(*display_field,id=messagehistory_id))[0]
        #取出history members的nick_name(給引用使用）
        receivers = list(HistoryMembers.objects.filter(messagehistory_id=messagehistory_id).values_list('user_id__nick_name',flat=True))
        #取出history members的nick_name以及id（給回覆的選單使用）
        reply_users = list(HistoryMembers.objects.filter(messagehistory_id=messagehistory_id).values('user_id','user_id__nick_name'))
        #取出history groups的name以及id（給回覆的選單使用）
        reply_groups = list(HistoryGroups.objects.filter(messagehistory_id=messagehistory_id).values('group_id','group_id__name'))
        #把已刪除的使用者以及組織名稱放入陣列中
        if reply_history['delete_users_username']:
            receivers.extend(literal_eval(reply_history['delete_users_username']))
        if reply_history['receive_groups_name']:
            receivers.extend(literal_eval(reply_history['receive_groups_name']))
        result['reply_users'] = reply_users
        result['reply_groups'] = reply_groups
        result['receivers'] = receivers
    request_user_group_list = list(request.user.groups.filter(omgroup__functional_flag=False).values('id','name'))
    result['reply_history'] = reply_history
    result['request_user_group_list'] = request_user_group_list
    info(request ,'%s load message success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('請求處理成功'), result).returnJSON()


@login_required
@try_except
def createMessagesAjax(request):
    '''
    create messages
    input: request
    return: json
    author: Kolin Hsu
    '''
    #取得post資料
    postdata = request.POST
    subject = postdata.get('subject','')
    if subject:
        #建立一筆新的messages
        messages = Messages.objects.create(subject=subject)
        #建立MessageHistory
        info(request ,'%s create message success.' % request.user.username)
        return createMessageHistoryAjax(request,messages.id)
    else:
        info(request ,'%s create message error.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('提供資料格式有誤')).returnJSON()


@login_required
@try_except
def listMessageHistoryAjax(request):
    '''
    show messages detail list
    input: request
    return: messages content object
    author: Kolin Hsu
    '''
    postdata = request.POST
    messages_id = postdata.get('messages_id',None)
    if messages_id is not None:
        box_lst = list(request.user.messagebox_set.filter(messages_id=messages_id).values_list('id',flat=True))
        result = list(MessageHistory.objects.filterformat('id','create_user__nick_name','create_group_name','createtime','messagebox__read','messagehistoryfiles__main_id',messagebox__id__in=box_lst,messagebox__omuser_id=request.user.id).distinct().order_by('-createtime'))
        info(request ,'%s list message history success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('搜尋成功'), result).returnJSON()
    else:
        info(request ,'%s list message history error.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('請提供訊息編號')).returnJSON()


@login_required
@try_except
def loadMessageHistoryAjax(request):
    '''
    load messages content
    input: request
    return: messagehistory object
    author: Kolin Hsu
    '''
    postdata = request.POST
    messagehistory_id = postdata.get('messagehistory_id','')
    if messagehistory_id:
        result = {}
        try:
            mes_box = request.user.messagebox_set.get(messagehistory_id=messagehistory_id)
        except:
            mes_box = None
        if mes_box:
            #取出歷史訊息
            mes_his = list(MessageHistory.objects.filterformat('create_user__username','create_user_id','create_user__nick_name','create_group_name','createtime','content','messages_id','messages_id__subject','delete_users_username','receive_groups_name',id=messagehistory_id))[0]
            mes_his['createtime'] = mes_his['createtime']
            #取出附件
            files = list(MessageHistoryFiles.objects.filter(main_id=messagehistory_id).values('file','size','delete'))
            for file in files:
                file_path = os.path.join(settings.MEDIA_ROOT, file['file'])
                if not file['delete'] and not os.path.exists(file_path):
                    file['delete'] = True
                    file_obj = MessageHistoryFiles.objects.get(file=file['file'])
                    file_obj.delete = True
                    file_obj.save()
            mes_his['files']=files
            #取出history members的nick_name
            receivers = list(HistoryMembers.objects.filter(messagehistory_id=messagehistory_id).values_list('user_id__nick_name',flat=True))
            #把已刪除的使用者以及組織名稱放入陣列中
            if mes_his['delete_users_username']:
                receivers.extend(literal_eval(mes_his['delete_users_username']))
            if mes_his['receive_groups_name']:
                receivers.extend(literal_eval(mes_his['receive_groups_name']))
            #將box更改為已讀
            if not mes_box.read:
                mes_box.read = True
                mes_box.save()
            result['messagehistory'] = mes_his
            result['receivers'] = receivers
            info(request ,'%s load message history success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('搜尋成功'), result).returnJSON()
        else:
            return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
    else:
        info(request ,'%s load message error.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('請提供訊息編號')).returnJSON()


@login_required
@try_except
def createMessageHistoryAjax(request, *args):
    '''
    create messages content
    input: request
    return: json
    author: Kolin Hsu
    '''
    #預設變數
    create_box_id_lst=[]
    create_group_name = ''
    create_user_username = ''
    receive_users_id_lst = ''
    receive_groups_id_lst = ''
    receive_groups_name = ''
    #取得post資料
    postdata = request.POST
    messages_id = postdata.get('messages_id','')
    content = postdata.get('content','')
    files = request.FILES.getlist('attachment[]','')
    try:
        create_user_id = int(postdata.get('create_user_id'))
    except:
        create_user_id = None
    create_group_id = postdata.get('create_group_id',None)
    receive_users_id_str = postdata.get('receive_users_id_lst','')
    if receive_users_id_str:
        receive_users_id_lst = receive_users_id_str.split(',')
        receive_users_id_lst = list(map(int, receive_users_id_lst))
    receive_groups_id_str = postdata.get('receive_groups_id_lst','')
    if receive_groups_id_str:
        receive_groups_id_lst = receive_groups_id_str.split(',')
    if not messages_id:
        messages_id = args[0]
    if (create_user_id or create_group_id) and (receive_users_id_lst or receive_groups_id_lst) and messages_id:
        #將寄件人放入box_list中
        if create_user_id:
            create_box_id_lst.append(create_user_id)
            create_user_username = OmUser.objects.get(id=create_user_id).username
        #將寄件群組放入box_list中
        if create_group_id:
            create_group = Group.objects.get(id=create_group_id)
            create_group_user_list = list(create_group.user_set.all().values_list('id',flat=True))
            create_box_id_lst += create_group_user_list
            create_group_name = create_group.name
        #將收件人放入box_list中
        if receive_users_id_lst:
            create_box_id_lst += receive_users_id_lst
        #將收件群組放入box_list中
        if receive_groups_id_lst:
            for receive_group_id in receive_groups_id_lst:
                receive_omgroup_user_list = list(Group.objects.get(id=receive_group_id).user_set.all().values_list('id',flat=True))
                receive_groups_name = list(Group.objects.filter(id__in=receive_groups_id_lst).values_list('name',flat=True))
                create_box_id_lst += receive_omgroup_user_list
        #進行list的去重複
        distinct_box_lst = list(set(create_box_id_lst))
        #建立一筆新的messagehistory
        messagehistory = MessageHistory.objects.create(create_user_id=create_user_id,create_user_username=create_user_username,create_group_id=create_group_id,create_group_name=create_group_name,receive_groups_name=receive_groups_name,content=content,messages_id=messages_id)
        message = Messages.objects.get(id = messages_id)
        message.save()
        #儲存上傳的檔案
        if files:
            MessageHistoryFiles.objects.bulk_create([MessageHistoryFiles(main=messagehistory,file=file,size=file.size) for file in files])
        #list中的所有人都建立一筆MessageBox
        MessageBox.objects.bulk_create([MessageBox(messagehistory=messagehistory,messages_id=messages_id,omuser_id=n) for n in distinct_box_lst])
        #建立history members
        if receive_users_id_lst:
            if create_user_id and (create_user_id not in receive_users_id_lst):
                receive_users_id_lst.append(create_user_id)
            HistoryMembers.objects.bulk_create([HistoryMembers(messagehistory=messagehistory,user_id=n) for n in receive_users_id_lst])
        #建立history groups
        if receive_groups_id_lst:
            HistoryGroups.objects.bulk_create([HistoryGroups(messagehistory=messagehistory,group_id=n) for n in receive_groups_id_lst])
        #將creator已讀設置為true
        if create_user_id:
            create_user_box = MessageBox.objects.get(messagehistory=messagehistory,messages_id=messages_id,omuser_id=create_user_id)
            create_user_box.read = True
            create_user_box.save()
        info(request ,'%s send message success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('發送成功')).returnJSON()
    else:
        info(request ,'%s send message error.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('提供資料格式有誤')).returnJSON()


@login_required
@try_except
def deleteMessageHistoryAjax(request):
    '''
    create messages content
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = request.POST
    messagehistory_id_list = postdata.getlist('messagehistory_id[]','')
    action = postdata.get('action', 'delete')
    if messagehistory_id_list:
        if action == 'delete':
            request.user.messagebox_set.filter(messagehistory_id__in=messagehistory_id_list).update(delete=True)
            info(request ,'%s delete message success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('刪除訊息成功')).returnJSON()
        else:
            request.user.messagebox_set.filter(messagehistory_id__in=messagehistory_id_list).update(delete=False)
            return ResponseAjax(statusEnum.success, _('訊息還原成功')).returnJSON()
    else:
        info(request ,'%s delete message success.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('找不到訊息資料')).returnJSON()


@login_required
@try_except
def searchSendUserAjax(request):
    '''
    list sender
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = request.POST
    searchkey = postdata.get('searchkey','')
    field_list=['username__icontains','nick_name__icontains']
    ordercolumn = 'nick_name'
    result = UserSearch(field_list, searchkey, ordercolumn)
    info(request ,'%s search send user success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('請求處理成功'), result).returnJSON()


@login_required
@try_except
def searchSendGroupAjax(request):
    '''
    list sender
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = request.POST
    searchkey = postdata.get('searchkey','')
    adGroup = postdata.get('adGroup[]',['1','0'])
    field_list=['name__icontains']
    ordercolumn = 'name'
    result = GroupSearch(field_list, searchkey, ordercolumn,adGroup)
    info(request ,'%s search send group success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('請求處理成功'), result).returnJSON()


@login_required
@try_except
def searchGroupUserAjax(request):
    '''
    list sender
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = request.POST
    searchkey = postdata.get('searchkey','')
    field_list=['groups__id']
    ordercolumn = 'nick_name'
    result = UserSearch(field_list, searchkey, ordercolumn)
    info(request ,'%s search users by group success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('請求處理成功'), result).returnJSON()
    
