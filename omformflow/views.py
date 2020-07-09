import uuid, os, json, shutil, time, re, copy
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, permission_required
from omflow.syscom.schedule_monitor import schedule_Execute, cancelScheduleJob
from omflow.syscom.common import try_except, DataChecker, DatatableBuilder, getModel, FormDataChecker, FormatToFormdataList, getAppAttr, merge_formobject_items, FormatFormdataListToFormdata, check_app, getPostdata
from omflow.syscom.message import ResponseAjax, statusEnum
from omflow.global_obj import GlobalObject, FlowActiveGlobalObject
from omflow.models import SystemSetting, Scheduler, TempFiles
from omuser.views import addPermissionToRole, checkLicense
from omuser.models import OmUser
from omformflow.models import FlowWorkspace, FlowActive, WorkspaceApplication, ActiveApplication, OmdataFiles, OmdataRelation, OmdataWorklog, OmParameter, SLARule, SLAData
from django.http.response import JsonResponse
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datetime import datetime, timedelta
from omformmodel.views import OMFormModel
from omflow.syscom.omengine import OmEngine
from omflow.syscom.license import getRepository
from ommission.views import setMission, deleteMission, updateMissionLevel
from ommission.models import Missions
from django.db.models import Q
from omflow.syscom.default_logger import info,debug,error
from django.contrib.auth.models import Permission
from django.apps import apps
if check_app('ommonitor'):
    from ommonitor.views import createEvent


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def flowAppManagePage(request):
    return render(request, 'flow_app_manage.html')

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def flowManagePage(request, url):
    app_id = url.split('/')[0]
    return render(request, 'flow_manage.html', locals())

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def flowCreatePage(request):
    return render(request, 'flow_create.html', locals())

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def flowDesignPage(request, url):
    app_id = url.split('/')[0]
    flow_id = url.split('/')[1]
    return render(request, 'flow_design.html', locals())

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def workflowManagePage(request,url):
    app_id = url.split('/')[0]
    return render(request, 'workflow_manage.html', locals())

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def workflowAppManagePage(request):
    return render(request, 'workflow_app_manage.html')

