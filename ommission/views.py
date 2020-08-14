import json
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from omflow.syscom.common import try_except, DataChecker, DatatableBuilder, getPostdata, listQueryBuilder, Translator
from omflow.syscom.message import ResponseAjax, statusEnum
from django.http.response import JsonResponse
from ommission.models import Missions
from django.db.models import Q
from omuser.models import OmUser
from django.db.models.aggregates import Max
from omflow.syscom.default_logger import info,debug,error
from omflow.global_obj import FlowActiveGlobalObject


@login_required
def mission_page(request):
    '''
    mission page
    input:request
    return: mission.html
    author:Pen Lin
    ''' 
    return render(request, "mission.html")

def createMission(param):
    '''
    create mission.
    input: param
    return: json
    author: Kolin Hsu
    '''
    try:
        status = True
        if isinstance(param, dict):
            new_param = param
        elif isinstance(param, str):
            new_param = json.loads(param)
        new_param['attachment'] = Missions.objects.filter(flow_uuid=new_param['flow_uuid'],data_no=new_param['data_no'],attachment=True).exists()
        Missions.objects.create(**new_param)
    except Exception as e:
        debug('create mission error:     %s' % e.__str__())
        status =  False
    finally:
        return status


def setMission(action, flow_uuid, data_no, data_id, update_user):
    '''
    create mission.
    input: param
    return: json
    author: Kolin Hsu
    '''
    try:
        status = True
        if action == 'history':
            m = Missions.objects.get(flow_uuid=flow_uuid,data_id=data_id)
            m.history = True
            m.update_user_id = update_user
            m.save()
        elif action == 'closed':
            Missions.objects.filter(flow_uuid=flow_uuid,data_no=data_no).update(closed=True)
    except Exception as e:
        debug('set mission error:     %s' % e.__str__())
        status =  False
    finally:
        return status


def updateMissionLevel(flow_uuid, data_no, level):
    '''
    create mission.
    input: param
    return: json
    author: Kolin Hsu
    '''
    try:
        status = True
        Missions.objects.filter(flow_uuid=flow_uuid,data_no=data_no,history=False).update(level=level)
    except Exception as e:
        error('update mission error:     %s' % e.__str__())
        status =  False
    finally:
        return status


def deleteMission(flow_uuid, data_no):
    '''
    create mission.
    input: param
    return: json
    author: Kolin Hsu
    '''
    try:
        status = True
        Missions.objects.filter(flow_uuid=flow_uuid,data_no=data_no).delete()
    except Exception as e:
        debug('set mission error:     %s' % e.__str__())
        status =  False
    finally:
        return status


@login_required
@try_except
def listMyMissionAjax(request):
    '''
    list my missions.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    omflow_restapi = postdata.get('omflow_restapi','')
    if not omflow_restapi:
        ticket_createtime = postdata.get('ticket_createtime','')
        ticket_createtime = ticket_createtime.split(',')
        field_list = ['title__icontains','flow_name__icontains','status__icontains','create_user_id__nick_name__icontains']
        display_field = ['flow_name','flow_uuid','level','status','title','create_user_id__nick_name','assign_group_id__display_name','assignee_id__nick_name','ticket_createtime','data_id','data_no','action','attachment']
        group_id_list = list(request.user.groups.all().values_list('id',flat=True))
        query = Missions.objects.filter((Q(assignee_id=request.user.id) | (Q(assign_group_id__in=group_id_list) & Q(assignee_id=None))) & Q(history=False) & Q(ticket_createtime__range=ticket_createtime)).values(*display_field)
        result = DatatableBuilder(request, query, field_list)
        
        #載入語言包
        language = request.COOKIES.get('django_language','zh-hant')
        data = result['data']
        if isinstance(data, str):
            pass
        elif isinstance(data, list) or isinstance(data, dict):
            for key_or_line in data:
                if isinstance(data, list):
                    line = key_or_line
                else:
                    line = data[key_or_line]
                fa = FlowActiveGlobalObject.UUIDSearch(line['flow_uuid'])
                if fa:
                    app_id = fa.flow_app_id
                    for key in line:
                        if key in['flow_name','level','status']:
                            line[key] = Translator('single_app', 'active', language, app_id, None).Do(line[key])
                        elif key == 'action':
                            action = line[key]
                            if action:
                                action1 = action.split(',')[0]
                                action2 = action.split(',')[1]
                                trans_a1 = Translator('single_app', 'active', language, app_id, None).Do(action1)
                                trans_a2 = Translator('single_app', 'active', language, app_id, None).Do(action2)
                                line[key] = trans_a1 + ',' + trans_a2
#         result['data'] = Translator('datatable_multi_app', 'active', language, None, None).Do(result['data'])
        
        info('%s list Mission success.' % request.user.username,request)
        return JsonResponse(result)
    else:
        #api使用
        group_id_list = list(request.user.groups.all().values_list('id',flat=True))
        query = Missions.objects.filter((Q(assignee_id=request.user.id) | (Q(assign_group_id__in=group_id_list) & Q(assignee_id=None))) & Q(history=False))
        result = listQueryBuilder(None, postdata, query)
        if result['status']:
            info('%s list Mission success.' % request.user.username,request)
            return ResponseAjax(statusEnum.success, result['message'], result['result']).returnJSON()
        else:
            info('%s list Mission error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()


@login_required
@try_except
def listHistoryMissionAjax(request):
    '''
    list my groups missions.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    updatetime_str = postdata.get('updatetime','')
    updatetime = updatetime_str.split(',')
    group_id = postdata.get('group_id','')
    field_list = ['title__icontains','flow_name__icontains','status__icontains','create_user__nick_name__icontains']
    display_field = ['flow_name','flow_uuid','title','create_user_id__nick_name','data_id','data_no','updatetime','assign_group_id','assign_group_id__display_name','assignee_id__nick_name','attachment']
    if group_id:
        username_list = list(OmUser.objects.filter(groups__id=group_id,delete=False).values_list('username',flat=True))
        query = Missions.objects.filter(Q(update_user_id__in=username_list) & Q(updatetime__range=updatetime) & Q(history=True)).values(*display_field)
    else:
        query = Missions.objects.filter(Q(update_user_id=request.user.username) & Q(updatetime__range=updatetime) & Q(history=True)).values(*display_field)
    result = DatatableBuilder(request, query, field_list)
        
    #載入語言包
    language = request.COOKIES.get('django_language','zh-hant')
    result['data'] = Translator('datatable_multi_app', 'active', language, None, None).Do(result['data'])
    
    info('%s list MissionHistory success.' % request.user.username,request)
    return JsonResponse(result)