@login_required
def workflowPage(request, url):
    app_id = url.split('/')[0]
    flow_uuid = url.split('/')[1]
    return render(request, 'workflow.html', locals())

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def flowvaluePage(request, url):
    app_id = url.split('/')[0]
    flow_uuid = url.split('/')[1]
    return render(request, 'flowvalue.html', locals())

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def parameterPage(request):
    return render(request, 'parameter_manage.html')

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def scheduleflowManagePage(request):
    return render(request, 'scheduleflow_manage.html')

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/page/403/')
def SLAManagePage(request):
    return render(request, 'SLA_manage.html')


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def editWorkspaceApplicationAjax(request):
    '''
    create, update, delete workspace application
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    require_field = ['action']
    #server side rule check
    postdata = getPostdata(request)
    data_checker = DataChecker(postdata, require_field)
    if data_checker.get('status') == 'success':
        #get post data
        app_name = postdata.get('app_name','')
        action = postdata.get('action','')
        app_attr_num = postdata.get('app_attr',0)
        app_attr = getAppAttr(app_attr_num)
        app_id_list = postdata.get('app_id_list','')
        if action == 'create':
            if app_name:
                try:
                    updatetime = datetime.now()
                    WorkspaceApplication.objects.create(app_name=app_name,updatetime=updatetime,user=request.user,app_attr=app_attr)
                    info(request ,'%s create WorkspaceApplication success.' % request.user.username)
                    return ResponseAjax(statusEnum.success, _('建立成功。')).returnJSON()
                except:
                    info(request ,'%s WorkspaceApplication already has same name.' % request.user.username)
                    return ResponseAjax(statusEnum.not_found, _('名稱重複。')).returnJSON()
            else:
                info(request ,'%s application name cannot be null.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, _('名稱不得為空值。')).returnJSON()
        else:
            try:
                WorkspaceApplication.objects.filter(id__in=app_id_list).delete()
                info(request ,'%s delete WorkspaceApplication success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('刪除成功。')).returnJSON()
            except:
                info(request ,'%s cannot find WorkspaceApplication.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, _('找不到該應用程式。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def listWorkspaceApplicationAjax(request):
    '''
    list workspace application
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable', None)
    if datatable:
        #function variable
        field_list=['app_name__icontains','user__username__icontains','active_app_name__icontains']
        query = ''
        app_attr = postdata.get('app_attr',['user','cloud','lib','sys'])
        updatetime = postdata.get('updatetime','')
        display_field =['id','app_name','app_attr','updatetime','active_app_name','user__username']
        query = WorkspaceApplication.objects.filterformat(*display_field,app_attr__in=app_attr,updatetime__lte=updatetime)
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list WorkspaceApplication success.' % request.user.username)
        return JsonResponse(result)
    else:
        result = list(WorkspaceApplication.objects.filterformat('id','app_name'))
        info(request ,'%s list WorkspaceApplication success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def exportWorkspaceApplicationAjax(request):
    '''
    export workspace application.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['app_id_list']
    result = []
    #get post data
    postdata = getPostdata(request)
    app_id_list = postdata.get('app_id_list','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        for app_id in app_id_list:
            app_dict = {}
            wa = WorkspaceApplication.objects.get(id=app_id)
            fw = list(FlowWorkspace.objects.filter(flow_app_id=app_id).values('flow_name','description','flowobject','config','flow_app_id__app_name'))
            for f in fw:
                f['flowobject'] = json.loads(f['flowobject'])
                f['config'] = json.loads(f['config']) 
            app_dict['app_name'] = wa.app_name
            app_dict['app_attr'] = wa.app_attr
            app_dict['flow_list'] = fw
            result.append(app_dict)
        info(request ,'%s export WorkspaceApplication success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('匯出成功。'), result).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def importWorkspaceApplicationAjax(request):
    '''
    import workspace application.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['app_list']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        app_list = postdata.get('app_list',[])
        result = importWorkspaceApplication(app_list, request.user)
        if result['status']:
            info(request ,'%s import WorkspaceApplication success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('匯入成功。')).returnJSON()
        else:
            info(request ,'%s import WorkspaceApplication error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def importWorkspaceApplication(app_list, user):
    try:
        #function variable
        message = ''
        status = True
        app_id_list = []
        updatetime = datetime.now()
        #get data
        if isinstance(app_list, str):
            app_list = json.loads(app_list)
        if isinstance(app_list, dict):
            app_list = [app_list]
        for app in app_list:
            app_name = app['app_name']
            app_attr = app['app_attr']
            flow_list = app['flow_list']
            wa = WorkspaceApplication.objects.create(app_name=app_name,updatetime=updatetime,user=user,app_attr=app_attr)
            app_id_list.append(wa.id)
            flow_name_list = []
            for flow in flow_list:
                if flow['flow_name'] not in flow_name_list:
                    flow_name_list.append(flow['flow_name'])
                    flow['app_id'] = wa.id
                    flow['formobject'] = json.dumps(flow['flowobject'].get('form_object',''))
                    flow['flowobject'] = json.dumps(flow['flowobject'])
                    flow['config'] = json.dumps(flow['config'])
                    result = createFlowWorkspace(flow, user)
                    if not result:
                        status = False
                        message += _('流程建立失敗。')
                        break
                else:
                    status = False
                    message += _('同應用內不可有重複的流程名稱。')
                    break
    except Exception as e:
        message = e.__str__()
        status = False
        WorkspaceApplication.objects.filter(id__in=app_id_list).delete()
    finally:
        return {'status':status, 'message':message, 'id_list':app_id_list}


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def createFlowWorkspaceAjax(request):
    '''
    create custom form, flow, setting.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    result = {}
    require_field = ['flow_name','app_id']
    #server side rule check
    postdata = getPostdata(request)
    data_checker = DataChecker(postdata, require_field)
    flow_name = postdata.get('flow_name','')
    app_id = postdata.get('app_id','')
    if data_checker.get('status') == 'success':
        same_name = FlowWorkspace.objects.filter(flow_app_id=app_id,flow_name=flow_name).count()
        if same_name == 0:
            result = createFlowWorkspace(postdata, request.user)
            if result:
                info(request ,'%s create FlowWorkspace success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('建立成功。'), result).returnJSON()
            else:
                info(request ,'%s create FlowWorkspace error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, _('建立失敗。')).returnJSON()
        else:
            info(request ,'%s create fail, FlowWorkspace has same name in this application.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, _('重複名稱。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


def createFlowWorkspace(param,user):
    '''
    create custom form, flow, setting.
    input: request
    return: json
    author: Kolin Hsu
    '''
    try:
        #function varaible
        result = {}
        subflow = []
        #get post data
        app_id = param.get('app_id','')
        flow_name = param.get('flow_name','')
        description = param.get('description','')
        formobject = param.get('formobject','')
        flowobject = param.get('flowobject','')
        config = param.get('config','')
        #map subflow object and config
        subflow_list = json.loads(flowobject).get('subflow','')
        subflow_config_list = json.loads(config).get('subflow','')
        for s in subflow_list:
            subflow_obj = {}
            for s_c in subflow_config_list:
                if str(s['uid']) == str(s_c['uid']):
                    subflow_obj['flow_name'] = s_c.get('name','')
                    subflow_obj['description'] = s_c.get('description','')
                    subflow_obj['flowobject'] = s
                    subflow_obj['flowcounter'] = s.get('flow_item_counter')
            subflow.append(subflow_obj)
        subflow = json.dumps(subflow)
        #create flow workspace
        flowworkspace = FlowWorkspace.objects.create(flow_name=flow_name,\
                                     create_user=user,formobject=formobject,\
                                     flowobject=flowobject,config=config,subflow=subflow,\
                                     description=description,updatetime=datetime.now(),\
                                     flow_app_id=app_id)
        result['flow_id'] = flowworkspace.id
        result['flow_name'] = flowworkspace.flow_name
        return result
    except Exception as e:
        debug(e.__str__())
        return False


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def getOutsideFlowAjax(request):
    '''
    get outside's input and outside's output
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    app_name = postdata.get('app_name','')
    flow_name = postdata.get('flow_name','')
    if app_name and flow_name:
        fa = FlowActiveGlobalObject.NameSearch(flow_name, None, app_name)
        form_items = json.loads(fa.formobject)['items']
        flow_items = json.loads(fa.flowobject)['items']
        #組合start point input 以及 end point output
        s = False
        e = False
        for flow_item in flow_items:
            if flow_item['type'] == 'start':
                outside_input = flow_item['config']['input']
                for line in outside_input:
                    line['name'] = '$(' + line['name'] + ')'
                    line.pop('value')
                s = True
            elif flow_item['type'] == 'end':
                outside_output = flow_item['config']['output']
                for line in outside_output:
                    line.pop('value')
                e = True
            if s and e:
                break
        #組合表單內容
        for form_item in form_items:
            if form_item['id'][:8] == 'FORMITM_':
                config = form_item['config']
                form_dict = {}
                form_dict['require'] = config.get('require',False)
                if form_item['type'] == 'h_group':
                    form_dict['name'] = '#G1(' + form_item['id'] + ')'
                    form_dict['des'] = config.get('group_title','')
                    form_dict_user = {}
                    form_dict_user['require'] = config.get('require',False)
                    form_dict_user['name'] = '#G2(' + form_item['id'] + ')'
                    form_dict_user['des'] = config.get('user_title','')
                    outside_input.append(form_dict)
                    outside_input.append(form_dict_user)
                else:
                    form_dict['name'] = '#(' + form_item['id'] + ')'
                    form_dict['des'] = config.get('title','')
                    outside_input.append(form_dict)
        result = {'outside_input':outside_input,'outside_output':outside_output}
    else:
        result = None
    info(request ,'%s load outside flow success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def getInsideFlowAjax(request):
    '''
    get inside's input and outside's output
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    app_name = postdata.get('app_name','')
    flow_name = postdata.get('flow_name','')
    if flow_name:
        fw = FlowWorkspace.objects.get(flow_name=flow_name,flow_app_id__app_name=app_name)
        form_items = json.loads(fw.formobject)['items']
        flow_items = json.loads(fw.flowobject)['items']
        #組合start point input 以及 end point output
        s = False
        e = False
        for flow_item in flow_items:
            if flow_item['type'] == 'start':
                outside_input = flow_item['config']['input']
                for line in outside_input:
                    line['name'] = '$(' + line['name'] + ')'
                    line.pop('value')
                s = True
            elif flow_item['type'] == 'end':
                outside_output = flow_item['config']['output']
                for line in outside_output:
                    line.pop('value')
                e = True
            if s and e:
                break
        #組合表單內容
        for form_item in form_items:
            if form_item['id'][:8] == 'FORMITM_':
                config = form_item['config']
                form_dict = {}
                form_dict['require'] = config.get('require',False)
                if form_item['type'] == 'h_group':
                    form_dict['name'] = '#G1(' + form_item['id'] + ')'
                    form_dict['des'] = config.get('group_title','')
                    form_dict_user = {}
                    form_dict_user['require'] = config.get('require',False)
                    form_dict_user['name'] = '#G2(' + form_item['id'] + ')'
                    form_dict_user['des'] = config.get('user_title','')
                    outside_input.append(form_dict)
                    outside_input.append(form_dict_user)
                else:
                    form_dict['name'] = '#(' + form_item['id'] + ')'
                    form_dict['des'] = config.get('title','')
                    outside_input.append(form_dict)
        result = {'outside_input':outside_input,'outside_output':outside_output}
    else:
        result = None
    info(request ,'%s load inside flow success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def updateFlowWorkspaceAjax(request):
    '''
    update custom form, flow, setting.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    same_name = 0
    result = {}
    subflow = []
    fw_obj = {}
    require_field = ['flow_name','flow_id']
    field_list = ['flow_name','description','formobject','flowobject','config']
    #server side rule check
    postdata = getPostdata(request)
    data_checker = DataChecker(postdata, require_field)
    if data_checker.get('status') == 'success':
        #get post data
        flowobject = postdata.get('flowobject','')
        config = postdata.get('config','')
        flow_name = postdata.get('flow_name','')
        flow_id = postdata.get('flow_id','')
        fw = FlowWorkspace.objects.get(id=flow_id)
        if fw.flow_name != flow_name:
            same_name = FlowWorkspace.objects.filter(flow_name=flow_name).count()
        if not same_name:
            #map subflow object and config
            subflow_list = json.loads(flowobject).get('subflow','')
            subflow_config_list = json.loads(config).get('subflow','')
            for s in subflow_list:
                for s_c in subflow_config_list:
                    if str(s['uid']) == str(s_c['uid']):
                        subflow_obj = {}
                        subflow_obj['flow_name'] = s_c.get('name','')
                        subflow_obj['description'] = s_c.get('description','')
                        subflow_obj['flowobject'] = s
                        subflow_obj['flowcounter'] = s.get('flow_item_counter')
                subflow.append(subflow_obj)
            #update flowworkspace model
            for i in field_list:
                fw_obj[i] = postdata.get(i,'')
            fw_obj['subflow'] = json.dumps(subflow)
            fw_obj['updatetime'] = datetime.now()
            FlowWorkspace.objects.filter(id=flow_id).update(**fw_obj)
            result['flow_id'] = flow_id
            info(request ,'%s update FlowWorkspace success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('更新成功。'), result).returnJSON()
        else:
            info(request ,'%s update FlowWorkspace error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, _('重複流程名稱。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def listFlowWorkspaceAjax(request):
    '''
    list custom form, flow, setting.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['flow_name__icontains','description__icontains']
    query = ''
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    app_id = postdata.get('app_id','')
    if datatable:
        updatetime = postdata.get('updatetime','')
        display_field =['id','flow_name','updatetime','description']
        query = FlowWorkspace.objects.filter(flow_app_id=app_id,updatetime__lte=updatetime).values(*display_field)
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list FlowWorkspace success.' % request.user.username)
        return JsonResponse(result)
    else:
        flow_id = postdata.get('flow_id',None)
        if flow_id == 'newflow':
            result = list(FlowWorkspace.objects.filter(flow_app_id=app_id).values('flow_name'))
        elif flow_id:
            result = list(FlowWorkspace.objects.filter(flow_app_id=app_id).exclude(id=flow_id).values('flow_name'))
        info(request ,'%s list FlowWorkspace success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def loadFlowWorkspaceAjax(request):
    '''
    load custom form, flow, setting.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id = postdata.get('flow_id','')
    if checker.get('status') == 'success':
        result = list(FlowWorkspace.objects.filter(id=flow_id).values('id','flow_name','description','formobject','flowobject','config'))[0]
        info(request ,'%s load FlowWorkspace success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def deleteFlowWorkspaceAjax(request):
    '''
    delete custom form, flow, setting.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id_list = postdata.get('flow_id','')
    if checker.get('status') == 'success':
        FlowWorkspace.objects.filter(id__in=flow_id_list).delete()
        info(request ,'%s delete FlowWorkspace success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('刪除成功。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def copyFlowWorkspaceAjax(request):
    '''
    copy custom form, flow, setting.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_id','app_id']
    display_field = ['flow_name','formobject','flowobject','config','subflow','create_user_id','createtime','updatetime']
    flow_name_list = []
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id_list = postdata.get('flow_id','')
    app_id = postdata.get('app_id','')
    thistime = datetime.now()
    if checker.get('status') == 'success':
        fw_list = list(FlowWorkspace.objects.filter(id__in=flow_id_list).values(*display_field))
        for fw in fw_list:
            flow_name_list.append(fw['flow_name'])
            fw['create_user_id'] = request.user.id
            fw['createtime'] = thistime
            fw['updatetime'] = thistime
            fw['flow_app_id'] = app_id
        duplicate_name = list(FlowWorkspace.objects.filter(flow_app_id=app_id,flow_name__in=flow_name_list).values_list('flow_name',flat=True))
        if len(duplicate_name):
            info(request ,'%s copy FlowWorkspace error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, _('複製失敗，該應用內含有同樣名稱之流程。')).returnJSON()
        else:
            FlowWorkspace.objects.bulk_create([FlowWorkspace(**fw) for fw in fw_list])
            info(request ,'%s copy FlowWorkspace success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('複製成功。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def listFlowVersionAjax(request):
    '''
    list flow version.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_uuid']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    if checker.get('status') == 'success':
        flowactive = list(FlowActive.objects.filterformat('flow_uuid','flow_name','version','description',flow_uuid=flow_uuid))
        info(request ,'%s list flow version success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), flowactive).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def deployWorkspaceApplicationAjax(request):
    '''
    deploy workspace application.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['w_app_id']
    #get post data
    postdata = getPostdata(request)
    a_app_id = postdata.get('a_app_id','')
    #check license
    if settings.OMFLOW_TYPE == 'server':
        if a_app_id:
            omlicense = checkLicense('app', True)
        else:
            omlicense = checkLicense('app')
    else:
        omlicense = True
    if omlicense:
        #server side rule check
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            result = deployWorkspaceApplication(postdata, request.user)
            if result['status']:
                info(request ,'%s deploy WorkspaceApplication success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('上架成功。')).returnJSON()
            else:
                info(request ,'%s deploy WorkspaceApplication error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, result.get('message','')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s the license error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, _('應用流程數量已達上限。')).returnJSON()


def deployWorkspaceApplication(postdata, user):
    try:
        #function variable
        status = False
        message = ''
        all_success = True
        flow_mapping = {}
        lside_pid = postdata.get('lside_pid','')
        w_app_id = postdata.get('w_app_id','')
        app_name = postdata.get('app_name','')
        a_app_id = postdata.get('a_app_id','')
        #建立app
        caa_result = createActiveApplication(w_app_id, app_name, a_app_id, user)
        if caa_result['status']:
            new_app_id = caa_result['app_id']
            new_app_name = caa_result['app_name']
            undeploy_list = caa_result['undeploy_list']
            a_app_id = caa_result['a_app_id']
            app_attr = caa_result.get('app_attr','user')
            #建立舊流程與新流程的對應關係
            fw_list = list(FlowWorkspace.objects.filterformat('id','flow_name',flow_app_id=w_app_id))
            if a_app_id:
                a_app_id_list = list(ActiveApplication.objects.filter(app_name=new_app_name).values_list('id',flat=True))
                fa_list = list(FlowActive.objects.filter(flow_app_id__in=a_app_id_list,parent_uuid=None).values('flow_uuid','flow_name'))
                for fw in fw_list:
                    mapping = False
                    for fa in fa_list:
                        if fw['flow_name'] == fa['flow_name']:
                            mapping = True
                            flow_mapping[fw['id']] = fa['flow_uuid']
                            break
                    if not mapping:
                        flow_mapping[fw['id']] = uuid.uuid4()
            else:
                for fw in fw_list:
                    flow_mapping[fw['id']] = uuid.uuid4()
            #建立該app的所有流程
            flow_list = []
            status = True
            for flow_id in flow_mapping:
                cfa_result = createFlowActive(new_app_id, flow_id, flow_mapping[flow_id], caa_result['version'], user, app_attr)
                flow_list.append(cfa_result)
                if not cfa_result['status']:
                    status = False
                    break
            if status:
                #create main flow python
                for flow in flow_list:
                    flowmaker = flowMaker(flow['flow_uuid'],flow['flowobject'],flow['version'],flow['subflow_mapping_dict'])
                    if not flowmaker:
                        all_success = False
                        break
            else:
                all_success = False
            if all_success:
                #找出舊版流程的schedule
                sch_dict = {}
                if undeploy_list:
                    sch_list = list(Scheduler.objects.filter(flowactive_id__in=undeploy_list).values('id','flowactive_id__flow_uuid'))
                    if sch_list:
                        for sch in sch_list:
                            sch_flow_uuid = sch['flowactive_id__flow_uuid'].hex
                            if sch_dict.get(sch_flow_uuid,''):
                                sch_dict[sch_flow_uuid].append(sch['id'])
                            else:
                                sch_dict[sch_flow_uuid] = [sch['id']]
                #將對應上的排程更新至新的流程
                for flow in flow_list:
                    if sch_dict.get(flow['flow_uuid'],''):
                        sch_id_list = sch_dict.pop(flow['flow_uuid'])
                        Scheduler.objects.filter(id__in=sch_id_list).update(flowactive_id=flow['flow_id'])
                #刪除剩餘排程
                if sch_dict:
                    delete_sch_list = []
                    for k in sch_dict:
                        delete_sch_list += sch_dict[k]
                    deleteSchedule(delete_sch_list)
                #建立側邊選單，如果是lib則不建立，如果是服務管理則只能放在第一層
                if app_attr in ['sys','user','cloud']:
                    if app_attr == 'sys':
                        removeSidebar(a_app_id)
                    elif lside_pid == 'disable':
                        lside_pid = removeSidebar(a_app_id)
                    createSidebar(flow_list, new_app_id, new_app_name, lside_pid)
                status = True
                message = _('上架成功。')
            else:
                #建立失敗時要刪除剛才建立的所有資料
                for flow in flow_list:
                    if flow.get('flow_id',''):
                        deleteFlowActive(flow['flow_id'])
                #同時恢復上一版的流程
                for re_id in undeploy_list:
                    redeployFlow(re_id)
                #刪除新增的app，並重啟舊的app
                ActiveApplication.objects.get(id=new_app_id).delete()
                if a_app_id:
                    aa = ActiveApplication.objects.get(id=a_app_id)
                    aa.undeploy_flag = False
                    aa.save()
                    FlowActiveGlobalObject.setAppNameDict(aa.app_name, aa.id)
                message = _('上架流程時失敗。')
        else:
            message = _('上架應用時失敗。')
    except Exception as e:
        debug(e.__str__())
        message = e.__str__()
    finally:
        return {'status':status, 'message':message}
        


def createActiveApplication(w_app_id, app_name, a_app_id, user):
    '''
    create active application
    input: w_app_id, a_app_id, user
    return: json
    author: Kolin Hsu
    '''
    try:
        result = {}
        result['status'] = True
        result['undeploy_list'] = []
        fw_flow_name_list = list(FlowWorkspace.objects.filter(flow_app_id=w_app_id).values_list('flow_name',flat=True))
        flow_name_list = []
        for i in fw_flow_name_list:
            if i in flow_name_list:
                result['status'] = False
                result['message'] = _('流程名稱重複，同一個應用程式不可有重複的流程名稱。')
                break
            else:
                flow_name_list.append(i)
        if result['status']:
            wa = WorkspaceApplication.objects.get(id=w_app_id)
            app_attr = wa.app_attr
            if a_app_id:
                aa = ActiveApplication.objects.get(id=a_app_id)
                if aa.app_attr in ['sys','lib'] and aa.app_attr != app_attr:
                    result['status'] = False
                    result['message'] = _('無法覆蓋預設流程。')
                else:
                    version = int(aa.version) + 1
                    app_name = aa.app_name
                    wa.active_app_name = app_name
                    wa.save()
                    if aa.undeploy_flag == False:
                        uaa_result = undeployActiveApplication(a_app_id, user)
                        result['undeploy_list'] = uaa_result['flow_id_list']
            else:
                if len(ActiveApplication.objects.filter(app_name=app_name,undeploy_flag=False)) == 0:
                    aa_list = list(ActiveApplication.objects.filter(app_name=app_name).order_by('version').reverse())
                    if aa_list:
                        aa = aa_list[0]
                        version = aa.version + 1
                        a_app_id = aa.id
                    else:
                        version = 1
                else:
                    result['status'] = False
                    result['message'] = _('重複的應用程式名稱。')
            if result['status']:
                updatetime = datetime.now()
                new_aa = ActiveApplication.objects.create(app_name=app_name,user=user,updatetime=updatetime,version=version,app_attr=app_attr)
                #set global
                FlowActiveGlobalObject.setAppNameDict(new_aa.app_name, new_aa.id)
                result['version'] = version
                result['app_id'] = new_aa.id
                result['app_name'] = new_aa.app_name
                result['a_app_id'] = a_app_id
                result['app_attr'] = app_attr
        return result
    except Exception as e:
        result['status'] = False
        result['message'] = e.__str__()
        return result
    

def undeployActiveApplication(app_id, user):
    '''
    undeploy active application
    input: app_id, user
    return: json
    author: Kolin Hsu
    '''
    try:
        aa = ActiveApplication.objects.get(id=app_id)
        app_attr = aa.app_attr
        #delete global
        FlowActiveGlobalObject.deleteAppNameDict(aa.app_name)
        aa.undeploy_flag = True
        aa.updatetime = datetime.now()
        aa.user = user
        aa.save()
        flow_id_list = list(FlowActive.objects.filter(flow_app_id=app_id,parent_uuid=None).values_list('id',flat=True))
        undeployFlow(flow_id_list)
        result = {'app_attr':app_attr,'flow_id_list':flow_id_list}
        return flow_id_list
    except Exception as e:
        debug(e.__str__())
        result = {'app_attr':'','flow_id_list':[]}
    finally:
        return result


def createFlowActive(new_app_id, flowworkspace_id, flow_uuid, version, user, app_attr):
    '''
    create flow active
    input: flowworkspace_id, flowactive_id, version, user
    return: json
    author: Kolin Hsu
    '''
    try:
        #bug 'title_field','status_field','display_field','search_field'
        #function variable
        result = {}
        active_obj = {}
        tf_list = ['fp_show','attachment','relation','worklog','history','mission','flowlog','api']
        subflow_mapping_dict = {}
        display_field = {'data_no':'資料編號','stop_chart_text':'關卡名稱','error':'是否異常','error_message':'錯誤訊息','create_user':'開單人員','updatetime':'更新時間'}
        fw = FlowWorkspace.objects.get(id=flowworkspace_id)
        flow_name = fw.flow_name
        #build flowactive dict
        config = json.loads(fw.config)
        active_obj['flow_name'] = flow_name
        active_obj['flow_uuid'] = flow_uuid
        active_obj['create_user_id'] = user.id
        active_obj['description'] = fw.description
        active_obj['attr'] = app_attr
        active_obj['version'] = version
        active_obj['formobject'] = fw.formobject
        active_obj['flowobject'] = fw.flowobject
        active_obj['formcounter'] = json.loads(fw.formobject).get('form_item_counter')
        active_obj['flowcounter'] = json.loads(fw.flowobject).get('flow_item_counter')
        active_obj['display_field'] = json.dumps(display_field)
        active_obj['flow_uid'] = str(json.loads(fw.flowobject).get('uid'))
        active_obj['flow_app_id'] = new_app_id
        p = config.get('permission','')
        if isinstance(p, list):
            permission = json.dumps(p)
        else:
            permission = p
        active_obj['permission'] = permission
        for tf in tf_list:
            active_obj[tf] = config.get(tf,False)
        #取得快速操作設定 / 取得人工點表單設計
        action1 = {}
        action2 = {}
        formpoint_formobject_items_list = []
        formpoint_formobject_items_list.append(json.loads(fw.formobject)['items'])
        flow_items = json.loads(fw.flowobject)['items']
        for item in flow_items:
            if item['type'] == 'form':
                config = item['config']
                if config['form_object']:
                    formpoint_formobject_items_list.append(config['form_object']['items'])
                if config['action1']:
                    action1[item['id']] = {'text':config['action1_text'], 'input':config['input1']}
                if config['action2']:
                    action2[item['id']] = {'text':config['action2_text'], 'input':config['input2']}
        if action1:
            active_obj['action1'] = json.dumps(action1)
        if action2:
            active_obj['action2'] = json.dumps(action2)
        #組合子流程
        subflow = json.loads(fw.subflow)
        sb_flow_uuid_list = []
        if len(subflow):
            subflow_list = list(FlowActive.objects.filter(parent_uuid=flow_uuid).values('flow_uuid','flow_name').distinct())
            sub_name_dict = {}
            for i in subflow_list:
                sub_name_dict[i['flow_name']] = i['flow_uuid'].hex
            for sb_d in subflow:
                subflow_name = sb_d['flow_name']
                if sub_name_dict.get(subflow_name,''):
                    sb_flow_uuid = sub_name_dict.get(subflow_name,'')
                else:
                    sb_flow_uuid = uuid.uuid4().hex
                sb_flow_uuid_list.append(sb_flow_uuid)
                sb_d['flow_uuid'] = sb_flow_uuid
                sb_d['parent_uuid'] = flow_uuid.hex
                sb_d['version'] = version
                sb_d['flowobject'] = json.dumps(sb_d['flowobject'])
                sb_d['flow_uid'] = str(json.loads(sb_d['flowobject'])['uid'])
                sb_d['flow_app_id'] = new_app_id
                #取得快速操作設定
                sub_action1 = {}
                sub_action2 = {}
                sub_flow_items = json.loads(fw.flowobject).get('items')
                for sub_item in sub_flow_items:
                    if sub_item['type'] == 'form':
                        sub_config = sub_item['config']
                        if config['form_object']:
                            formpoint_formobject_items_list.append(config['form_object']['items'])
                        if sub_config['action1']:
                            sub_action1[sub_item['id']] = {'text':sub_config['action1_text'], 'input':sub_config['input1']}
                        if sub_config['action2']:
                            sub_action2[sub_item['id']] = {'text':sub_config['action2_text'], 'input':sub_config['input2']}
                if sub_action1:
                    sb_d['action1'] = json.dumps(sub_action1)
                if sub_action2:
                    sb_d['action2'] = json.dumps(sub_action2)
                s_uid = str(json.loads(sb_d['flowobject'])['uid'])
                subflow_mapping_dict[s_uid] = sb_flow_uuid
        #合併所有(包含子流程)人工點的表單設計
        merge_formobject = merge_formobject_items(formpoint_formobject_items_list)
        active_obj['merge_formobject'] = json.dumps(merge_formobject)
        #create flowactive
        flowactive = FlowActive.objects.create(**active_obj)
        #set global
        FlowActiveGlobalObject.setFlowActive(flowactive)
        #create main flow model
        formmodel = OMFormModel.deployModel(flow_uuid.hex, flow_name, int(flowactive.formcounter))
        #add permission to role
        if p:
            for p_config in p:
                per_list = []
                role_name = p_config.get('role_name','')
                value = p_config.get('value',{})
                if value.get('view',False):
                    p_code_name = 'Omdata_' + flow_uuid.hex + '_View'
                    per_list.append(p_code_name)
                if value.get('delete',False):
                    p_code_name = 'Omdata_' + flow_uuid.hex + '_Delete'
                    per_list.append(p_code_name)
                if value.get('modify',False):
                    p_code_name = 'Omdata_' + flow_uuid.hex + '_Modify'
                    per_list.append(p_code_name)
                if value.get('add',False):
                    p_code_name = 'Omdata_' + flow_uuid.hex + '_Add'
                    per_list.append(p_code_name)
                addPermissionToRole(role_name, per_list)
        if formmodel:
            #create subflow
            flowmaker_sub = True
            if len(subflow):
                for sb_d in subflow:
                    #把merge_formobject放入subflow
                    sb_d['merge_formobject'] = json.dumps(merge_formobject)
                    #製作flow main.py
                    sb_flow_uuid = sb_d['flow_uuid']
                    s_flowobject = sb_d['flowobject']
                    flowmaker_sub = flowMaker(sb_flow_uuid,s_flowobject,version,subflow_mapping_dict)
                    if not flowmaker_sub:
                        break
                if flowmaker_sub:
                    FlowActive.objects.bulk_create([FlowActive(**sb_d) for sb_d in subflow])
                    sfa_list = FlowActive.objects.filter(flow_uuid__in=sb_flow_uuid_list,undeploy_flag=False)
                    for sfa in sfa_list:
                        FlowActiveGlobalObject.setFlowActive(sfa)
            if flowmaker_sub:
                #set result
                result['status'] = True
                result['flow_id'] = flowactive.id
                result['flow_uuid'] = flow_uuid.hex
                result['flow_name'] = flow_name
                result['version'] = version
                result['flowobject'] = fw.flowobject
                result['subflow_mapping_dict'] = subflow_mapping_dict
                return result
            else:
                result['flow_id'] = flowactive.id
                result['flow_uuid'] = flow_uuid.hex
                result['flow_name'] = flow_name
                result['status'] = False
                return result
        else:
            result['flow_id'] = flowactive.id
            result['flow_uuid'] = 'none'
            result['flow_name'] = flow_name
            result['status'] = False
            return result
    except Exception as e:
        debug(e.__str__())
        result['flow_uuid'] = 'none'
        result['flow_name'] = flow_name
        result['status'] = False
        return result


def deleteFlowActive(flowactive_id):
    '''
    delete flow active
    input: flowactive_id
    return: boolean
    author: Kolin Hsu
    '''
    try:
        #刪除主流程
        fa = FlowActiveGlobalObject.deleteFlowActive(None, flowactive_id)
        flow_uuid = fa.flow_uuid.hex
        fa.delete()
        removePythonFile(flow_uuid)
        #刪除子流程
        subflow_uuid_list = list(FlowActive.objects.filter(parent_uuid=flow_uuid).values_list('flow_uuid',flat=True))
        for subflow_uuid in subflow_uuid_list:
            removePythonFile(subflow_uuid)
            fa_b = FlowActiveGlobalObject.deleteFlowActive(flow_uuid, None)
            fa_b.delete()
        #如果該筆資料為最後一筆，刪除model
        if len(FlowActive.objects.filter(flow_uuid=flow_uuid)) == 0:
            OMFormModel.deleteModel(flow_uuid)
    except Exception as e:
        debug(e.__str__())


def createSidebar(flow_list, app_id, app_name, lside_pid):
    '''
    deploy custom form, flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    try:
        #function variable
        icon = 'bomb'
        app_icon = 'laptop'
        sidebar_design_new = []
        not_put_in_list = True
        app_list = []
        #先組合當前app的list
        if app_name == '服務管理':
            lside_pid = ''
            app_icon = 'headphones'
        elif app_name == '系統設定':
            lside_pid = 'syssetting'
            icon = 'circle-o'
        app_obj = {}
        app_sidebar_id = 'app-' + str(app_id)
        app_obj['id'] = app_sidebar_id
        app_obj['name'] = app_name
        app_obj['p_id'] = lside_pid
        app_obj['flow_uuid'] = 'app'
        app_obj['icon'] = app_icon
        app_list.append(app_obj)
        for flow in flow_list:
            lside_obj = {}
            lside_obj['id'] = 'formflow-' + flow['flow_uuid']
            lside_obj['name'] = flow['flow_name']
            lside_obj['p_id'] = app_sidebar_id
            lside_obj['flow_uuid'] = flow['flow_uuid']
            lside_obj['icon'] = icon
            app_list.append(lside_obj)
        #set app to left side bar
        sidebar_design = GlobalObject.__sidebarDesignObj__['sidebar_design']
        root_count = 0
        for item in sidebar_design:
            if item['p_id'] == '':
                root_count += 1
            if app_name == '服務管理' and root_count == 3 and item['p_id'] == '':
                sidebar_design_new.extend(app_list)
                sidebar_design_new.append(item)
                not_put_in_list = False
            elif item['id'] == lside_pid:
                sidebar_design_new.append(item)
                sidebar_design_new.extend(app_list)
                not_put_in_list = False
            else:
                sidebar_design_new.append(item)
        if not_put_in_list:
            sidebar_design_new.extend(app_list)
        #update database
        sidebar_design_str = json.dumps(sidebar_design_new)
        systemsetting = SystemSetting.objects.get(name='sidebar_design')
        systemsetting.value = sidebar_design_str
        systemsetting.save()
        #update global object
        updatetime = str(datetime.now())
        GlobalObject.__sidebarDesignObj__['sidebar_design'] = sidebar_design_new
        GlobalObject.__sidebarDesignObj__['design_updatetime'] = updatetime
    except Exception as e:
        debug(e.__str__())


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def listFlowActiveAjax(request):
    '''
    list deployed custom flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['flow_name__icontains','description__icontains']
    query = ''
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    app_name = postdata.get('app_name','')
    if datatable:
        deploytime = postdata.get('deploytime','')
        is_active = postdata.get('is_active',['1','0'])
        undeploy_flag = postdata.get('undeploy_flag', ['0'])
        query = FlowActive.objects.filter(flow_app_id__app_name=app_name,undeploy_flag__in=undeploy_flag,parent_uuid=None,deploytime__lte=deploytime,is_active__in=is_active).values('id','flow_uuid','flow_name','deploytime','version','is_active','description','flowlog','api','undeploy_flag')
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list FlowActive success.' % request.user.username)
        return JsonResponse(result)
    else:
        display_field = ['id','flow_uuid','flow_name']
        if app_name:
            result = list(FlowActive.objects.filterformat(*display_field,flow_app_id__app_name=app_name,undeploy_flag=False,parent_uuid=None))
        else:
            result = []
        info(request ,'%s list FlowActive success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def updateFlowActiveAjax(request):
    '''
    update deployed custom flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['field','app_name','flow_name']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    app_name = postdata.get('app_name','')
    flow_name = postdata.get('flow_name','')
    action_field = postdata.get('field','')
    if checker.get('status') == 'success':
        try:
            flowactive = FlowActiveGlobalObject.NameSearch(flow_name, None, app_name)
            if action_field == 'is_active':
                if flowactive.is_active:
                    flowactive.is_active = False
                else:
                    flowactive.is_active = True
            elif action_field == 'api':
                if flowactive.api:
                    flowactive.api = False
                else:
                    flowactive.api = True
            elif action_field == 'flowlog':
                if flowactive.flowlog:
                    flowactive.flowlog = False
                else:
                    flowactive.flowlog = True
            elif action_field == 'display_field':
                display_field = postdata.get('display_field','')
                flowactive.display_field = display_field
            flowactive.save()
            info(request ,'%s update FlowActive success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('設定成功。')).returnJSON()
        except Exception as e:
            error(request,e)
            return ResponseAjax(statusEnum.not_found, _('找不到該流程。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def activeFlowActiveAjax(request):
    '''
    active or inactive deployed custom flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['id','active']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id_list = postdata.get('id','')
    active = postdata.get('active','active')
    if checker.get('status') == 'success':
        if active == 'active':
            is_active = True
        else:
            is_active = False
        FlowActive.objects.filter(id__in=flow_id_list).update(is_active=is_active)
        fa_list = FlowActive.objects.filter(id__in=flow_id_list)
        for fa in fa_list:
            flow_uuid = fa.flow_uuid.hex
            FlowActiveGlobalObject.deleteFlowActive(flow_uuid, None)
            FlowActiveGlobalObject.setFlowActive(fa)
        info(request ,'%s active FlowActive success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('設定成功。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def getFlowAPIFormatAjax(request):
    '''
    list flowactive form point chart_id.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_name','app_name']
    result = {}
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_name = postdata.get('flow_name','')
    app_name = postdata.get('app_name','')
    action = postdata.get('action','')
    if checker.get('status') == 'success':
        fa = FlowActiveGlobalObject.NameSearch(flow_name, None, app_name)
        if fa:
            formdata = []
            items = json.loads(fa.merge_formobject)
            for key in items:
                field_dict = {}
                item = items[key]
                if item['type'] == 'checkbox':
                    field_dict = {'id':item['id'], 'value':'[<' + item['config']['title'] + '>,...]', 'type':item['type']}
                elif item['type'] == 'h_status':
                    field_dict = {'id':item['id'], 'value':'<' + item['config']['title'] + '>', 'type':item['type']}
                    header_dict = {'id':'status', 'value':'<' + item['config']['title'] + '>', 'type':'header'}
                    formdata.append(header_dict)
                elif item['type'] == 'h_group':
                    field_dict = {'id':item['id'], 'value':{'group':'<'+item['config']['group_title']+'>','user':'<'+item['config']['user_title']+'>'}, 'type':item['type']}
                    header_dict = {'id':'group', 'value':{'group':'<'+item['config']['group_title']+'>','user':'<'+item['config']['user_title']+'>'}, 'type':'header'}
                    formdata.append(header_dict)
                elif item['type'] == 'h_title':
                    field_dict = {'id':item['id'], 'value':'<' + item['config']['title'] + '>', 'type':item['type']}
                    header_dict = {'id':'title', 'value':'<' + item['config']['title'] + '>', 'type':'header'}
                    formdata.append(header_dict)
                elif item['type'] == 'h_level':
                    field_dict = {'id':item['id'], 'value':'<' + item['config']['title'] + '>', 'type':item['type']}
                    header_dict = {'id':'level', 'value':'<' + item['config']['title'] + '>', 'type':'header'}
                    formdata.append(header_dict)
                else:
                    field_dict = {'id':item['id'], 'value':'<' + item['config']['title'] + '>', 'type':item['type']}
                formdata.append(field_dict)
            result['security'] = '<security>'
            result['app_name'] = app_name
            result['flow_name'] = flow_name
            result['action'] = action
            result['omflow_restapi'] = True
            if formdata:
                result['formdata'] = formdata
            if action == 'update':
                result['data_id'] = '<data_id>'
            elif action == 'create':
                if not formdata:
                    #如果沒有表單
                    start_input = {}
                    items = json.loads(fa.flowobject)['items']
                    for item in items:
                        if item['id'] == 'FITEM_1':
                            break
                    input_list = item['config']['input']
                    for input_dict in input_list:
                        name = input_dict['name']
                        value = input_dict['value']
                        start_input[name] = value
                    result['start_input'] = start_input
            info(request ,'%s list flow form point success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
        else:
            info(request ,'%s list flow form point error.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('讀取失敗。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def scheduleFlowActiveAjax(request):
    '''
    schedule deployed custom flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['action']
    status = True
    message = ''
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    schedule_id_list = postdata.get('schedule_id','')
    schedule_action = postdata.get('action','')
    if checker.get('status') == 'success':
        #update or create or delete schedule
        if schedule_action in ['delete','update']:
            d_s = deleteSchedule(schedule_id_list)
            if not d_s['status']:
                status = False
                message += d_s['message']
        if schedule_action in ['update','create']:
            module_name = 'omformflow.views'
            method_name = 'createOmData'
            c_s = createSchedule(postdata, module_name, method_name)
            if not c_s['status']:
                status = False
                message += c_s['message']
        if status:
            info(request ,'%s schedule FlowActive success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('設定成功。')).returnJSON()
        else:
            info(request ,'%s schedule FlowActive error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, message).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    

def deleteSchedule(schedule_id_list):
    '''
    delete schedule.
    input: schedule_id[]
    return: json
    author: Kolin Hsu
    '''
    try:
        #function variable
        result = {}
        if schedule_id_list:
            #delete schedule
            scheduler_list = Scheduler.objects.filter(id__in=schedule_id_list)
            if len(scheduler_list):
                scheduler_id_list = scheduler_list.values_list('id',flat=True)
                cancelScheduleJob(scheduler_id_list)
                scheduler_list.delete()
            result['status'] = True
        else:
            result['status'] = False
            result['message'] = _('缺少schedule_id。\n')
        return result
    except Exception as e:
        debug(e.__str__())
        return {}


def createSchedule(postdata, module_name, method_name):
    '''
    delete schedule.
    input: schedule_id[]
    return: json
    author: Kolin Hsu
    '''
    try:
        #function variable
        result = {}
        input_param = {}
        #get post data
        flow_id = postdata.get('flow_id',None)
        flow_uuid = postdata.get('flow_uuid','')
        exec_time = postdata.get('exec_time','')
        every = postdata.get('every','')
        cycle = postdata.get('cycle','')
        if postdata.__class__.__name__ == 'dict':
            cycle_date = postdata.get('cycle_date',[])
        else:
            cycle_date = postdata.get('cycle_date',[])
        formdata = postdata.get('formdata','')
        if flow_id and flow_uuid:
            exec_fun = {'module_name':'omflow.syscom.schedule_monitor','method_name':'put_flow_job'}
            input_param['module_name'] = module_name
            input_param['method_name'] = method_name
            input_param['flow_uuid'] = flow_uuid
            if formdata:
                input_param['formdata'] = formdata
            else:
                start_input = postdata.get('start_input','{}')
                input_param['start_input'] = start_input
            exec_fun_dict = json.dumps(exec_fun)
            input_param_dict = json.dumps(input_param)
            if cycle == "Monthly" or cycle == "Weekly":
                if cycle_date:
                    scheduler = Scheduler.objects.create(exec_time=exec_time,every=every,cycle=cycle,cycle_date=cycle_date,exec_fun=exec_fun_dict,input_param=input_param_dict,flowactive_id=flow_id)
                    schedule_Execute(scheduler)
                    result['status'] = True
                else:
                    result['status'] = False
                    result['message'] = _('請選擇日期或星期。\n')
            else:
                scheduler = Scheduler.objects.create(exec_time=exec_time,every=every,cycle=cycle,cycle_date=cycle_date,exec_fun=exec_fun_dict,input_param=input_param_dict,flowactive_id=flow_id)
                schedule_Execute(scheduler)
                result['status'] = True
        else:
            result['status'] = False
            result['message'] = _('請選擇流程。\n')
        return result
    except Exception as e:
        debug(e.__str__())
        return {}
    

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def activeScheduleAjax(request):
    '''
    active or inactive schedule.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['schedule_id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    schedule_id = postdata.get('schedule_id','')
    scheduler_id_list = []
    scheduler_id_list.append(schedule_id)
    if checker.get('status') == 'success':
        try:
            scheduler = Scheduler.objects.get(id=schedule_id)
            if scheduler.is_active:
                is_active = False
                cancelScheduleJob(scheduler_id_list)
            else:
                is_active = True
                schedule_Execute(scheduler)
            scheduler.is_active = is_active
            scheduler.save()
            info(request ,'%s active Schedule success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('設定成功。')).returnJSON()
        except:
            info(request ,'%s active Schedule error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, _('找不到該排程。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()

    
@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def listSchedulerAjax(request):
    '''
    list scheduler.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['flowactive_id__flow_name__icontains']
    #get post data
    postdata = getPostdata(request)
    is_active = postdata.get('is_active',['1','0'])
    display_field = ['id','create_time','every','cycle','cycle_date','is_active','next_exec_time','last_exec_time','flowactive_id','flowactive_id__flow_name','flowactive_id__flow_uuid','input_param','exec_time']
    query = Scheduler.objects.filter(is_active__in=is_active).exclude(flowactive_id=None).values(*display_field)
    result = DatatableBuilder(request, query, field_list)
    datas = result['data']
    if isinstance(datas, str):
        pass
    elif isinstance(datas, list):
        for record in datas:
            #計算下次執行時間與上次執行時間
            next_exec_time = record['next_exec_time']
            last_exec_time = record['last_exec_time']
            if last_exec_time == None or last_exec_time == '':
                pass
            else:
                last_exec_time = json.loads(last_exec_time)
                record['last_exec_time'] = max(list(last_exec_time.values()))
            if next_exec_time == None or next_exec_time == '':
                pass
            else:
                next_exec_time = json.loads(next_exec_time)
                record['next_exec_time'] = min(list(next_exec_time.values()))
            #取得formdata
            formdata = json.loads(record['input_param']).get('formdata','')
            start_input = json.loads(record['input_param']).get('start_input','')
            if formdata:
                record['input_param'] = formdata
            else:
                record['input_param'] = start_input
    elif isinstance(datas, dict):
        for key in datas:
            next_exec_time = datas[key]['next_exec_time']
            last_exec_time = datas[key]['last_exec_time']
            if last_exec_time == None or last_exec_time == '':
                pass
            else:
                last_exec_time = json.loads(last_exec_time)
                datas[key]['last_exec_time'] = max(list(last_exec_time.values()))
            if next_exec_time == None or next_exec_time == '':
                pass
            else:
                next_exec_time = json.loads(next_exec_time)
                datas[key]['next_exec_time'] = min(list(next_exec_time.values()))
            formdata = json.loads(datas[key]['input_param']).get('formdata','')
            start_input = json.loads(datas[key]['input_param']).get('start_input','')
            if formdata:
                datas[key]['input_param'] = formdata
            else:
                datas[key]['input_param'] = start_input
    info(request ,'%s list Schedule success.' % request.user.username)
    return JsonResponse(result)


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def undeployActiveApplicationAjax(request):
    '''
    undeploy app.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    app_id = postdata.get('app_id','')
    app_name = postdata.get('app_name','')
    if app_name:
        app_id = ActiveApplication.objects.get(app_name=app_name,undeploy_flag=False).id
    if app_id:
        uaa_result = undeployActiveApplication(app_id, request.user)
        #移除側欄
        if uaa_result['app_attr'] in ['sys','user','cloud']:
            removeSidebar(app_id)
        #移除schedule
        flow_id_list = uaa_result['flow_id_list']
        schedule_id_list = list(Scheduler.objects.filter(flowactive_id__in=flow_id_list).values_list('id',flat=True))
        if schedule_id_list:
            deleteSchedule(schedule_id_list)
        info(request ,'%s undeploy ActiveApplication success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('下線成功。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, _('請提供必要參數：app_id或是app_name。')).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def redeployActiveApplicationAjax(request):
    '''
    redeploy active application.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['new_app_id','lside_pid']
    status = True
    #get post data
    postdata = getPostdata(request)
    lside_pid = postdata.get('lside_pid','')
    new_app_id = postdata.get('new_app_id','')
    ex_app_id = postdata.get('ex_app_id','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    #check license
    if ex_app_id:
        omlicense = checkLicense('app',True)
    else:
        omlicense = checkLicense('app')
    if omlicense:
        if checker.get('status') == 'success':
            try:
                if ex_app_id:
                    ex_aa = ActiveApplication.objects.get(id=ex_app_id)
                    if not ex_aa.undeploy_flag:
                        #下架現有流程
                        uaa_result = undeployActiveApplication(ex_app_id, request.user)
                        if uaa_result['app_attr'] in ['sys','user','cloud']:
                            #移除側邊選單
                            removeSidebar(ex_app_id)
                    else:
                        status = False
                if status:
                    #重新上架應用
                    aa = ActiveApplication.objects.get(id=new_app_id)
                    app_attr = aa.app_attr
                    aa.undeploy_flag = False
                    aa.save()
                    FlowActiveGlobalObject.setAppNameDict(aa.app_name, aa.id)
                    #重新上架流程
                    flow_list = list(FlowActive.objects.filterformat('id','flow_uuid','flow_name',flow_app_id=aa.id))
                    for fa in flow_list:
                        flow_id = fa['id']
                        redeployFlow(flow_id)
                    #重新建立側邊選單
                    if app_attr in ['user','cloud','sys']:
                        createSidebar(flow_list, aa.id, aa.app_name, lside_pid)
                    info(request ,'%s redeploy ActiveApplication success.' % request.user.username)
                    return ResponseAjax(statusEnum.success, _('重新上架成功。')).returnJSON()
                else:
                    info(request ,'%s redeploy ActiveApplication error.' % request.user.username)
                    return ResponseAjax(statusEnum.not_found, _('重新上架失敗。')).returnJSON()
            except Exception as e:
                error(request,e)
                return ResponseAjax(statusEnum.not_found, _('找不到該應用流程。')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s the license error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, _('應用流程數量已達上限。')).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def listActiveApplicationAjax(request):
    '''
    list active application
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    if datatable:
        #function variable
        field_list=['app_name__icontains','user_id__username__icontains']
        query = ''
        #get post data
        postdata = getPostdata(request)
        app_attr = postdata.get('app_attr',['user','cloud','lib','sys'])
        updatetime = postdata.get('updatetime','')
        undeploy_flag = postdata.get('undeploy_flag',['0'])
        display_field =['id','app_name','app_attr','updatetime','version','user_id__username','undeploy_flag']
        query = ActiveApplication.objects.filterformat(*display_field,app_attr__in=app_attr,updatetime__lte=updatetime,undeploy_flag__in=undeploy_flag)
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list ActiveApplication success.' % request.user.username)
        return JsonResponse(result)
    else:
        schedule = postdata.get('schedule',None)
        if schedule:
            app = list(ActiveApplication.objects.filterformat('id','app_name',undeploy_flag=False))
            flow = list(FlowActive.objects.filterformat('id','flow_uuid','flow_name','flow_app_id',undeploy_flag=False,parent_uuid=None))
            result = {'app':app,'flow':flow}
        else:
            app_id = postdata.get('app_id',None)
            if app_id:
                result = list(ActiveApplication.objects.filter(undeploy_flag=False).exclude(id=app_id).values('id','app_name'))
            else:
                result = list(ActiveApplication.objects.filter(undeploy_flag=False).values('id','app_name'))
        info(request ,'%s list ActiveApplication success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()

@login_required
@try_except
def listActiveApplication4RelationAjax(request):
    '''
    list active application
    input: request
    return: json
    author: Kolin Hsu
    '''
    flow_uuid_list = []
    app_id_list = []
    this_activeList = list(FlowActive.objects.filter(undeploy_flag=0,parent_uuid__isnull=True).values_list('flow_uuid', flat=True))
    this_activeList = [o.hex for o in this_activeList]
    #print(this_activeList)
    if request.user.is_superuser:
        p = list(Permission.objects.filter(codename__contains="_View").values())
    else: 
        p = list(Permission.objects.filter(group__in=request.user.groups.all(),codename__contains="_View").values())
    for i in p:
        this_model = list(filter(lambda x: x.__name__==re.findall("^(Om.+)_View", i.get("codename"))[0],apps.get_models()))
        if len(this_model):
            this_name = this_model[0].__name__
            this_flow_uuid = re.findall("^Omdata_(.+)", this_name)
            if len(this_flow_uuid) :
                flow_uuid_list.append(this_flow_uuid[0])
    flow = list(FlowActive.objects.filterformat('id','flow_uuid','flow_name','flow_app_id',flow_uuid__in=flow_uuid_list,undeploy_flag=False,parent_uuid=None))
    for f in flow:
        app_id_list.append(f['flow_app_id'])
    app = list(ActiveApplication.objects.filter(id__in=app_id_list,undeploy_flag=False).values('id','app_name'))
    result = {'app':app,'flow':flow}
    info(request ,'%s list ActiveApplication success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


@login_required
@try_except
def getCloudFlowAjax(request):
    try:
        postdata = getPostdata(request)
        content = postdata.get('content', '')
        result = getRepository(content)
        if result != None:
            return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()
        else:
            return ResponseAjax(statusEnum.error, _('查詢失敗。'), result).returnJSON()
    except:
        return ResponseAjax(statusEnum.error, _('查詢失敗。')).returnJSON()
        
    
    
def undeployFlow(flow_id_list):
    '''
    undeploy custom flow.
    input: flow_id
    return: json
    author: Kolin Hsu
    '''
    #function variable
    result = {}
    status = True
    message = ''
    try:
        for flow_id in flow_id_list:
            #undeploy main flow
            undeploy_time = datetime.now()
            #remove global
            main_flow = FlowActiveGlobalObject.deleteFlowActive(None, flow_id)
            flow_uuid = main_flow.flow_uuid.hex
            main_flow.undeploy_flag = True
            main_flow.undeploy_time = undeploy_time
            main_flow.save()
            #undeploy subflow
            subflow_uuid_list = list(FlowActive.objects.filter(parent_uuid=flow_uuid,undeploy_flag=False).values_list('flow_uuid',flat=True))
            #remove global
            for subflow_uuid in subflow_uuid_list:
                FlowActiveGlobalObject.deleteFlowActive(subflow_uuid.hex, None)
            FlowActive.objects.filter(parent_uuid=flow_uuid,undeploy_flag=False).update(undeploy_flag=True,undeploy_time=undeploy_time)
            #remove python file
            removePythonFile(flow_uuid)
            #remove subflow python file
            all_subflow_uuid_list = []
            for subflow_uuid in subflow_uuid_list:
                subflow_uuid = subflow_uuid.hex
                removePythonFile(subflow_uuid)
                all_subflow_uuid_list.append(subflow_uuid)
            #remove chart compile object
            all_subflow_uuid_list.append(flow_uuid)
            removeChartCompileObject(all_subflow_uuid_list)
    except Exception as e:
        debug(e.__str__())
        status = False
        message = e.__str__()
    finally:
        result['status'] = status
        result['message'] = message
        return result
    

def redeployFlow(flow_id):
    '''
    undeploy custom flow.
    input: flow_id
    return: json
    author: Kolin Hsu
    '''
    #function variable
    result = {}
    status = True
    message = ''
    subflow_mapping_dict = {}
    try:
        #redeploy main flow
        main_flow = FlowActive.objects.get(id=flow_id,undeploy_flag=True)
        flow_uuid = main_flow.flow_uuid.hex
        version = main_flow.version
        main_flow.undeploy_flag = False
        main_flow.undeploy_time = None
        main_flow.save()
        #set flowactive global
        FlowActiveGlobalObject.setFlowActive(main_flow)
        #redeploy subflow
        subflow_list = list(FlowActive.objects.filterformat('flow_uuid','flowobject',parent_uuid=flow_uuid,version=version))
        if len(subflow_list):
            FlowActive.objects.filter(parent_uuid=flow_uuid,version=version).update(undeploy_flag=False,undeploy_time=None)
            #set flowactive global
            sub_fa_list = FlowActive.objects.filter(parent_uuid=flow_uuid,version=version)
            for sub_fa in sub_fa_list:
                FlowActiveGlobalObject.setFlowActive(sub_fa)
            #create subflow_mapping_dict
            for sb_d in subflow_list:
                s_uid = str(json.loads(sb_d['flowobject'])['uid'])
                subflow_mapping_dict[s_uid] = sb_d['flow_uuid']
            #create subflow main.py
            for sb_d in subflow_list:
                sb_flow_uuid = sb_d['flow_uuid']
                s_flowobject = sb_d['flowobject']
                flowMaker(sb_flow_uuid,s_flowobject,version,subflow_mapping_dict)
        #create mainflow main.py
        flowMaker(flow_uuid,main_flow.flowobject,version,subflow_mapping_dict)
    except Exception as e:
        status = False
        message = e.__str__()
        debug(message)
    finally:
        result['status'] = status
        result['message'] = message
        return result


def removeSidebar(app_id):
    '''
    remove side bar.
    input: flow_uuid
    return: boolean
    author: Kolin Hsu
    '''
    try:
        #function variable
        sidebar_design_new = []
        last_folder_id = ''
        app_parent_id = ''
        #remove left side bar
        sidebar_design = GlobalObject.__sidebarDesignObj__['sidebar_design']
        for item in sidebar_design:
            if item['p_id'] == 'app-'+str(app_id):
                pass
            elif item['id'] == 'app-'+str(app_id):
                app_parent_id = last_folder_id
                pass
            else:
                sidebar_design_new.append(item)
            if 'custom_' in item['id']:
                last_folder_id = item['id']
        #update database
        sidebar_design_str = json.dumps(sidebar_design_new)
        systemsetting = SystemSetting.objects.get(name='sidebar_design')
        systemsetting.value = sidebar_design_str
        systemsetting.save()
        #update global object
        updatetime = datetime.now()
        GlobalObject.__sidebarDesignObj__['sidebar_design'] = sidebar_design_new
        GlobalObject.__sidebarDesignObj__['design_updatetime'] = updatetime
        return app_parent_id
    except Exception as e:
        debug(e.__str__())
        return False


def removePythonFile(flow_uuid):
    '''
    remove python file.
    input: flow_uuid,version
    return: boolean
    author: Kolin Hsu
    '''
    try:
        path = os.path.join(settings.BASE_DIR, "omformflow", "production", flow_uuid)
        shutil.rmtree(path)
        return True
    except:
        return False


def removeChartCompileObject(all_uuid_list):
    '''
    remove chart compile object.
    input: flow_uuid,version
    return: boolean
    author: Kolin Hsu
    '''
    try:
        keys = list(GlobalObject.__chartCompileObj__.keys())
        for key in keys:
            for ex_uuid in all_uuid_list:
                if ex_uuid in key:
                    GlobalObject.__chartCompileObj__.pop(key)
        return True
    except Exception as e:
        debug(e.__str__())
        return False


#前端用途：開單、設定schedule
@login_required
@try_except
def loadFormDesignAjax(request):
    '''
    load form design for deploy flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_uuid']
    result = {}
    formobject = None
    use_form = True
    #get post data
    postdata = getPostdata(request)
    flow_uuid = postdata.get('flow_uuid','')
    if request.user.has_perm('omformmodel.Omdata_' + flow_uuid + '_View') or request.user.has_perm('omformflow.OmFormFlow_Manage'):
        #server side rule check
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            try:
                fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                flowobject = json.loads(fa.flowobject)
                formobject = fa.formobject
                formobject_dict = json.loads(formobject)
                if len(formobject_dict['items']) == 0:
                    items = flowobject['items']
                    for i in items:
                        if i['type'] == 'start':
                            result['start_input'] = i['config']['input']
                            use_form = False
                            break
                else:
                    result['start_input'] = []
                result['flow_name'] = fa.flow_name
                result['formobject'] = formobject
                result['attachment'] = fa.attachment
                result['use_form'] = use_form
                info(request ,'%s load form design success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
            except Exception as e:
                debug(e.__str__())
                info(request ,'%s load form design error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, _('找不到該流程。')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


#前端用途：各表單頁面的標頭
@login_required
@try_except
def getApplicationFlowNameAjax(request):
    '''
    get app name or flow name.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    a_flow_uuid = postdata.get('a_flow_uuid','')
    w_flow_id = postdata.get('w_flow_id','')
    a_app_id = postdata.get('a_app_id','')
    w_app_id = postdata.get('w_app_id','')
    if a_flow_uuid:
        fa = FlowActiveGlobalObject.UUIDSearch(a_flow_uuid)
        aa = ActiveApplication.objects.get(id=fa.flow_app_id)
        result = {'flow_name':fa.flow_name,'app_name':aa.app_name}
    elif w_flow_id:
        fw = FlowWorkspace.objects.get(id=w_flow_id)
        wa = WorkspaceApplication.objects.get(id=fw.flow_app_id)
        result = {'flow_name':fw.flow_name,'app_name':wa.app_name}
    elif a_app_id:
        result = ActiveApplication.objects.get(id=a_app_id).app_name
    elif w_app_id:
        result = WorkspaceApplication.objects.get(id=w_app_id).app_name
    info(request ,'%s get app name or flow name success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def exportActiveApplicationAjax(request):
    '''
    export custom form flow design.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['app_id_list']
    result = []
    #get post data
    postdata = getPostdata(request)
    app_id_list = postdata.get('app_id_list','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        try:
            for app_id in app_id_list:
                app_dict = {}
                flow_list = []
                aa = ActiveApplication.objects.get(id=app_id)
                fa_list = list(FlowActive.objects.filter(flow_app_id=app_id,parent_uuid=None).values())
                for flowactive in fa_list:
                    flow = {}
                    config = {}
                    subflow = []
                    flowactive_subflow_list = list(FlowActive.objects.filterformat(parent_uuid=flowactive['flow_uuid'],undeploy_flag=False))
                    if len(flowactive_subflow_list):
                        for flowactive_subflow in flowactive_subflow_list:
                            sub_obj = {}
                            sub_obj['uid'] = json.loads(flowactive_subflow['flowobject'])['uid']
                            sub_obj['name'] = flowactive_subflow['flow_name']
                            sub_obj['description'] = flowactive_subflow['description']
                            subflow.append(sub_obj)
                    config['name'] = flowactive['flow_name']
                    config['description'] = flowactive['description']
                    config['fp_show'] = flowactive['fp_show']
                    config['attachment'] = flowactive['attachment']
                    config['relation'] = flowactive['relation']
                    config['worklog'] = flowactive['worklog']
                    config['history'] = flowactive['history']
                    config['mission'] = flowactive['mission']
                    config['flowlog'] = flowactive['flowlog']
                    config['api'] = flowactive['api']
                    config['subflow'] = subflow
                    config['permission'] = json.loads(flowactive['permission'])
                    flow['flow_name'] = flowactive['flow_name']
                    flow['description'] = flowactive['description']
                    flow['flowobject'] = json.loads(flowactive['flowobject'])
                    flow['config'] = config
                    flow_list.append(flow)
                app_dict['app_name'] = aa.app_name
                app_dict['app_attr'] = aa.app_attr
                app_dict['flow_list'] = flow_list
                result.append(app_dict)
            info(request ,'%s export ActiveApplication success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('匯出成功。'), result).returnJSON()
        except Exception as e:
            debug(request,e.__str__())
            info(request ,'%s export ActiveApplication error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, _('匯出失敗。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


#開單、推單、刪單
@login_required
@try_except
def editOmDataAjax(request):
    '''
    create/update/delete ticket.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['action']
    per = True
    #get post data
    postdata = getPostdata(request)
    action = postdata.get('action','')
    files = request.FILES.getlist('files','')
    app_name = postdata.get('app_name','')
    flow_name = postdata.get('flow_name','')
    flow_uuid = postdata.get('flow_uuid','')
    if app_name and flow_name:
        fa = FlowActiveGlobalObject.NameSearch(flow_name, None, app_name)
        flow_uuid = fa.flow_uuid.hex
        postdata['flow_uuid'] = flow_uuid
    #server side rule check
    omflow_restapi = postdata.get('omflow_restapi',False)
    api_pass = True
    if omflow_restapi:
        fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
        if not fa.api:
            api_pass = False
    checker = DataChecker(postdata, require_field)
    if api_pass:
        if checker.get('status') == 'success':
            if action == 'update':
                if checkOmDataPermission(request.user, postdata.get('flow_uuid',''), None, postdata.get('data_id',''), '_Modify'):
                    result = updateOmData(postdata, request.user.username)
                else:
                    per = False
            elif action == 'delete':
                if request.user.has_perm('omformmodelOmdata_' + flow_uuid + '_Delete'):
                    result = deleteOmData(postdata)
                else:
                    per = False
            elif action == 'create':
                if request.user.has_perm('omformmodel.Omdata_' + flow_uuid + '_Add'):
                    result = createOmData(postdata, request.user.username, files)
                else:
                    per = False
            else:
                result = {'status':False, 'message':_('請提供正確的動作，新增、編輯或刪除。')}
            if per:
                if result['status']:
                    data_no = result.get('data_no','')
                    info(request ,'%s edit OmData success.' % request.user.username)
                    return ResponseAjax(statusEnum.success, result['message'], data_no).returnJSON()
                else:
                    info(request ,'%s edit OmData error.' % request.user.username)
                    return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
            else:
                info(request ,'%s has no permission.' % request.user.username)
                return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s edit omdata by rest api fail, because this flow did not active the api flag.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, _('該流程未啟用API呼叫。')).returnJSON()
    

def checkOmDataPermission(user, flow_uuid, data_no, data_id, per_type):
    '''
    檢查使用者是否有編輯權限，或是該使用者為該單的受派人，或是開單人
    '''
    try:
        result = False
        assign_per = False
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        user_groups = list(user.groups.all().values_list('id',flat=True))
        if data_id:
            omdata = omdata_model.objects.get(id=data_id)
            create_user_id = omdata.create_user_id
            group = omdata.group
            if group:
                group = json.loads(group)
                u = group.get('user','')
                g = str(group.get('group',''))
                if re.match(r'[0-9]+', g):
                    g = int(g)
                if u == str(user.id):
                    assign_per = True
                elif g in user_groups and not group['user']:
                    assign_per = True
            if per_type == '_View' and not assign_per:
                if create_user_id == user.username:
                    assign_per = True
        elif data_no:
            omdata = list(omdata_model.objects.filter(data_no=data_no).values('group','create_user_id'))
            for omdata_row in omdata:
                create_user_id = omdata_row['create_user_id']
                group = omdata_row['group']
                if create_user_id == user.username:
                    assign_per = True
                    break
                elif group:
                    group = json.loads(group)
                    u = group.get('user','')
                    g = str(group.get('group',''))
                    if re.match(r'[0-9]+', g):
                        g = int(g)
                    if u == str(user.id):
                        assign_per = True
                        break
                    elif g in user_groups and not group['user']:
                        assign_per = True
                        break
        if user.has_perm('omformmodel.Omdata_' + flow_uuid + per_type) or assign_per:
            result = True
    except Exception as e:
        debug(e.__str__())
    finally:
        return result


def createOmData(param,user='system',files=None):
    '''
    create ticket.
    input: param,user
    return: json
    author: Kolin Hsu
    '''
    #function variable
    result = {}
    formdata = {}
    form_pass = True
    message = ''
    status = False
    data_no = None
    #get postdata
    flow_uuid = param.get('flow_uuid','')
    outflow_content = json.loads(param.get('outflow_content','{}'))
    start_input = param.get('start_input',{})
    if isinstance(start_input, str):
        start_input = json.loads(start_input)
    formdata_list = param.get('formdata',[])
    if isinstance(formdata_list, str):
        formdata_list = json.loads(formdata_list)
    if formdata_list:
        formdata = FormatFormdataListToFormdata(formdata_list)
    fillupFormdata(formdata, flow_uuid)
    #get flowactive object
    try:
        flowactive = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
        #check this flow is active
        if flowactive.is_active:
            #get form design object
            formobject = json.loads(flowactive.formobject)
            if formdata:
                #check the required field have value in postdata
                item_list = formobject.get('items',[])
                form_require_check = FormDataChecker(formdata_list, item_list)
                if not form_require_check:
                    form_pass = False
                    message = _('缺少必填欄位。')
            if form_pass:
                #save files to temp db
                if files:
                    unixtime = int(time.mktime(datetime.now().timetuple()))
                    mapping_id = flow_uuid + '_' + str(unixtime)
                    TempFiles.objects.bulk_create([TempFiles(file=file,size=file.size,file_name=file.name,mapping_id=mapping_id) for file in files])
                #om engine
                data = {}
                data['flow_uuid'] = flow_uuid
                data['chart_id_to'] = 'FITEM_1'
                data['chart_id_from'] = None
                data['data_no'] = None
                data['data_id'] = None
                data['table_uuid'] = flow_uuid
                data['flowlog'] = flowactive.flowlog
                data['start_input'] = start_input
                data['error'] = False
                if files:
                    data['mapping_id'] = mapping_id
                #set formdata
                formdata['create_user_id'] = user
                formdata['update_user_id'] = user
                formdata['flow_uuid'] = flow_uuid
                formdata['running'] = True
                data['formdata'] = formdata
                data['flow_value'] = {}
                if outflow_content:
                    data['outflow_content'] = outflow_content
                omengine_result = OmEngine(flow_uuid, data).checkActive()
                if omengine_result:
                    if isinstance(omengine_result, str):
                        message = _('開單失敗：') + omengine_result
                    elif isinstance(omengine_result, dict):
                        status = True
                        data_no = omengine_result['data_no']
                        message = _('開單成功。')
                else:
                    message = _('開單成功。')
                    status = True
        else:
            message = _('該流程目前為停用狀態。')
    except ObjectDoesNotExist:
        message = _('該流程沒有已上架的版本')
    except Exception as e:
        message = e.__str__()
    finally:
        result['message'] = message
        result['status'] = status
        result['data_no'] = data_no
        return result


def fillupFormdata(formdata, flow_uuid):
    try:
        fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
        items = json.loads(fa.merge_formobject)
        for key in items:
            item = items[key]
            item_id = item['id'].lower()
            if formdata.get(item_id,None) == None:
                default_value = item['config'].get('value','')
                if item['type'] == 'checkbox':
                    if default_value:
                        value = default_value.split(',')
                    else:
                        value = []
                    value = json.dumps(value)
                elif item['type'] == 'h_group':
                    if default_value:
                        value_list = default_value.split(',')
                        if len(value_list) == 1:
                            group = str(value_list[0])
                            user = ""
                        else:
                            group = str(value_list[0])
                            user = str(value_list[1])
                        value = {"group": group, "user":user}
                    else:
                        value = {"group": "", "user":""}
                    value = json.dumps(value)
                else:
                    value = default_value
                formdata[item_id] = value
    except Exception as e:
        error('',e.__str__())

 
def updateOmData(param,user='system'):
    '''
    update ticket.
    input: param,user
    return: json
    author: Kolin Hsu
    '''
    #function variable
    result = {}
    message = ''
    status = False
    data_no = None
    formdata = {}
    #get postdata
    data_id = param.get('data_id','')
    flow_uuid = param.get('flow_uuid','')
    formdata_list = param.get('formdata',[])
    quick_action = param.get('quick_action','')
    #get omdata object
    try:
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        if omdata_model:
            omdata = omdata_model.objects.get(id=data_id,history=False,closed=False)
            omdata_dict = omdata.__dict__.copy()
            #check this ticket's status is not running
            if not omdata.running:
                #get flowactive object
                try:
                    stop_list = omdata.stop_uuid.split('-')
                    stop_uuid = stop_list[-1]
                    stop_level = len(stop_list)
                    if stop_level == 1:
                        flowactive = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                        create_or_set_mission = flowactive.mission
                        is_active = flowactive.is_active
                    else:
                        data_param = json.loads(omdata.data_param)
                        subflow_uuid = data_param.get('flow_uuid','')
                        flowactive = FlowActiveGlobalObject.UUIDSearch(subflow_uuid)
                        parent_flowactive = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                        create_or_set_mission = parent_flowactive.mission
                        is_active = parent_flowactive.is_active
                    flowobject = json.loads(flowactive.flowobject)
                    flowobject_items = flowobject['items']
                    #check this flow is active
                    if is_active:
                        is_form = False
                        for fitem in flowobject_items:
                            if fitem['id'] == stop_uuid:
                                if fitem['type'] == 'form':
                                    is_form = True
                                    if not fitem['config']['form_object']:
                                        if stop_level == 1:
                                            formobject = json.loads(flowactive.formobject)
                                        else:
                                            formobject = json.loads(parent_flowactive.formobject)
                                    else:
                                        if isinstance(fitem['config']['form_object'], dict):
                                            formobject = fitem['config']['form_object']
                                        elif isinstance(fitem['config']['form_object'], str):
                                            formobject = json.loads(fitem['config']['form_object'])
                                break
                        if is_form:
                            #把快速操作的輸入組合成formdata_list格式
                            if quick_action:
                                formdata_list = doQuickAction(flowactive, quick_action, stop_uuid, omdata_dict)
                            #組合formdata
                            if formdata_list:
                                formdata = FormatFormdataListToFormdata(formdata_list)
                            #check the required field have value in postdata
                            item_list = formobject.get('items',[])
                            if quick_action:
                                form_require_check = True
                            else:
                                form_require_check = FormDataChecker(formdata_list, item_list)
                            if form_require_check:
                                #整理formdata
                                formdata['stoptime'] = None
                                formdata['stop_uuid'] = None
                                formdata['stop_chart_text'] = None
                                formdata['error'] = False
                                formdata['error_message'] = None
                                formdata['running'] = True
                                formdata['update_user_id'] = user
                                formdata['updatetime'] = datetime.now()
                                #update omdata
                                omdata_model.objects.filter(id=data_id).update(**formdata)
                                #檢查sla
                                checkSLARule(flow_uuid, data_id)
                                if create_or_set_mission:
                                    #set mission history
                                    setMission('history', flow_uuid, None, data_id, user)
                                #om engine
                                data = json.loads(omdata_dict['data_param'])
                                data['data_id'] = data_id
                                data['chart_id_from'] = None
                                data['error'] = False
                                if stop_level == 1:
                                    omengine_result = OmEngine(flow_uuid, data).checkActive()
                                else:
                                    omengine_result = OmEngine(subflow_uuid, data).checkActive()
                                if omengine_result:
                                    if isinstance(omengine_result, str):
                                        message = _('開單失敗：') + omengine_result
                                    elif isinstance(omengine_result, dict):
                                        status = True
                                        data_no = omengine_result['data_no']
                                        message = _('開單成功。')
                                else:
                                    message = _('更新成功。')
                                    status = True
                            else:
                                message = _('缺少必填欄位。')
                        else:
                            message = _('該流程目前並未處於人工處理點，無法人工推進流程。')
                    else:
                        message = _('該流程目前為停用狀態。')
                except MultipleObjectsReturned:
                    message = _('該流程有多個已上架的版本，請聯絡系統管理員協助處理。')
                except ObjectDoesNotExist:
                    message = _('該流程沒有已上架的版本')
            else:
                message = _('該單目前為執行狀態，無法進行更新/刪除。')
        else:
            message = _('找不到該資料庫：Omdata_')+flow_uuid
    except Exception as e:
        debug(e.__str__())
        message = e.__str__()
    finally:
        result['message'] = message
        result['status'] = status
        result['data_no'] = data_no
        return result


def doQuickAction(flowactive, quick_action, stop_uuid, omdata_dict):
    merge_formobject = json.loads(flowactive.merge_formobject)
    if quick_action == 'action1' and flowactive.action1:
        action = json.loads(flowactive.action1)
    elif quick_action == 'action2' and flowactive.action2:
        action = json.loads(flowactive.action2)
    else:
        action = {}
    action_dict = action.get(stop_uuid,'')
    if action_dict:
        action_input_list = action_dict['input']
        #取得flow value
        flow_value = json.loads(omdata_dict['data_param'])['flow_value']
        quick_formdata_list = []
        action_input_name_list = []
        for action_input in action_input_list:
            #找到input的值是flow value還是欄位還是字串
            name = action_input['name'][2:-1]
            value = action_input['value']
            action_input_name_list.append(name)
            if value == None:
                input_value = ''
            elif re.match(r'\$\(.+\)', value):
                input_value = flow_value.get(value[2:-1],'')
            elif re.match(r'#[A-Z]*[0-9]*\(.+\)', value):
                table_field = value[2:-1].lower()
                input_value = omdata_dict[table_field]
            else:
                input_value = value
            #確認填入的欄位類型
            merge_item = merge_formobject.get(name,{})
            FormatToFormdataList(merge_item, input_value, quick_formdata_list)
        #把表單中的欄位值都帶入formdata_list
#                                     for item in items:
#                                         if item['id'][:8] == 'FORMITM_' and item['id'] not in action_input_name_list:
#                                             omdata_value = omdata_dict.get(item['id'].lower(),'')
#                                             FormatToFormdataList(item, omdata_value, quick_formdata_list)
        return quick_formdata_list


def deleteOmData(param):
    '''
    delete ticket.
    input: param,user
    return: json
    author: Kolin Hsu
    '''
    #function variable
    result = {}
    message = ''
    status = False
    flow_uuid = param.get('flow_uuid','')
    data_no = param.get('data_no','')
    data_id = param.get('data_id','')
    #get omdata object
    try:
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        omdata_value_history_model = getModel('omformmodel', 'Omdata_' + flow_uuid + '_ValueHistory')
        if omdata_model and omdata_value_history_model:
            omdata = omdata_model.objects.get(id=data_id)
            #check this ticket's status is not running
            if not omdata.running:
                #刪除該筆單以及所有歷史資料
                omdata_model.objects.filter(data_no=data_no).delete()
                #刪除該筆單的flow value
                omdata_value_history_model.objects.filter(data_no=data_no).delete()
                #刪除該筆單的附檔
                d_f = deleteOmdataFiles(flow_uuid, data_no)
                #刪除該筆單的所有mission
                deleteMission(flow_uuid, data_no)
                #刪除相關關聯
                deleteOmDataRelationAjax(flow_uuid, [data_no])
                
                if d_f:
                    message = _('刪除成功。')
                    status = True
                else:
                    message = _('刪除檔案失敗，請聯絡管理員清理剩餘檔案。')
                    status = False
            else:
                message = _('該單目前為執行狀態，無法進行更新/刪除。')
        else:
            message = _('找不到該資料庫：Omdata_')+flow_uuid
    except Exception as e:
        debug(e.__str__())
        message = _('找不到該筆資料。')
    finally:
        result['message'] = message
        result['status'] = status
        return result


#檔案上傳、表列
@login_required
@try_except
def uploadOmdataFilesAjax(request):
    '''
    upload file
    input: request
    return: file
    author: Kolin Hsu
    '''
    #function variable
    files = request.FILES.getlist('files','')
    #get postdata
    postdata = getPostdata(request)
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    if checkOmDataPermission(request.user, flow_uuid, None, data_id, '_Modify'):
        uploadOmdataFiles(files, flow_uuid, data_no, data_id, request.user.username)
        info(request ,'%s upload OmData file success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('上傳成功。')).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


def uploadOmdataFiles(files, flow_uuid, data_no, data_id, user):
    try:
        file_name_list = []
        for f in files:
            file_name_list.append(f.name)
        d_files = OmdataFiles.objects.filter(flow_uuid=flow_uuid,data_no=data_no,data_id=data_id,file_name__in=file_name_list)
        d_file_list = list(d_files.values())
        for file in d_file_list:
            file_path = os.path.join(settings.MEDIA_ROOT, file['file'])
            if os.path.isfile(file_path):
                os.remove(file_path)
        d_files.delete()
        #儲存上傳的檔案
        OmdataFiles.objects.bulk_create([OmdataFiles(flow_uuid=flow_uuid,data_no=data_no,data_id=data_id,file=file,size=file.size,file_name=file.name,upload_user_id=user) for file in files])
        #修改mission
        Missions.objects.filter(flow_uuid=flow_uuid,data_no=data_no,attachment=False).update(attachment=True)
        return True
    except Exception as e:
        debug(e.__str__())
        return False


def deleteOmdataFiles(flow_uuid, data_no):
    try:
        files = OmdataFiles.objects.filter(flow_uuid=flow_uuid,data_no=data_no)
        file_list = list(files.values())
        for file in file_list:
            file_path = os.path.join(settings.MEDIA_ROOT, file['file'])
            if os.path.isfile(file_path):
                os.remove(file_path)
        files.delete()
        return True
    except Exception as e:
        debug(e.__str__())
        return False
    

@login_required
@try_except
def listOmDataFilesAjax(request):
    '''
    list omdata.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    delete_id_list = []
    #get post data
    postdata = getPostdata(request)
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    if checkOmDataPermission(request.user, flow_uuid, None, data_id, '_View'):
        field = ['id','file','size','delete','createtime','file_name']
#         if data_id:
#             #目前沒有功能使用
#             files = list(OmdataFiles.objects.filterformat(*field,flow_uuid=flow_uuid,data_no=data_no,data_id=data_id))
#         else:
        files = list(OmdataFiles.objects.filterformat(*field,flow_uuid=flow_uuid,data_no=data_no).order_by('-createtime'))
        #檢查所有當案是否都還在存在，同時進行去重複
        distinct_file_list = []
        file_name_list = []
        for file in files:
            file_path = os.path.join(settings.MEDIA_ROOT, file['file'])
            if not file['delete'] and not os.path.exists(file_path):
                file['delete'] = True
                delete_id_list.append(file['id'])
            if file['file_name'] in file_name_list:
                pass
            else:
                file_name_list.append(file['file_name'])
                distinct_file_list.append(file)
        #清除遭人為砍檔案的資料
        if delete_id_list:
            OmdataFiles.objects.filter(id__in=delete_id_list).update(delete=True)
        info(request ,'%s load OmData file success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), distinct_file_list).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


#編輯流程列表顯示欄位
@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def getFlowFieldNameAjax(request):
    '''
    get flow field.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    default_field = ['data_no','status','level','error','error_message','stop_chart_text','updatetime','create_user']
    require_field = ['flow_name','app_name']
    result = {}
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_name = postdata.get('flow_name','')
    app_name = postdata.get('app_name','')
    need_default_field = postdata.get('need_default_field',False)
    if checker.get('status') == 'success':
        try:
            flowactive = FlowActiveGlobalObject.NameSearch(flow_name, None, app_name)
            flow_uuid = flowactive.flow_uuid.hex
            items = json.loads(flowactive.formobject)['items']
            if need_default_field:
                result['display_field'] = flowactive.display_field
                #get omdata model
                omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
                #組合固定欄位
                for field in omdata_model._meta.fields:
                    if (field.name in default_field) and ('formitm_' not in field.name):
                        result[field.name] = field.verbose_name
            #組合動態欄位
            for item in items:
                if item['id'][:8] == 'FORMITM_':
                    if item['type'] == 'h_group':
                        result[item['id'].lower()+'-group'] = item['config']['group_title']
                        result[item['id'].lower()+'-user'] = item['config']['user_title']
                    elif need_default_field and item['type'] in ['h_level','h_status']:
                        pass
                    else:
                        result[item['id'].lower()] = item['config']['title']
            info(request ,'%s get flow field name success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
        except Exception as e:
            error(request,e)
            return ResponseAjax(statusEnum.not_found, _('找不到該流程。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@try_except
def getFlowActiveDisplayFieldAjax(request):
    '''
    get flow display_field.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    result = {}
    display_text = {}
    postdata = getPostdata(request)
    flow_uuid = postdata.get('a_flow_uuid','')
    if request.user.has_perm('omformmodel.Omdata_' + flow_uuid + '_View'):
        fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
        display_field = json.loads(fa.display_field)
        new_display_field = {}
        items = json.loads(fa.formobject)['items']
        for key in display_field:
            if key == 'create_user_id' or key == 'create_user':
                new_key = 'create_user_id__nick_name'
            elif key == 'update_user_id' or key == 'update_user':
                new_key = 'update_user_id__nick_name'
            else:
                new_key = key
            if key[:8] == 'formitm_':
                for item in items:
                    if item['id'].lower() == key:
                        if item['config'].get('lists',''):
                            display_text[key] = item['config'].get('lists','')
            new_display_field[new_key] = display_field[key]
        result = {'display_field':json.dumps(new_display_field),'display_text':display_text}
        info(request ,'%s get flow display field success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


@login_required
@try_except
def listOmDataAjax(request):
    '''
    list omdata.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    flow_uuid = postdata.get('flow_uuid','')
    updatetime = postdata.get('updatetime','')
    closed = postdata.get('closed',[0])
    display_field_list = []
    search_field_list = []
    if request.user.has_perm('omformmodel.Omdata_' + flow_uuid + '_View'):
        #get field setting
        flowactive = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
        display_field_dict = json.loads(flowactive.display_field)
        for key in display_field_dict:
            if '-' in key:
                key = re.findall(r'(.+)-[a-z]', key)[0]
            if key == 'create_user_id' or key == 'create_user':
                key = 'create_user_id__nick_name'
            elif key == 'update_user_id' or key == 'update_user':
                key = 'update_user_id__nick_name'
            display_field_list.append(key)
        display_field_list.append('id')
        display_field_list.append('data_no')
        display_field_list.append('stop_uuid')
        display_field_list.append('stop_chart_text')
        display_field_list.append('error')
        display_field_list.append('error_message')
        display_field_list.append('closed')
        display_field_list.append('running')
        search_field_list = display_field_list.copy()
#         search_field_list.append('data_no')
#         search_field_list.append('create_user_id__username')
        #暫時先使用display_field當作search_field
        field_list = list(map(lambda search_field : search_field + '__icontains', search_field_list))
        #get model
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        query = omdata_model.objects.filter(closed__in=closed,updatetime__lte=updatetime,history=False).values(*display_field_list)
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list OmData success.' % request.user.username)
        return JsonResponse(result)
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


@login_required
@try_except
def listOmDataHistoryAjax(request):
    '''
    list omdata history.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['update_user__username__icontains','data_no__icontains']
    #get post data
    postdata = getPostdata(request)
    flow_uuid = postdata.get('flow_uuid','')
    createtime = postdata.get('createtime','')
    closed = postdata.get('closed',[1,0])
    manage = int(postdata.get('manage',1))
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    if checkOmDataPermission(request.user, flow_uuid, None, data_id, '_View') or request.user.has_perm('omformflow.OmFormFlow_Manage'):
        if manage:
            display_field = ['data_no','history','stop_uuid','stop_chart_text','error','error_message','createtime','update_user','id']
        else:
            display_field = ['level','status','updatetime','update_user','id']
        #get model
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        if data_no:
            query = omdata_model.objects.filter(Q(data_no=data_no) & (Q(history=True) & Q(closed=False))).values(*display_field)
        else:
            query = omdata_model.objects.filter(closed__in=closed,createtime__lte=createtime).values(*display_field)
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list OmDataHistory success.' % request.user.username)
        return JsonResponse(result)
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
   

@login_required
@try_except
def listOmDataRelationAjax(request):
    '''
    input: request
    return: json
    author: Arthur
    '''
    #function variable
    field_list=['relation_type__icontains']
    #get post data
    postdata = getPostdata(request)
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    
    if checkOmDataPermission(request.user, flow_uuid, data_no, data_id, '_View') or request.user.has_perm('omformflow.OmFormFlow_Manage'):
        display_field = ['id','subject_flow','subject_no','object_flow','object_no','relation_type','relation_percentage','createtime','create_user_id__username']
        #get model
        query = OmdataRelation.objects.filter(Q(subject_flow=flow_uuid,subject_no=data_no) | Q(object_flow=flow_uuid,object_no=data_no)).values(*display_field)
        
        result = copy.deepcopy(DatatableBuilder(request, query, field_list))
        if isinstance(result["data"], list):
            for row in result["data"]:
                isSubject = True if row['subject_flow']==flow_uuid and row['subject_no']==data_no else False
                if isSubject:
                    object_flow = row['subject_flow']
                    object_no = row['subject_no']
                    row['relation_type'] = switchRelation(row['relation_type'])
                else:
                    object_flow = row['object_flow']
                    object_no = row['object_no']
                    
                thisFlow = FlowActiveGlobalObject.UUIDSearch(object_flow)
                thisModel = getModel('omformmodel','Omdata_' + object_flow)
                thisData = thisModel.objects.filter(data_no=object_no).last()#.aggregate(Max('id'))
                
                row['flow_uuid'] = thisFlow.flow_uuid.hex
                row['flow_name'] = thisFlow.flow_name
                row['title'] = thisData.title if hasattr(thisData, 'title') else ''
                row['data_no'] = thisData.data_no
                row['data_id'] = thisData.id
                row['level'] = thisData.title if hasattr(thisData, 'level') else 'green'
                row['closed'] = thisData.closed
            
        elif isinstance(result["data"], dict):
            for key in result["data"]:
                row = result["data"][key]
                isSubject = True if row['subject_flow']==flow_uuid and row['subject_no']==data_no else False
                if isSubject:
                    object_flow = row['subject_flow']
                    object_no = row['subject_no']
                    row['relation_type'] = switchRelation(row['relation_type'])
                else:
                    object_flow = row['object_flow']
                    object_no = row['object_no']
                    
                thisFlow = FlowActiveGlobalObject.UUIDSearch(object_flow)
                thisModel = getModel('omformmodel','Omdata_' + object_flow)
                thisData = thisModel.objects.filter(data_no=object_no).last()#.aggregate(Max('id'))
                
                row['flow_uuid'] = thisFlow.flow_uuid.hex
                row['flow_name'] = thisFlow.flow_name
                row['title'] = thisData.title
                row['data_no'] = thisData.data_no
                row['data_id'] = thisData.id
                row['level'] = thisData.level
                row['closed'] = thisData.closed
            
        info(request ,'%s list OmDataRelation success.' % request.user.username)
        return JsonResponse(result)
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


@login_required
@try_except
def editOmDataRelationAjax(request):
    '''
    input: request
    return: json
    author: Arthur
    '''
    #get post data
    postdata = getPostdata(request)
    action = postdata.get('action','')
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    if action == 'create' and (checkOmDataPermission(request.user, flow_uuid, data_no, data_id, '_Modify') or request.user.has_perm('omformflow.OmFormFlow_Manage')):
        user = request.user
        subject_flow = flow_uuid
        subject_no = data_no
        object_flow = postdata.get('object_flow','')
        object_no_list = postdata.get('object_no',[])
        relation_type = postdata.get('relation_type','')
        relation_percentage = postdata.get('relation_percentage',0)
        
        #判斷是否同表單
        if subject_flow == object_flow :
            #判斷是否為同編號
            if subject_no in object_no_list :
                info(request ,'%s add OmDataRelation error.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('關聯對象不可為同一資料。')).returnJSON()
        
        elif relation_type in ['parent','child']:
            info(request ,'%s add OmDataRelation error.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('不同表單資料不可建立母子關聯。')).returnJSON()
        
        display_field = ['subject_flow','subject_no','object_flow','object_no','relation_type']
        query_list = list(OmdataRelation.objects.filter(Q(subject_flow=flow_uuid,subject_no=data_no) | Q(object_flow=flow_uuid,object_no=data_no)).values_list(*display_field))
        OmdataRelationList = []
        for object_no in object_no_list:
            rowA = (uuid.UUID(subject_flow),int(subject_no),uuid.UUID(object_flow),int(object_no),relation_type)
            rowB = (uuid.UUID(object_flow),int(object_no),uuid.UUID(subject_flow),int(subject_no),switchRelation(relation_type))
            if rowA in query_list or rowB in query_list :
                pass
            else :
                OmdataRelationList.append(
                    OmdataRelation(\
                        subject_flow=subject_flow,\
                        subject_no=subject_no,\
                        object_flow=object_flow,\
                        object_no=object_no,\
                        relation_type=relation_type,\
                        relation_percentage=relation_percentage,\
                        create_user=user\
                    )
                )
        
        OmdataRelation.objects.bulk_create(OmdataRelationList);
        
        info(request ,'%s add OmDataRelation success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('建立關聯成功。')).returnJSON()
    
    elif action == 'update' and (checkOmDataPermission(request.user, flow_uuid, data_no, data_id, '_Modify') or request.user.has_perm('omformflow.OmFormFlow_Manage')):
        info(request ,'%s update OmDataRelation success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('更改關聯成功。')).returnJSON()
    
    elif action == 'delete' and (checkOmDataPermission(request.user, flow_uuid, data_no, data_id, '_Modify') or request.user.has_perm('omformflow.OmFormFlow_Manage')):
        id_list = postdata.get('id',[])
        id_list = OmdataRelation.objects.filter(Q(subject_flow=flow_uuid,subject_no=data_no,id__in=id_list) | Q(object_flow=flow_uuid,object_no=data_no,id__in=id_list)).values_list('id', flat=True)
        OmdataRelation.objects.filter(id__in=id_list).delete()
        info(request ,'%s delete OmDataRelation success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('刪除關聯成功。')).returnJSON()
    
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


def switchRelation(relation_type):
    '''
    input: relation_type
    author: Arthur
    '''
    if relation_type == 'parent':
        return 'child'
    elif relation_type == 'child':
        return 'parent'
    elif relation_type == 'affect':
        return 'affected'
    elif relation_type == 'affected':
        return 'affect'
    elif relation_type == 'own':
        return 'belong'
    elif relation_type == 'belong':
        return 'own'


def deleteOmDataRelationAjax(flow_uuid,data_no_list):
    '''
    input: request
    return: json
    author: Arthur
    '''
    #get post data
    try:
        OmdataRelation.objects.filter(Q(subject_flow=flow_uuid,subject_no__in=data_no_list) | Q(object_flow=flow_uuid,object_no__in=data_no_list)).delete()
        return True
    except:
        return False


@login_required
@try_except
def listOmData4RelationAjax(request):
    '''
    list omdata.
    input: request
    return: json
    author: Arthur
    '''
    #get post data
    postdata = getPostdata(request)
    flow_uuid = postdata.get('flow_uuid','')
    updatetime = postdata.get('updatetime','')
    relation = postdata.get('relation','')
    data_no = postdata.get('data_no','')
    closed = postdata.get('closed',[0])
    display_field_list = []
    search_field_list = []
    if request.user.has_perm('omformmodel.Omdata_' + flow_uuid + '_View'):
        #get field setting
        flowactive = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
        display_field_dict = json.loads(flowactive.display_field)
        for key in display_field_dict:
            if '-' in key:
                key = re.findall(r'(.+)-[a-z]', key)[0]
            if key == 'create_user_id' or key == 'create_user':
                key = 'create_user_id__nick_name'
            elif key == 'update_user_id' or key == 'update_user':
                key = 'update_user_id__nick_name'
            display_field_list.append(key)
        display_field_list.append('id')
        display_field_list.append('data_no')
        display_field_list.append('stop_uuid')
        display_field_list.append('stop_chart_text')
        display_field_list.append('error')
        display_field_list.append('error_message')
        display_field_list.append('closed')
        display_field_list.append('running')
        search_field_list = display_field_list.copy()

        field_list = list(map(lambda search_field : search_field + '__icontains', search_field_list))
        #get model
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        query = omdata_model.objects.filter(closed__in=closed,updatetime__lte=updatetime,history=False).values(*display_field_list)
        
        #判斷類型
        no_list = [data_no]
        if relation=='parent':
            no_list = no_list + list(OmdataRelation.objects.filter(subject_flow=flow_uuid,relation_type="parent").values_list('subject_no',flat=True))
            no_list = no_list + list(OmdataRelation.objects.filter(object_flow=flow_uuid,relation_type="child").values_list('object_no',flat=True))
        elif relation=='child':
            no_list = no_list + list(OmdataRelation.objects.filter(subject_flow=flow_uuid,relation_type="child").values_list('subject_no',flat=True))
            no_list = no_list + list(OmdataRelation.objects.filter(object_flow=flow_uuid,relation_type="parent").values_list('object_no',flat=True))
            
        success_msg = '%s list OmData success.'
        
        try:
            query = query.exclude(data_no__in=no_list)
        except:
            success_msg = '%s list OmData success but too many variables.'
        
        info(request , success_msg % request.user.username)
        result = DatatableBuilder(request, query, field_list)
        return JsonResponse(result)
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


#流程暫停點推進方法
def pushSleepPoint(param):
    '''
    push omdata to next point.
    input: param
    return: json
    author: Kolin Hsu
    '''
    data = param['formdata']
    data['chart_id_from'] = None
    flow_uuid = data['flow_uuid']
    OmEngine(flow_uuid,data).checkActive()


#我的任務、任務歷史、流程列表 --- 點擊表單
@login_required
@try_except
def loadOmDataAjax(request):
    '''
    load omdata.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_uuid','data_id']
    dict_type_list = ['h_group']
    list_type_list = ['checkbox']
    quick_action = None
    find_item = False
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    data_id = postdata.get('data_id','')
    if checkOmDataPermission(request.user, flow_uuid, None, data_id, '_View'):
        if checker.get('status') == 'success':
            try:
                main_fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                app_name = main_fa.flow_app.app_name
                formobject = {}
                formdata = []
                omdata_model = getModel('omformmodel', 'Omdata_' + flow_uuid)
                omdata = omdata_model.objects.get(id=data_id)
                omdata_param = json.loads(omdata.data_param)
                fa = FlowActiveGlobalObject.UUIDSearch(omdata_param['flow_uuid'])
                flowobject = json.loads(fa.flowobject)
                config = {'fp_show':main_fa.fp_show,'worklog':main_fa.worklog,'history':main_fa.history,'attachment':main_fa.attachment,'relation':main_fa.relation}
                #get files
                omdata_files = list(OmdataFiles.objects.filterformat('file','size','createtime','delete','file_name','upload_user_id__nick_name',flow_uuid=flow_uuid,data_id=data_id))
                stop_uuid = omdata.stop_uuid
                stop_uuid_list = stop_uuid.split('-')
                stop_uuid_index = len(stop_uuid_list) - 1
                chart_id = stop_uuid_list[stop_uuid_index]
                items = flowobject['items']
                for item in items:
                    if item['id'] == chart_id:
                        if item['type'] == 'form':
                            find_item = True
                            #找出快速操作設定
                            action1_text = ''
                            action2_text = ''
                            if fa.action1:
                                action1 = json.loads(fa.action1).get(chart_id,'')
                                if action1:
                                    action1_text = action1['text']
                            if fa.action2:
                                action2 = json.loads(fa.action2).get(chart_id,'')
                                if action2:
                                    action2_text = action2['text']
                            quick_action = action1_text + ',' + action2_text
                            #如果停留點是form，取得該人工點的表單設計
                            if not item['config']['form_object']:
                                if fa.formobject:
                                    formobject = json.loads(fa.formobject)
                                else:
                                    p_fa = FlowActiveGlobalObject.UUIDSearch(fa.parent_uuid.hex)
                                    formobject = json.loads(p_fa.formobject)
                            else:
                                if isinstance(item['config']['form_object'], dict):
                                    formobject = item['config']['form_object']
                                elif isinstance(item['config']['form_object'], str):
                                    formobject = json.loads(item['config']['form_object'])
                        break
                if not find_item:
                    if flow_uuid == omdata_param['flow_uuid']:
                        formobject = json.loads(fa.formobject)
                    else:
                        formobject = json.loads(main_fa.formobject)
                omdata_dict = omdata.__dict__
                form_items = formobject.get('items',[])
                for form_item in form_items:
                    form_dict = {}
                    item_id = form_item['id'].lower()
                    if item_id[:8] == 'formitm_':
                        if form_item['type'] in dict_type_list:
                            if omdata_dict[item_id]:
                                json_value = json.loads(omdata_dict[item_id])
                            else:
                                json_value = {}
                        elif form_item['type'] in list_type_list:
                            if omdata_dict[item_id]:
                                json_value = json.loads(omdata_dict[item_id])
                            else:
                                json_value = []
                        else:
                            json_value = omdata_dict[item_id]
                        form_dict['id'] = form_item['id']
                        form_dict['value'] = json_value
                        form_dict['type'] = form_item['type']
                        formdata.append(form_dict)
                result = {'formobject':formobject, 'formdata':formdata, 'config':config, 'flow_name':main_fa.flow_name, 'app_name':app_name, 'quick_action':quick_action, 'files':omdata_files, 'find_item':find_item, 'closed':omdata.closed}
                info(request ,'%s load OmData success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
            except Exception as e:
                info(request ,'load OmData error: ' + e.__str__())
                return ResponseAjax(statusEnum.not_found, _('找不到該流程。')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


#已上架流程中選擇表單進行推進
@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def getFlowValueAjax(request):
    '''
    get ticket's flow value.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_uuid','data_no','data_id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    if checker.get('status') == 'success':
        #get model
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        data_str = list(omdata_model.objects.filter(data_no=data_no,id=data_id).values_list('data_param',flat=True))[0]
        data_dict = json.loads(data_str)
        result = data_dict.get('flow_value','')
        info(request ,'%s get flow value success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    

@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def updateFlowValueAjax(request):
    '''
    update ticket's flow value.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_uuid','data_no','data_id','flow_value']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    flow_value = json.loads(postdata.get('flow_value'))
    if checker.get('status') == 'success':
        #get model
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        omdata = omdata_model.objects.get(data_no=data_no,id=data_id)
        if not omdata.history:
            if not omdata.closed:
                if not omdata.running:
                    if omdata.error:
                        data = json.loads(omdata.data_param)
                        data['flow_value'] = flow_value
                        #整理formdata
                        omdata.stoptime = None
                        omdata.stop_uuid = None
                        omdata.stop_chart_text = None
                        omdata.error = False
                        omdata.error_message = None
                        omdata.running = True
                        omdata.update_user_id = request.user.username
                        omdata.data_param = json.dumps(data)
                        omdata.save()
                        #om engine
                        data['data_id'] = data_id
                        data['chart_id_from'] = None
                        omengine_result = OmEngine(flow_uuid, data).checkActive()
                        if isinstance(omengine_result, str):
                            info(request ,'%s update flow value error.' % request.user.username)
                            return ResponseAjax(statusEnum.success, _('更新失敗：') + omengine_result).returnJSON()
                        else:
                            info(request ,'%s update flow value success.' % request.user.username)
                            return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()
                    else:
                        info(request ,'%s update flow value error.' % request.user.username)
                        return ResponseAjax(statusEnum.not_found, _('此筆資料並無錯誤，無法進行修改。')).returnJSON()
                else:
                    info(request ,'%s update flow value error.' % request.user.username)
                    return ResponseAjax(statusEnum.not_found, _('此筆資料正在執行中，無法進行修改。')).returnJSON()
            else:
                info(request ,'%s update flow value error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, _('此筆資料已經關閉，無法進行修改。')).returnJSON()
        else:
            info(request ,'%s update flow value error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, _('無法修改歷史資料。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    

#表單歷程、表單現況
@login_required
@try_except
def loadFlowObjectAjax(request):
    '''
    load flow object.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_uuid','data_no','flow_level']
    subflow_uuid = None
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    flow_name = postdata.get('flow_name','')
    app_name = postdata.get('app_name','')
    flow_uid = postdata.get('flow_uid','')
    data_no = postdata.get('data_no','')
    parent_chart_id = postdata.get('parent_chart_id','')
    flow_level = postdata.get('flow_level','')
    #檢查權限
    if checkOmDataPermission(request.user, flow_uuid, data_no, None, '_View'):
        if checker.get('status') == 'success':
            try:
                if flow_uid: #子流程
                    fa = FlowActive.objects.filter(parent_uuid=flow_uuid,flow_uid=flow_uid).order_by('deploytime').reverse()[0]
                    subflow_uuid = fa.flow_uuid.hex
                elif flow_name and flow_uuid: #內部流程
                    app_id = FlowActiveGlobalObject.UUIDSearch(flow_uuid).flow_app_id
                    fa = FlowActive.objects.filter(flow_app_id=app_id,flow_name=flow_name).order_by('deploytime').reverse()[0]
                elif flow_name and app_name: #外部流程
                    fa = FlowActive.objects.filter(flow_app_id__app_name=app_name,flow_name=flow_name).order_by('deploytime').reverse()[0]
                else: #主流程
                    fa = FlowActive.objects.filter(flow_uuid=flow_uuid).order_by('deploytime').reverse()[0]
                inoutput = listFlowInOutput(flow_uuid, data_no, flow_level, subflow_uuid, parent_chart_id)
                result = {'flowobject':fa.flowobject,'inoutput':inoutput, 'flow_name':fa.flow_name}
                info(request ,'%s load flow object success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('更新成功。'), result).returnJSON()
            except Exception as e:
                error(request,e)
                return ResponseAjax(statusEnum.not_found, _('找不到流程。')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


def listFlowInOutput(flow_uuid,data_no,flow_level,subflow_uuid,parent_chart_id):
    '''
    list flow input and output.
    input: flow_uuid,data_no,flow_level
    return: json
    author: Kolin Hsu
    '''
    try:
        result = []
        field = ['chart_id','createtime','updatetime','input_data','output_data','error','stop_chart_type','stop_chart_text']
        #get flowobject items
        if subflow_uuid:
            items = json.loads(FlowActiveGlobalObject.UUIDSearch(subflow_uuid).flowobject)['items']
        else:
            items = json.loads(FlowActiveGlobalObject.UUIDSearch(flow_uuid).flowobject)['items']
        type_dict = {}
        subid_dict = {}
        for i in items:
            type_dict[i['id']] = i['type']
            subid_dict[i['id']] = i['config'].get('subflow_id','')
        #get model
        omdata_history_model = getModel('omformmodel','Omdata_' + flow_uuid + '_ValueHistory')
        omdata_history = list(omdata_history_model.objects.filterformat(*field,data_no=data_no))
        for i in omdata_history:
            stop_uuid = i['chart_id'].split('-')
            if '-' not in i['chart_id']:
                chart_id = i['chart_id']
                his_level = 1
                parent_check = True
            else:
                chart_id = stop_uuid[-1]
                his_level = len(stop_uuid)
                if parent_chart_id ==  stop_uuid[-2]:
                    parent_check = True
                else:
                    parent_check = False
            if his_level == int(flow_level) and parent_check:
                if i['input_data']:
                    try:
                        i['input_data'] = json.loads(i['input_data'])
                    except:
                        i['input_data'] = i['input_data']
                if i['output_data']:
                    try:
                        i['output_data'] = json.loads(i['output_data'])
                    except:
                        i['output_data'] = i['output_data']
                    #如果是外部流程或內部流程點，將output中的outflow_uuid以及outflow_data_no
                    #取出並另外拋給前端
                    if type_dict[chart_id] in ['outflow','inflow']:
                        try:
                            i['outflow_uuid'] = i['output_data'].pop('outflow_uuid')
                            i['outflow_data_no'] = i['output_data'].pop('outflow_data_no')
                        except:
                            pass
                if type_dict[chart_id] == 'subflow':
                    try:
                        i['subflow_uid'] = subid_dict.get(chart_id,'')
                    except:
                        pass
                result.append(i)
        return result
    except Exception as e:
        debug(e.__str__())
        return None
    

@login_required
@try_except
def createOmDataWorkLogAjax(request):
    '''
    create omdata worklog.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['data_no']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    flow_name = postdata.get('flow_name',None)
    app_name = postdata.get('app_name',None)
    app_id = postdata.get('app_id',None)
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    content = postdata.get('content','')
    if flow_name:
        flow_uuid = FlowActiveGlobalObject.NameSearch(flow_name, app_id, app_name).flow_uuid
    #檢查權限
    if checkOmDataPermission(request.user, flow_uuid, None, data_id, '_Modify'):
        if checker.get('status') == 'success':
            OmdataWorklog.objects.create(flow_uuid=flow_uuid,data_no=data_no,content=content,create_user=request.user)
            info(request ,'%s create omdata worklog success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('建立成功。')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
    

@login_required
@try_except
def listOmDataWorkLogAjax(request):
    '''
    list omdata worklog.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['data_no']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    #檢查權限
    if checkOmDataPermission(request.user, flow_uuid, None, data_id, '_View'):
        if checker.get('status') == 'success':
            result = list(OmdataWorklog.objects.filterformat('flow_uuid','create_user_id__nick_name','content','createtime',flow_uuid=flow_uuid,data_no=data_no))
            info(request ,'%s list omdata worklog success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('搜尋成功。'), result).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


#參數管理
@login_required
@try_except
def createOmParameterAjax(request):
    '''
    create parameter.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['name']
    #get post data
    postdata = getPostdata(request)
    group_id = postdata.get('group_id',None)
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        per_type = checkParameterPermission(group_id, request.user)
        if per_type:
            result = createOmParameter(postdata)
            if result['status']:
                info(request ,'%s create parameter success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('建立成功。')).returnJSON()
            else:
                info(request ,'%s create parameter error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
        else:
            info(request ,'%s create parameter error.' % request.user.username)
            return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def createOmParameter(postdata):
    try:
        status = True
        message = ''
        name = postdata.get('name','')
        value = postdata.get('value','')
        description = postdata.get('description','')
        p_type = postdata.get('type','')
        shadow = postdata.get('shadow',False)
        group_id = postdata.get('group_id',None)
        if group_id:
            if not OmParameter.objects.filter(name=name,group_id=group_id).exists():
                OmParameter.objects.create(name=name,value=value,description=description,type=p_type,shadow=shadow,group_id=group_id)
            else:
                status = False
                message = _('重複名稱。')
        else:
            if not OmParameter.objects.filter(name=name,group_id=None).exists():
                OmParameter.objects.create(name=name,value=value,description=description,type=p_type,shadow=shadow)
                GlobalObject.__OmParameter__[name] = value
            else:
                status = False
                message = _('重複名稱。')
    except Exception as e:
        debug(e.__str__())
        status = False
        message = e.__str__()
    finally:
        return {'status':status,'message':message}


@login_required
@try_except
def updateOmParameterAjax(request):
    '''
    update parameter.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['id']
    #get post data
    postdata = getPostdata(request)
    group_id = postdata.get('group_id',None)
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        per_type = checkParameterPermission(group_id, request.user)
        if per_type:
            result = updateOmParameter(postdata)
            if result['status']:
                info(request ,'%s create parameter success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()
            else:
                info(request ,'%s create parameter error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
        else:
            info(request ,'%s create parameter error.' % request.user.username)
            return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def updateOmParameter(postdata):
    try:
        status = True
        message = ''
        param_id = postdata.get('id','')
        name = postdata.get('name','')
        value = postdata.get('value','')
        description = postdata.get('description','')
        shadow = postdata.get('shadow','')
        p_type = postdata.get('type','')
        group_id = postdata.get('group_id',None)
        if group_id:
            if not OmParameter.objects.filter(name=name,group_id=group_id).exclude(id=param_id).exists():
                OmParameter.objects.filter(id=param_id,group_id=group_id).update(name=name,value=value,description=description,shadow=shadow,type=p_type)
            else:
                status = False
                message = _('重複名稱。')
        else:
            if not OmParameter.objects.filter(name=name,group_id=None).exclude(id=param_id).exists():
                OmParameter.objects.filter(id=param_id,group_id=None).update(name=name,value=value,description=description,shadow=shadow,type=p_type)
                GlobalObject.__OmParameter__[name] = value
            else:
                status = False
                message = _('重複名稱。')
    except Exception as e:
        status = False
        message = e.__str__()
        debug(e.__str__())
    finally:
        return {'status':status,'message':message}


@login_required
@try_except
def deleteOmParameterAjax(request):
    '''
    delete parameter.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['id']
    #get post data
    postdata = getPostdata(request)
    group_id = postdata.get('group_id',None)
    id_list = postdata.get('id',[])
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        per_type = checkParameterPermission(group_id, request.user)
        if per_type:
            deleteOmParameter(id_list, group_id)
            info(request ,'%s create parameter success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('刪除成功。')).returnJSON()
        else:
            info(request ,'%s create parameter error.' % request.user.username)
            return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def deleteOmParameter(id_list, group_id):
    try:
        if group_id:
            OmParameter.objects.filter(id__in=id_list,group_id=group_id).delete()
        else:
            op = OmParameter.objects.filter(id__in=id_list,group_id=None)
            name_list = list(op.values_list('name',flat=True))
            op.delete()
            for name in name_list:
                GlobalObject.__OmParameter__.pop(name)
    except Exception as e:
        debug(e.__str__())
    

@login_required
@try_except
def listOmParameterAjax(request):
    '''
    list parameter.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list = ['name__icontains','description__icontains']
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable','')
    group_id = postdata.get('group_id','')
    per_type = checkParameterPermission(group_id, request.user)
    if per_type:
        if datatable:
            if group_id:
                query = OmParameter.objects.filter(group_id=group_id).values()
            else:
                query = OmParameter.objects.filter(group_id=None).values()
            result = DatatableBuilder(request, query, field_list)
            info(request ,'%s list parameter success.' % request.user.username)
            return JsonResponse(result)
        else:
            result = listOmParameter(group_id)
            info(request ,'%s list parameter success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()
    else:
        info(request ,'%s create parameter error.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作')).returnJSON()


def listOmParameter(group_id):
    try:
        if group_id:
            result = FlowActive.objects.filter(group_id=group_id).values()
        else:
            result = FlowActive.objects.filter(group_id=None).values()
        return result
    except Exception as e:
        debug(e.__str__())


def checkParameterPermission(group_id, user):
    p = None
    if not group_id and user.has_perm('omformflow.OmFormFlow_Manage'):
        p = 1
    elif group_id and user.has_perm('ommonitor.OmMonitor_Manage'):
        p = 2
    return p


@login_required
@try_except
def exportOmParameterAjax(request):
    '''
    '''
    postdata = getPostdata(request)
    param_id_list = postdata.get('param_id_list','')
    result = list(OmParameter.objects.filter(id__in=param_id_list).values('name','value','type','description','shadow'))
    return ResponseAjax(statusEnum.success, _('匯出成功。'), result).returnJSON()
 
 
@login_required
@try_except
def importOmParameterAjax(request):
    postdata = getPostdata(request)
    param_list_str = postdata.get('param_list','')
    param_list = json.loads(param_list_str)
    param_name_list = []
    for pm in param_list:
        param_name_list.append(pm.get('name'))
    check_param = OmParameter.objects.filter(name__in=param_name_list)
    if check_param:
        result = []
        for check in check_param:
            result.append(check.name) 
        result = json.dumps(result,ensure_ascii=False)
        return ResponseAjax(statusEnum.not_found, result + _('重複名稱。')).returnJSON()
    else:
        OmParameter.objects.bulk_create([OmParameter(**pm) for pm in param_list])
        for pm in param_list:
            GlobalObject.__OmParameter__[pm['name']] = pm['value']
        return ResponseAjax(statusEnum.success, _('匯入成功。')).returnJSON() 


#collector接收policy
def receivePolicyAjax(request):
    '''
    collector receive policy.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    deploy_data = {}
    #get post data
    postdata = getPostdata(request)
    dispatch_policy = postdata.get('dispatch_policy','')
    if dispatch_policy:
        dispatch_policy = json.loads(dispatch_policy)
    app_attr = postdata.get('app_attr','')
    app_name = postdata.get('app_name','')
    schedule = postdata.get('schedule','')
    omparameter_sys = json.loads(postdata.get('omparameter_sys','[]'))
    omparameter_group = json.loads(postdata.get('omparameter_group','[]'))
    #import flow
    iwa_result = importWorkspaceApplication(dispatch_policy, request.user)
    if iwa_result['status']:
        #上架流程
        app_id = iwa_result['id_list'][0]
        ex_fa = FlowActiveGlobalObject.NameSearch(app_name, None, app_name)
        if ex_fa:
            a_app_id = ex_fa.flow_app.id
        else:
            a_app_id = ''
        deploy_data['lside_pid '] = ''
        deploy_data['w_app_id'] = app_id
        deploy_data['app_name'] = app_name
        deploy_data['a_app_id'] = a_app_id
        dwa_result = deployWorkspaceApplication(deploy_data, request.user)
        if dwa_result['status']:
            fa = FlowActiveGlobalObject.NameSearch(app_name, None, app_name)
            schedule_id_list = list(Scheduler.objects.filter(flowactive_id=fa.id).values_list('id',flat=True))
            deleteSchedule(schedule_id_list)
            #設定排程
            if schedule:
                schedule = json.loads(schedule)
                schedule['flow_id'] = str(fa.id)
                schedule['flow_uuid'] = fa.flow_uuid.hex
                schedule['formdata'] = {}
                module_name = 'omformflow.views'
                method_name = 'createOmData'
                createSchedule(schedule, module_name, method_name)
            #建立參數
            gp_name_list = []
            for gp in omparameter_group:
                gp_name_list.append(gp['name'])
            for sp in omparameter_sys:
                if sp['name'] not in gp_name_list:
                    omparameter_group.append(sp)
            OmParameter.objects.bulk_create([OmParameter(**p) for p in omparameter_group])
            #刪除workspace
            WorkspaceApplication.objects.all().delete()
            info(request ,'%s receive policy success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('派送成功。')).returnJSON()
        else:
            info(request ,'%s receive policy error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, dwa_result['message']).returnJSON()
    else:
        info(request ,'%s receive policy error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, iwa_result['message']).returnJSON()
    


def flowMaker(flow_uuid, flowobject, version, subflow_mapping_dict={}):
    '''
    create custom flow python file.
    input: json
    return: boolean
    author: Kolin Hsu
    '''
    try:
        if isinstance(flowobject, str):
            flowobject = json.loads(flowobject)
        version = str(version)
        #check path exist or not
        file_path = os.path.join(settings.BASE_DIR, "omformflow", "production", flow_uuid, version)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        #function variable
        first_ifelse = True
        file_content = ''
        flowobject_items = flowobject['items']
        switch_error_message = _('找不到符合的條件。')
        python_error_message = _('找不到符合的條件。')
        #distinguish line or source item
        line_list = list(filter((lambda f_item : f_item['type'] == 'line'),flowobject_items))
        chart_list = list(filter((lambda f_item : f_item['type'] != 'line'),flowobject_items))
        #create custom flow python code#
        file_content += "import os, uuid, json\n"
        file_content += "from omflow.syscom.omengine import OmEngine\n"
        file_content += "from omflow.global_obj import GlobalObject\n"
        file_content += "from omflow.settings import BASE_DIR\n"
        file_content += "flow_uuid = '" + flow_uuid + "'\n"
        file_content += "version = " + version + "\n"
        file_content += "def main(data):\n"
        code_space = "    "
        file_content += code_space + "chart_id = data.get('chart_id_from','')\n"
        file_content += code_space + "file_path = os.path.join(BASE_DIR, 'omformflow', 'production', flow_uuid, str(version))\n"
        for chart in chart_list:
            next_chart_id_list = []
            new_line_list = []
            config = chart['config']
            chart_id = chart['id']
            #get next chart id
            for line in line_list:
                if line['config']['source_item'] == chart_id:
                    next_chart_id_list.append(line['config']['target_item'])
                else:
                    new_line_list.append(line)
            line_list = new_line_list
            if first_ifelse:
                file_content += code_space + "if chart_id == '" + chart_id + "':\n"
                first_ifelse = False
            else:
                file_content += code_space + "elif chart_id == '" + chart_id + "':\n"
            code_space += "    "
            file_content += code_space + "try:\n"
            code_space += "    "
            if chart['type'] in ['start','end','org1','org2','outflow','inflow','setform','sleep','form','collection']:
                #this point has nothing to do
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'python':
                #create chart.py
                code = config['code']
                chart_file = os.path.join(file_path, chart_id+".py")
                cf = open(chart_file,"w+",encoding='UTF-8')
                cf.write(code)
                cf.close()
                #get chart's input and output variable
                file_content += code_space + "autoinstall = data.get('autoinstall',False)\n"
                file_content += code_space + "load_balance = data.get('load_balance',False)\n"
                file_content += code_space + "chart_input = data['chart_input']\n"
                file_content += code_space + "chart_input_str = json.dumps(chart_input)\n"
                file_content += code_space + "chart_input_c = json.loads(chart_input_str)\n"
                #get or set chart compile object
                file_content += code_space + "import_error = False\n"
                file_content += code_space + "package = ''\n"
                file_content += code_space + "key = flow_uuid + '_' + chart_id\n"
                file_content += code_space + "compileObj = GlobalObject.__chartCompileObj__.get(key,'')\n"
                file_content += code_space + "chart_file_path = os.path.join(file_path, chart_id + '.py')\n"
                file_content += code_space + "if load_balance:\n"
                code_space += "    "
                file_content += code_space + "with open(chart_file_path,'r',encoding='UTF-8') as f:\n"
                code_space += "    "
                file_content += code_space + "chart_file = f.read()\n"
                file_content += code_space + "f.close()\n"
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "else:\n"
                code_space += "    "
                file_content += code_space + "if not compileObj:\n"
                code_space += "    "
                file_content += code_space + "with open(chart_file_path,'r',encoding='UTF-8') as f:\n"
                code_space += "    "
                file_content += code_space + "chart_file = f.read()\n"
                file_content += code_space + "f.close()\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "import_str = ''\n"
                file_content += code_space + "chart_file_to_list = chart_file.split('\\n')\n"
                file_content += code_space + "for line in chart_file_to_list:\n"
                code_space += "    "
                file_content += code_space + "line_lstrip = line.lstrip()\n"
                file_content += code_space + "if (line_lstrip[:7] == 'import ') or (line_lstrip[:5] == 'from '):\n"
                code_space += "    "
                file_content += code_space + "import_str += line_lstrip + '\\n'\n"
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "compile_import_str = compile(import_str,'','exec')\n"
                file_content += code_space + "loop = True\n"
                file_content += code_space + "last_package = ''\n"
                file_content += code_space + "while loop:\n"
                code_space += "    "
                file_content += code_space + "try:\n"
                code_space += "    "
                file_content += code_space + "exec(compile_import_str)\n"
                file_content += code_space + "compileObj = compile(chart_file,'','exec')\n"
                file_content += code_space + "loop = False\n"
                file_content += code_space + "package = ''\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "if 'No module named ' in e.__str__():\n"
                code_space += "    "
                file_content += code_space + "import subprocess\n"
                file_content += code_space + "import sys\n"
                file_content += code_space + "package = e.__str__()[17:-1]\n"
                file_content += code_space + "if package == last_package or (not autoinstall):\n"
                code_space += "    "
                file_content += code_space + "import_error = True\n"
                file_content += code_space + "loop = False\n"
                file_content += code_space + "data['error'] = True\n"
                file_content += code_space + "data['error_message'] = e.__str__()\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "else:\n"
                code_space += "    "
                file_content += code_space + "last_package = package\n"
                file_content += code_space + "try:\n"
                code_space += "    "
                if settings.PYTHON_PATH:
                    file_content += code_space + "subprocess.check_call(['" + settings.PYTHON_PATH + "', '-m', 'pip', 'install', package])\n"
                else:
                    file_content += code_space + "subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "import_error = True\n"
                file_content += code_space + "loop = False\n"
                file_content += code_space + "data['error'] = True\n"
                file_content += code_space + "data['error_message'] = e.__str__()\n"
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "else:\n"
                code_space += "    "
                file_content += code_space + "import_error = True\n"
                file_content += code_space + "loop = False\n"
                file_content += code_space + "data['error'] = True\n"
                file_content += code_space + "data['error_message'] = e.__str__()\n"
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "if not import_error:\n"
                code_space += "    "
                file_content += code_space + "GlobalObject.__chartCompileObj__[key] = compileObj\n"
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "if not import_error:\n"
                code_space += "    "
                file_content += code_space + "exec(compileObj,chart_input_c)\n"
                file_content += code_space + "for key in list(chart_input.keys()):\n"
                code_space += "    "
                file_content += code_space + "output_value = chart_input_c[key]\n"
                file_content += code_space + "if isinstance(output_value, list) or isinstance(output_value, dict):\n"
                code_space += "    "
                file_content += code_space + "output_value_str = json.dumps(output_value)\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "else:\n"
                code_space += "    "
                file_content += code_space + "output_value_str = str(output_value)\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "chart_input[key] = output_value_str\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "if package:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = '" + python_error_message + "' + package\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "else:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = e.__str__()\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'switch':
                #switch point
                file_content += code_space + "chart_input = data['chart_input']\n"
                file_content += code_space + "data['error'] = False\n"
                #find next point
                switch_rules = config['rules']
                for s_r in switch_rules:
                    #{'target': 'FITEM_2', 'value1': '$(NC)', 'value2': '30', 'rule': '='}
                    #{'type': 'switch', 'config': {'calculate': [], 'rules': [{'target': 'FITEM_5', 'value1': '$(NC)', 'value2': '30', 'rule': '!='}]}}
                    if s_r['rule'] == '=':
                        rule = '=='
                    else:
                        rule = s_r['rule']
                    value1 = s_r['value1']
                    value2 = s_r['value2']
                    if value1 == None:
                        pass
                    elif re.match(r'\$\(.+\)', value1) or re.match(r'#[A-Z]*[0-9]*\(.+\)', value1):
                        if re.match(r'\$\(.+\)', value1):
                            value1 = value1[2:-1]
                        else:
                            if re.match(r'#[A-Z][0-9]+\(.+\)', value1):
                                value1 = re.findall(r'#[A-Z][0-9]+\((.+)\)', value1)[0]
                            elif re.match(r'#\(.+\)', value1):
                                value1 = re.findall(r'#\((.+)\)', value1)[0]
                        if value2 == None:
                            file_content += code_space + "if chart_input['" + value1 + "'] " + rule + " '':\n"
                        elif re.match(r'\$\(.+\)', value2):
                            file_content += code_space + "if chart_input['" + value1 + "'] " + rule + " chart_input['" + value2[2:-1] + "']:\n"
                        elif re.match(r'#[A-Z]*[0-9]*\(.+\)', value2):
                            if re.match(r'#[A-Z][0-9]+\(.+\)', value2):
                                value2 = re.findall(r'#[A-Z][0-9]+\((.+)\)', value2)[0]
                            elif re.match(r'#\(.+\)', value2):
                                value2 = re.findall(r'#\((.+)\)', value2)[0]
                            file_content += code_space + "if chart_input['" + value1 + "'] " + rule + " chart_input['" + value2 + "']:\n"
                        else:
                            file_content += code_space + "if chart_input['" + value1 + "'] " + rule + " '" + value2 + "':\n"
                    else:
                        if value2 == None:
                            file_content += code_space + "if '" + value1 + "' " + rule + " '':\n"
                        elif re.match(r'\$\(.+\)', value2):
                            file_content += code_space + "if '" + value1 + "' " + rule + " chart_input['" + value2[2:-1] + "']:\n"
                        elif re.match(r'#[A-Z]*[0-9]*\(.+\)', value2):
                            if re.match(r'#[A-Z][0-9]+\(.+\)', value2):
                                value2 = re.findall(r'#[A-Z][0-9]+\((.+)\)', value2)[0]
                            elif re.match(r'#\(.+\)', value2):
                                value2 = re.findall(r'#\((.+)\)', value2)[0]
                            file_content += code_space + "if '" + value1 + "' " + rule + " chart_input['" + value2 + "']:\n"
                        else:
                            file_content += code_space + "if '" + value1 + "' " + rule + " '" + value2 + "':\n"
                    if value1 != None:
                        code_space += "    "
                        file_content += code_space + "data['chart_id_to'] = '" + s_r['target'] + "'\n"
                        code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except:\n"
                code_space += "    "
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'subflow':
                s_uid = config.get('subflow_id','')
                if s_uid and s_uid != 0 and s_uid != '0':
                    #set content
                    file_content += code_space + "data_str = json.dumps(data)\n"
                    file_content += code_space + "content = json.loads(data_str)\n"
                    file_content += code_space + "content['chart_id_to'] = '" + next_chart_id_list[0] + "'\n"
                    #set subflow data
                    subflow_uuid = subflow_mapping_dict.get(s_uid,'')
                    file_content += code_space + "data['flow_uuid'] = '" + subflow_uuid + "'\n"
                    file_content += code_space + "data['chart_id_from'] = ''\n"
                    file_content += code_space + "data['chart_id_to'] = 'FITEM_1'\n"
                    file_content += code_space + "data['flow_value'] = {}\n"
                    file_content += code_space + "data['content'] = content\n"
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'async':
                file_content += code_space + "data['error'] = False\n"
                file_content += code_space + "data['collection_uuid'] = uuid.uuid4().hex\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            #錯誤通過
            if config.get('error_pass',''):
                file_content += code_space + "data['error_pass'] = True\n"
            else:
                file_content += code_space + "data['error_pass'] = False\n"
            #確定下一個點
            if chart['type'] == 'switch':
                file_content += code_space + "if not data['chart_id_to']:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = '" + switch_error_message + "'\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "OmEngine(flow_uuid,data).checkActive()\n"
            elif chart['type'] == 'subflow':
                file_content += code_space + "OmEngine(data['flow_uuid'],data).checkActive()\n"
            elif chart['type'] == 'python':
                if len(next_chart_id_list) == 1:
                    file_content += code_space + "data['chart_id_to'] = '" + next_chart_id_list[0] + "'\n"
                else:
                    file_content += code_space + "data['chart_id_to'] = ''\n"
                file_content += code_space + "if load_balance:\n"
                code_space += "    "
                file_content += code_space + "try:\n"
                code_space += "    "
                file_content += code_space + "from ommonitor.views import sendPython\n"
                file_content += code_space + "sendPython(flow_uuid, data, chart_file)\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except:\n"
                code_space += "    "
                file_content += code_space + "OmEngine(flow_uuid,data).checkActive()\n"
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "else:\n"
                code_space += "    "
                file_content += code_space + "OmEngine(flow_uuid,data).checkActive()\n"
                code_space = code_space.replace("    ", "", 1)
            else:
                if len(next_chart_id_list) == 1:
                    file_content += code_space + "data['chart_id_to'] = '" + next_chart_id_list[0] + "'\n"
                    file_content += code_space + "OmEngine(flow_uuid,data).checkActive()\n"
                elif len(next_chart_id_list) == 0:
                    file_content += code_space + "data['chart_id_to'] = ''\n"
                    file_content += code_space + "OmEngine(flow_uuid,data).checkActive()\n"
                else:
                    file_content += code_space + "data_str = json.dumps(data)\n"
                    for next_chart_id in next_chart_id_list:
                        file_content += code_space + "data_"+next_chart_id+" = json.loads(data_str)\n"
                        file_content += code_space + "data_"+next_chart_id+"['chart_id_to'] = '" + next_chart_id + "'\n"
                        file_content += code_space + "OmEngine(flow_uuid,data_"+next_chart_id+").checkActive()\n"
            code_space = code_space.replace("    ", "", 1)
        #write the code into main.py
        file_mainpy = os.path.join(file_path, "main.py")
        f=open(file_mainpy,"w+", encoding='UTF-8')
        f.write(file_content)
        f.close()
        return True
    except Exception as e:
        debug(e.__str__())
        return False


#SLA
@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def createSLARuleAjax(request):
    '''
    create sla rule.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    result = {}
    require_field = ['sla_name','app_name','flow_name','flow_uuid','type','target','remind','violation']
    #server side rule check
    postdata = getPostdata(request)
    sla_data = json.loads(postdata.get('SLA_data','{}'))
    data_checker = DataChecker(sla_data, require_field)
    field_list = ['sla_name','description','app_name','flow_name','flow_uuid','type','target','remind','violation','advanced','timer_start','timer_end','title','content','notify_createuser','notify_group','notify_user']
    update_dict = {}
    for key in field_list:
        value = sla_data.get(key,'')
        if isinstance(value, dict) or isinstance(value, list):
            update_dict[key] = json.dumps(value)
        else:
            update_dict[key] = value
    if data_checker.get('status') == 'success':
        same_name = SLARule.objects.filter(sla_name=update_dict['sla_name']).exists()
        if not same_name:
            SLARule.objects.create(**update_dict)
            info(request ,'%s create sla rule success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('建立成功。'), result).returnJSON()
        else:
            info(request ,'%s create sla rule error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, _('重複名稱。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def updateSLARuleAjax(request):
    '''
    update sla rule.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    result = {}
    require_field = ['sla_id']
    #server side rule check
    postdata = getPostdata(request)
    sla_data = json.loads(postdata.get('SLA_data','{}'))
    data_checker = DataChecker(sla_data, require_field)
    sla_id = sla_data.get('sla_id','')
    field_list = ['sla_name','description','app_name','flow_name','flow_uuid','type','target','remind','violation','advanced','timer_start','timer_end','title','content','notify_createuser','notify_group','notify_user']
    update_dict = {}
    for key in sla_data:
        if key in field_list:
            value = sla_data.get(key,'')
            if isinstance(value, dict) or isinstance(value, list):
                update_dict[key] = json.dumps(value)
            else:
                update_dict[key] = value
    if data_checker.get('status') == 'success':
        same_name = SLARule.objects.filter(sla_name=update_dict['sla_name']).exclude(id=sla_id).exists()
        if not same_name:
            SLARule.objects.filter(id=sla_id).update(**update_dict)
            info(request ,'%s update sla rule success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('更新成功。'), result).returnJSON()
        else:
            info(request ,'%s update sla rule error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, _('重複名稱。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def deleteSLARuleAjax(request):
    '''
    delete sla rule.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    result = {}
    require_field = ['sla_id']
    #server side rule check
    postdata = getPostdata(request)
    data_checker = DataChecker(postdata, require_field)
    sla_id = postdata.get('sla_id','')
    if data_checker.get('status') == 'success':
        SLARule.objects.filter(id__in=sla_id).delete()
        info(request ,'%s delete sla rule success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('建立成功。'), result).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def loadSLARuleAjax(request):
    '''
    load sla rule.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    postdata = getPostdata(request)
    sla_id = postdata.get('sla_id','')
    sla_name = postdata.get('sla_name','')
    if sla_id:
        result = list(SLARule.objects.filter(id=sla_id).values())[0]
    else:
        result = list(SLARule.objects.filter(sla_name=sla_name).values())[0]
    if result:
        info(request ,'%s load sla rule success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result[0]).returnJSON()
    else:
        info(request ,'%s load sla rule error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, _('查詢失敗。')).returnJSON()


@login_required
@permission_required('omformflow.OmFormFlow_Manage','/api/permission/denied/')
@try_except
def listSLARuleAjax(request):
    '''
    list sla rule.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['sla_name__icontains','app_name__icontains','flow_name__icontains']
    query = ''
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable', None)
    sla_type = postdata.get('type','num')
    if datatable:
        query = SLARule.objects.filterformat(type=sla_type)
        result = DatatableBuilder(request, query, field_list)
        data = result['data']
        if isinstance(data, dict):
            for key in data:
                row = data[key]
                for key in ['target', 'remind', 'violation', 'advanced', 'notify_user', 'notify_group','timer_start','timer_end']:
                    row[key] = json.loads(row[key])
        elif isinstance(data, list):
            for row in data:
                for key in ['target', 'remind', 'violation', 'advanced', 'notify_user', 'notify_group','timer_start','timer_end']:
                    row[key] = json.loads(row[key])
        info(request ,'%s list sla rule success.' % request.user.username)
        return JsonResponse(result)
    else:
        #目前尚無功能使用
        result = list(SLARule.objects.filterformat('id','sla_name',type=sla_type))
        info(request ,'%s list sla rule success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()


def checkSLARule(flow_uuid, data_id, omdata_object=None):
    '''
    資料寫入時，檢查SLA規則是否符合
    '''
    try:
        if check_app('ommonitor'):
            sla_list = list(SLARule.objects.filter(flow_uuid=flow_uuid).values())
            if sla_list:
                model = getModel('omformmodel', 'Omdata_' + flow_uuid)
                omdata_obj = model.objects.get(id=data_id)
                omdata = omdata_obj.__dict__
                #取得flow_name
                fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                flow_name = fa.flow_name
                #取得app_name
                app_id = fa.flow_app_id
                app_name_dict = FlowActiveGlobalObject.appname_dict
                app_name = ''
                for key in app_name_dict:
                    if str(app_name_dict[key]) == str(app_id):
                        app_name = key
                        break
                
                delete_sladata_list = []
                for sla in sla_list:
                    try:
                        trigger_SLA = False
                        param = {}
                        sla_type = sla['type']
                        #數值測量
                        if sla_type == 'num':
                            #進階條件計算
                            ad_res = evalMutiCons(sla['advanced'], omdata, True)
                            #判斷是否需要開單
                            target = json.loads(sla['target'])
                            field_value = getEvalFieldValue(target['id'], omdata)
                            violation = json.loads(sla['violation'])
                            v = eval("lambda : " + buildEvalString(field_value, violation['rule'], violation['value']))()
                            if v:
                                if ad_res:
                                    param['title'] = _('[違反] ') + sla['title']
                                    trigger_SLA = True
                                    level = 'red'
                                    critical = 5
                            else:
                                remind = json.loads(sla['remind'])
                                r = eval("lambda : " + buildEvalString(field_value, remind['rule'], remind['value']))()
                                if r:
                                    if ad_res:
                                        param['title'] = _('[提醒] ') + sla['title']
                                        trigger_SLA = True
                                        level = 'yellow'
                                        critical = 3
                            if trigger_SLA:
                                #建立或更新sla data
                                create_event = False
                                sla_data_list = SLAData.objects.filter(sla_id=sla['id'],data_no=omdata['data_no'])
                                if sla_data_list:
                                    sla_data = sla_data_list[0]
                                    if sla_data.level != level:
                                        sla_data_list.update(level=level)
                                        create_event = True
                                else:
                                    create_event = True
                                    SLAData.objects.create(sla_id=sla['id'],type=sla_type,app_name=app_name,\
                                                           flow_name=flow_name,data_no=omdata['data_no'],\
                                                           level=level)
                                if create_event:
                                    #組合開event的內容
                                    url = 'http://' + settings.LOCAL_IP + ':' + settings.LOCAL_PORT + '/my-mission/page/myform/' + flow_uuid + '/' + str(omdata['data_no'])
                                    param['content'] = sla['content'] + '\n' + url
                                    param['critical'] = critical
                                    param['source'] = 'sla'
                                    param['source2'] = sla['sla_name'] + '<' + app_name + '><' + flow_name + '><' + str(omdata['data_no']) + '>'
                                    users = ''
                                    if sla['notify_createuser']:
                                        users += omdata_obj.create_user.email
                                        
                                    notify_group = json.loads(sla['notify_group'])
                                    if notify_group:
                                        group_user_list = list(OmUser.objects.filter(groups__id__in=notify_group).values_list('email',flat=True))
                                        for i in group_user_list:
                                            users += ';' + i
                                    notify_user = json.loads(sla['notify_user'])
                                    if notify_user:
                                        user_list = list(OmUser.objects.filter(id__in=notify_user).values_list('email',flat=True))
                                        for i in user_list:
                                            users += ';' + i
                                    param['users'] = users
                                    createEvent(param)
                            else:
                                delete_sladata_list.append(sla['id'])
                        #時間測量
                        else:
                            ts_res = evalMutiCons(sla['timer_start'], omdata, True)
                            if ts_res:
                                s = SLAData.objects.filter(sla_id=sla['id'],data_no=omdata['data_no'])
                                if not s:
                                    SLAData.objects.create(sla_id=sla['id'],type=sla_type,app_name=app_name,\
                                                           flow_name=flow_name,data_no=omdata['data_no'],\
                                                           level='green',remind=sla['remind'],violation=sla['violation'])
                            te_res = evalMutiCons(sla['timer_end'], omdata, False)
                            if te_res:
                                closeSLAData(flow_uuid, omdata['data_no'])
                    except Exception as e:
                        pass
                #刪除變成綠燈的sla資料（數值測量）
                SLAData.objects.filter(sla_id__in=delete_sladata_list,data_no=omdata['data_no']).delete()
                #更新燈號
                level_list = list(SLAData.objects.filter(app_name=app_name,flow_name=flow_name,data_no=omdata['data_no']).values_list('level',flat=True))
                update_level = 'green'
                for i in level_list:
                    if i == 'red':
                        update_level = i
                        break
                    elif i == 'yellow':
                        update_level = i
                if omdata_obj.level != update_level:
                    update_dict = {}
                    update_dict['level'] = update_level
                    #找到燈號欄位
                    level_id = None
                    items = json.loads(fa.merge_formobject)
                    for key in items:
                        item = items[key]
                        if item['type'] == 'h_level':
                            level_id = item['id'].lower()
                            break
                    if level_id:
                        update_dict[level_id] = update_level
                    model.objects.filter(id=data_id).update(**update_dict)
                    if omdata_object:
                        omdata_object.level = update_level
    except Exception as e:
        debug(e.__str__())
    

def evalMutiCons(cons_str, data_dict, result):
    cons = json.loads(cons_str)
    if cons:
        eval_str = "lambda : "
        count = 0
        for con in cons:
            #第一圈不加'and'
            if count:
                eval_str += ' and '
            field_value = getEvalFieldValue(con['id'], data_dict)
            eval_str += buildEvalString(field_value, con['rule'], con['value'])
            count += 1
        result = eval(eval_str)()
    return result


def getEvalFieldValue(field_name, data_dict):
    field_name = field_name.lower()
    if re.match(r'.+-group', field_name):
        field_name = re.findall(r'(.+)-group', field_name)[0]
        group_value = json.loads(data_dict.get(field_name))
        field_value = group_value.get('group','')
    elif re.match(r'.+-user', field_name):
        field_name = re.findall(r'(.+)-user', field_name)[0]
        group_value = json.loads(data_dict.get(field_name))
        field_value = group_value.get('user','')
    else:
        field_value = data_dict.get(field_name,'')
    return field_value

def buildEvalString(param1, rule, param2):
    param1 = str(param1)
    param2 = str(param2)
    if rule in ['=','!=']:
        if rule == '=':
            rule = '=='
        eval_str = "'" + param1 + "'" + rule + "'" + param2 + "'"
    else:
        eval_str = param1 + rule + param2
    return eval_str


def checkSLAData(*args):
    '''
    定期檢查時間測量sla
    '''
    try:
        if check_app('ommonitor'):
            now_time = datetime.now()
            sla_data_list = list(SLAData.objects.filter(type='time',closed=False,level__in=['green','yellow']))
            for sla_data in sla_data_list:
                try:
                    #判斷是否需要開事件
                    param = {}
                    sla = sla_data.sla
                    create_event = False
                    violation = json.loads(sla_data.violation)
                    violation_time = sla_data.createtime + timedelta(minutes=int(violation['value']))
                    if now_time > violation_time:
                        create_event = True
                        level = 'red'
                        param['title'] = _('[違反] ') + sla.title
                        critical = 5
                    else:
                        remind = json.loads(sla_data.remind)
                        remind_time = sla_data.createtime + timedelta(minutes=int(remind['value']))
                        if now_time > remind_time:
                            level = 'yellow'
                            if sla_data.level == 'green':
                                create_event = True
                                param['title'] = _('[提醒] ') + sla.title
                                critical = 3
                    if create_event:
                        #取得omdata
                        fa = FlowActiveGlobalObject.NameSearch(sla_data.flow_name, None, sla_data.app_name)
                        flow_uuid = fa.flow_uuid.hex
                        model = getModel('omformmodel', 'Omdata_' + flow_uuid)
                        omdata_list = model.objects.filter(data_no=sla_data.data_no,history=False)
                        omdata = omdata_list[0]
                        #組合開event的內容
                        url = 'http://' + settings.LOCAL_IP + ':' + settings.LOCAL_PORT + '/my-mission/page/myform/' + flow_uuid + '/' + str(sla_data.data_no)
                        param['content'] = sla.content + '\n' + url
                        param['critical'] = critical
                        param['source'] = 'sla'
                        param['source2'] = sla.sla_name + '<' + sla_data.app_name + '><' + sla_data.flow_name + '><' + str(sla_data.data_no) + '>'
                        users = ''
                        if sla.notify_createuser:
                            users += omdata.create_user.email
                             
                        notify_group = json.loads(sla.notify_group)
                        if notify_group:
                            group_user_list = list(OmUser.objects.filter(groups__id__in=notify_group).values_list('email',flat=True))
                            for i in group_user_list:
                                users += ';' + i
                        notify_user = json.loads(sla.notify_user)
                        if notify_user:
                            user_list = list(OmUser.objects.filter(id__in=notify_user).values_list('email',flat=True))
                            for i in user_list:
                                users += ';' + i
                        param['users'] = users
                        createEvent(param)
                        #更新sla data
                        sla_data.level = level
                        sla_data.save()
                        #更新燈號
                        level_list = list(SLAData.objects.filter(app_name=sla_data.app_name,flow_name=sla_data.flow_name,data_no=omdata.data_no).values_list('level',flat=True))
                        update_level = 'green'
                        for i in level_list:
                            if i == 'red':
                                update_level = i
                                break
                            elif i == 'yellow':
                                update_level = i
                        update_dict = {'level':update_level}
                        #找到燈號欄位
                        level_id = None
                        items = json.loads(fa.merge_formobject)
                        for key in items:
                            item = items[key]
                            if item['type'] == 'h_level':
                                level_id = item['id'].lower()
                                break
                        if level_id:
                            update_dict[level_id] = update_level
                        omdata_list.update(**update_dict)
                        #更改my mission燈號
                        updateMissionLevel(flow_uuid, sla_data.data_no, update_level)
                except:
                    pass
    except Exception as e:
        debug(e.__str__())


def closeSLAData(flow_uuid,data_no):
    try:
        if check_app('ommonitor'):
            fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
            flow_name = fa.flow_name
            #取得app_name
            app_id = fa.flow_app_id
            app_name_dict = FlowActiveGlobalObject.appname_dict
            app_name = ''
            for key in app_name_dict:
                if str(app_name_dict[key]) == str(app_id):
                    app_name = key
                    break
            SLAData.objects.filter(flow_name=flow_name,app_name=app_name,data_no=data_no,closed=False).update(closed=True)
    except:
        pass


@login_required
@try_except
def listSLADataAjax(request):
    '''
    list sla data.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    app_name = postdata.get('app_name', '')
    flow_name = postdata.get('flow_name', '')
    data_no = postdata.get('data_no', '')
    sla_rule_list = list(SLARule.objects.filter(app_name=app_name,flow_name=flow_name).values('id','sla_name','description'))
    sla_data_list = list(SLAData.objects.filter(app_name=app_name,flow_name=flow_name,data_no=data_no).values('sla_id','level','createtime'))
    sla_data_dict = {}
    for sla_data in sla_data_list:
        sla_data_dict[sla_data['sla_id']] = {'level':sla_data['level'], 'createtime':sla_data['createtime']}
    for sla_rule in sla_rule_list:
        sla_id = sla_rule['id']
        data_mapping = sla_data_dict.get(sla_id,{})
        sla_rule['level'] = data_mapping.get('level','green')
        sla_rule['createtime'] = data_mapping.get('createtime',None)
    info(request ,'%s list sla data success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('讀取成功。'), sla_rule_list).returnJSON()