@login_required
@try_except
def listHistoryMissionCurrentStateAjax(request):
    '''
    list my groups missions.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    ticket_createtime = postdata.get('ticket_createtime','')
    ticket_createtime = ticket_createtime.split(',')
    group_id = postdata.get('group_id','')
    field_list = ['title__icontains','flow_name__icontains','status__icontains','create_user__nick_name__icontains']
    display_field = ['flow_name','flow_uuid','level','status','title','ticket_createtime','data_id','data_no','assign_group_id','assign_group_id__display_name','assignee_id__nick_name','closed','stop_uuid','stop_chart_text']
    #取得我(群組)曾經處理過的任務
    if group_id:
        username_list = list(OmUser.objects.filter(groups__id=group_id,delete=False).values_list('username',flat=True))
        mission_list = list(Missions.objects.filter(Q(update_user_id__in=username_list) & Q(ticket_createtime__range=ticket_createtime) & Q(history=True) & Q(closed=False)).values('flow_uuid','data_no'))
    else:
        mission_list = list(Missions.objects.filter(Q(update_user_id=request.user.username) & Q(ticket_createtime__range=ticket_createtime) & Q(history=True) & Q(closed=False)).values('flow_uuid','data_no'))
    #將查詢結果分為兩個list  建立對照的dict--(以flow_uuid為KEY，該流程的單號組成list為VALUE)
    flow_uuid_list = []
    data_no_list = []
    mapping_dict = {}
    for i in mission_list:
        mapping_data_no_list = mapping_dict.get(i['flow_uuid'],[])
        mapping_data_no_list.append(i['data_no'])
        if len(mapping_data_no_list) == 1:
            mapping_dict[i['flow_uuid']] = mapping_data_no_list
        if i['flow_uuid'] not in flow_uuid_list:
            flow_uuid_list.append(i['flow_uuid'])
        if i['data_no'] not in data_no_list:
            data_no_list.append(i['data_no'])
    try:
        #將所有flow_uuid_list、data_no_list組合的max id查出來
        max_mission_list = list(Missions.objects.filter(flow_uuid__in=flow_uuid_list,data_no__in=data_no_list).values('flow_uuid','data_no').annotate(max_id=Max('id')))
        toomany = False
    except:
        data_no_list = data_no_list[:900]
        max_mission_list = list(Missions.objects.filter(flow_uuid__in=flow_uuid_list,data_no__in=data_no_list).values('flow_uuid','data_no').annotate(max_id=Max('id')))
        toomany = True
    #透過對照dict找出真正該撈出來的max id
    max_id_list = []
    for m in max_mission_list:
        mapping_no_list = mapping_dict.get(m['flow_uuid'],None)
        if m['data_no'] in mapping_no_list:
            max_id_list.append(m['max_id'])
    query = Missions.objects.filter(id__in=max_id_list).values(*display_field)
    result = DatatableBuilder(request, query, field_list)
    result['toomany'] = toomany
        
    #載入語言包
    language = request.COOKIES.get('django_language','zh-hant')
    result['data'] = Translator('datatable_multi_app', 'active', language, None, None).Do(result['data'])
    
    info('%s list MissionCurrentState success.' % request.user.username,request)
    return JsonResponse(result)
