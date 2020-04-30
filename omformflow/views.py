import uuid, os, json, shutil, time, re
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, permission_required
from omflow.syscom.schedule_monitor import schedule_Execute, cancelScheduleJob
from omflow.syscom.common import try_except, DataChecker, DatatableBuilder, getModel, FormDataChecker, FormatToFormdataList
from omflow.syscom.message import ResponseAjax, statusEnum
from omflow.global_obj import GlobalObject, FlowActiveGlobalObject
from omflow.models import SystemSetting, Scheduler, TempFiles
from omuser.views import addPermissionToRole
from omformflow.models import FlowWorkspace, FlowActive, WorkspaceApplication, ActiveApplication, OmdataFiles
from django.http.response import JsonResponse
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datetime import datetime
from omformmodel.views import OMFormModel
from omflow.syscom.omengine import OmEngine
from omflow.syscom.license import getApps, getRepository
from ommission.views import setMission
from ommission.models import Missions
from django.db.models import Q
from omflow.syscom.default_logger import info,debug,error


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
def scheduleflowManagePage(request):
    return render(request, 'scheduleflow_manage.html')


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
    postdata = request.POST
    data_checker = DataChecker(postdata, require_field)
    if data_checker.get('status') == 'success':
        #get post data
        app_name = postdata.get('app_name','')
        action = postdata.get('action','')
        app_id_list = postdata.getlist('app_id_list[]','')
        if action == 'create':
            if app_name:
                try:
                    updatetime = datetime.now()
                    WorkspaceApplication.objects.create(app_name=app_name,updatetime=updatetime,user=request.user,app_attr='user')
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
    postdata = request.POST
    datatable = postdata.get('datatable', None)
    if datatable:
        #function variable
        field_list=['app_name__icontains','user__username__icontains','active_app_name__icontains']
        query = ''
        app_attr = postdata.getlist('app_attr[]',['user','cloud','lib'])
        updatetime = postdata.get('updatetime','')
        display_field =['id','app_name','app_attr','updatetime','active_app_name','user__username']
        query = WorkspaceApplication.objects.filterformat(*display_field,app_attr__in=app_attr,updatetime__lte=updatetime)
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list WorkspaceApplication success.' % request.user.username)
        return JsonResponse(result)
    else:
        result = list(WorkspaceApplication.objects.filterformat('id','app_name'))
        info(request ,'%s list WorkspaceApplication success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功'), result).returnJSON()
    

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
    require_field = ['app_id_list[]']
    result = {}
    #get post data
    postdata = request.POST
    app_id_list = postdata.getlist('app_id_list[]','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        for app_id in app_id_list:
            app_name = WorkspaceApplication.objects.get(id=app_id).app_name
            fw = list(FlowWorkspace.objects.filter(flow_app_id=app_id).values('flow_name','flowobject','config','flow_app_id__app_name'))
            for f in fw:
                f['flowobject'] = json.loads(f['flowobject'])
                f['config'] = json.loads(f['config']) 
            result[app_name] = fw
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
    status = True
    message = ''
    app_id_list = []
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    app_list = json.loads(postdata.get('app_list'))
    if checker.get('status') == 'success':
        for app_name in app_list:
            try:
                updatetime = datetime.now()
                wa = WorkspaceApplication.objects.create(app_name=app_name,updatetime=updatetime,user=request.user,app_attr='user')
                app_id_list.append(wa.id)
                flow_list = app_list[app_name]
                flow_name_list = []
                for flow in flow_list:
                    if flow['flow_name'] not in flow_name_list:
                        flow_name_list.append(flow['flow_name'])
                        flow['app_id'] = wa.id
                        flow['formobject'] = json.dumps(flow['flowobject'].get('form_object',''))
                        flow['flowobject'] = json.dumps(flow['flowobject'])
                        flow['config'] = json.dumps(flow['config'])
                        result = createFlowWorkspace(flow, request.user)
                        if not result:
                            status = False
                            message += _('流程建立失敗。')
                            break
                    else:
                        status = False
                        message += _('同應用內不可有重複的流程名稱。')
                        break
            except Exception as e:
                if 'unique constraint' in e.__str__():
                    message += _('重複應用名稱：') + app_name + '   '
                status = False
            if not status:
                break
        if status:
            info(request ,'%s import WorkspaceApplication success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('匯入成功。')).returnJSON()
        else:
            try:
                WorkspaceApplication.objects.filter(id__in=app_id_list).delete()
            except:
                pass
            info(request ,'%s export WorkspaceApplication error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, message).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


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
    postdata = request.POST
    data_checker = DataChecker(postdata, require_field)
    if data_checker.get('status') == 'success':
        result = createFlowWorkspace(postdata, request.user)
        if result:
            info(request ,'%s create FlowWorkspace success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('建立成功'), result).returnJSON()
        else:
            info(request ,'%s create FlowWorkspace error.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('建立失敗')).returnJSON()
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
        subflow_obj = {}
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
    postdata = request.POST
    flow_uuid = postdata.get('flow_uuid','')
    if flow_uuid:
        fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
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
    postdata = request.POST
    app_id = postdata.get('app_id','')
    flow_name = postdata.get('flow_name','')
    if flow_name:
        fw = FlowWorkspace.objects.get(flow_name=flow_name,flow_app_id=app_id)
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
    result = {}
    subflow = []
    fw_obj = {}
    require_field = ['flow_name','flow_id']
    field_list = ['flow_name','description','formobject','flowobject','config']
    #server side rule check
    postdata = request.POST
    data_checker = DataChecker(postdata, require_field)
    if data_checker.get('status') == 'success':
        #get post data
        flowobject = postdata.get('flowobject','')
        config = postdata.get('config','')
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
        flow_id = postdata.get('flow_id','')
        for i in field_list:
            fw_obj[i] = postdata.get(i,'')
        fw_obj['subflow'] = json.dumps(subflow)
        fw_obj['updatetime'] = datetime.now()
        FlowWorkspace.objects.filter(id=flow_id).update(**fw_obj)
        result['flow_id'] = flow_id
        info(request ,'%s update FlowWorkspace success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('更新成功。'), result).returnJSON()
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
    postdata = request.POST
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
    postdata = request.POST
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
    require_field = ['flow_id[]']
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id_list = postdata.getlist('flow_id[]','')
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
    require_field = ['flow_id[]','app_id']
    display_field = ['flow_name','formobject','flowobject','config','subflow','create_user_id','createtime','updatetime']
    flow_name_list = []
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id_list = postdata.getlist('flow_id[]','')
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
    postdata = request.POST
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
    license_app_num = getApps('')
    #function variable
    require_field = ['w_app_id']
    all_success = True
    flow_mapping = {}
    #get post data
    postdata = request.POST
    lside_pid = postdata.get('lside_pid','')
    w_app_id = postdata.get('w_app_id','')
    app_name = postdata.get('app_name','')
    a_app_id = postdata.get('a_app_id','')
    now_app_num = ActiveApplication.objects.filter(undeploy_flag=False).count()
    now_app_num = now_app_num - 1
    if now_app_num < license_app_num:
        #server side rule check
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            #建立app
            caa_result = createActiveApplication(w_app_id, app_name, a_app_id, request.user)
            if caa_result['status']:
                new_app_id = caa_result['app_id']
                new_app_name = caa_result['app_name']
                undeploy_list = caa_result['undeploy_list']
                a_app_id = caa_result['a_app_id']
                #建立舊流程與新流程的對應關係
                fw_list = list(FlowWorkspace.objects.filterformat('id','flow_name',flow_app_id=w_app_id))
                if a_app_id:
                    fa_list = list(FlowActive.objects.filter(flow_app_id=a_app_id,parent_uuid=None).values('flow_uuid','flow_name'))
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
                    cfa_result = createFlowActive(new_app_id, flow_id, flow_mapping[flow_id], caa_result['version'], request.user)
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
                    #建立側邊選單
                    if lside_pid == 'disable':
                        flow_uuid_list = []
                        for flow in flow_list:
                            flow_uuid_list.append(flow['flow_uuid'])
                        lside_pid = removeSidebar(flow_uuid_list, a_app_id)
                    createSidebar(flow_list, new_app_id, new_app_name, lside_pid)
                    return ResponseAjax(statusEnum.success, _('部署成功。')).returnJSON()
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
                    info(request ,'%s deploy FlowWorkspace error.' % request.user.username)
                    return ResponseAjax(statusEnum.not_found, _('部署失敗。')).returnJSON()
            else:
                info(request ,'%s deploy WorkspaceApplication error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, caa_result.get('message','')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s the license error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, _('應用流程數量已達上限，請向原廠購買授權。')).returnJSON()


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
                version = int(aa.version) + 1
                app_name = aa.app_name
                wa.active_app_name = app_name
                wa.save()
                if aa.undeploy_flag == False:
                    result['undeploy_list'] = undeployActiveApplication(a_app_id, user)
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
        #delete global
        FlowActiveGlobalObject.deleteAppNameDict(aa.app_name)
        aa.undeploy_flag = True
        aa.updatetime = datetime.now()
        aa.user = user
        aa.save()
        flow_id_list = list(FlowActive.objects.filter(flow_app_id=app_id,parent_uuid=None).values_list('id',flat=True))
        undeployFlow(flow_id_list)
        return flow_id_list
    except Exception as e:
        debug(e.__str__())
        return []


def createFlowActive(new_app_id, flowworkspace_id, flow_uuid, version, user):
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
        tf_list = ['fp_show','attachment','relation','worklog','history']
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
            active_obj[tf] = config.get(tf)
        #取得快速操作設定
        action1 = {}
        action2 = {}
        flow_items = json.loads(fw.flowobject)['items']
        for item in flow_items:
            if item['type'] == 'form':
                config = item['config']
                if config['action1']:
                    action1[item['id']] = {'text':config['action1_text'], 'input':config['input1']}
                if config['action2']:
                    action2[item['id']] = {'text':config['action2_text'], 'input':config['input2']}
        if action1:
            active_obj['action1'] = json.dumps(action1)
        if action2:
            active_obj['action2'] = json.dumps(action2)
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
            subflow = json.loads(fw.subflow)
            if len(subflow):
                for sb_d in subflow:
                    sb_flow_uuid = uuid.uuid4().hex
                    sb_flow_uuid_list = []
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
                for sb_d in subflow:
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
        for item in sidebar_design:
            if item['id'] == lside_pid:
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
    postdata = request.POST
    datatable = postdata.get('datatable',None)
    flow_app_id = postdata.get('app_id','')
    if datatable:
        deploytime = postdata.get('deploytime','')
        is_active = postdata.getlist('is_active[]',['1','0'])
        undeploy_flag = postdata.getlist('undeploy_flag[]', ['0'])
        query = FlowActive.objects.filter(flow_app_id=flow_app_id,undeploy_flag__in=undeploy_flag,parent_uuid=None,deploytime__lte=deploytime,is_active__in=is_active).values('id','flow_uuid','flow_name','deploytime','version','is_active','description','flowlog','api','undeploy_flag')
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list FlowActive success.' % request.user.username)
        return JsonResponse(result)
    else:
        display_field = ['id','flow_uuid','flow_name']
        if flow_app_id:
            result = list(FlowActive.objects.filterformat(*display_field,flow_app_id=flow_app_id,undeploy_flag=False,parent_uuid=None))
        else:
            result = []
        info(request ,'%s list FlowActive success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('查詢成功'), result).returnJSON()


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
    require_field = ['field','flow_id']
    status = True
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id = postdata.get('flow_id','')
    action_field = postdata.get('field','')
    if checker.get('status') == 'success':
        try:
            flowactive = FlowActiveGlobalObject.IDSearch(flow_id)
#                 flowactive = FlowActive.objects.get(id=flow_id)
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
                display_field_dict = json.loads(display_field)
                keys = list(display_field_dict.keys())
                if 'error' in keys and 'error_message' in keys:
                    flowactive.display_field = display_field
                else:
                    status = False
            if status:
                flowactive.save()
                info(request ,'%s update FlowActive success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('設定成功')).returnJSON()
            else:
                info(request ,'%s update FlowActive error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, _('設定失敗。')).returnJSON()
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
    require_field = ['id[]','active']
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id_list = postdata.getlist('id[]','')
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
        return ResponseAjax(statusEnum.success, _('設定成功')).returnJSON()
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
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    schedule_id_list = postdata.getlist('schedule_id[]','')
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
            return ResponseAjax(statusEnum.success, _('設定成功')).returnJSON()
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
        cycle_date = postdata.getlist('cycle_date[]',[])
        formdata = postdata.get('formdata','')
        if flow_id and flow_uuid:
            exec_fun = {'module_name':'omflow.syscom.schedule_monitor','method_name':'put_flow_job'}
            input_param['module_name'] = module_name
            input_param['method_name'] = method_name
            input_param['flow_uuid'] = flow_uuid
            input_param['formdata'] = formdata
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
    postdata = request.POST
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
            return ResponseAjax(statusEnum.success, _('設定成功')).returnJSON()
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
    postdata = request.POST
    is_active = postdata.getlist('is_active[]',['1','0'])
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
            record['input_param'] = json.loads(record['input_param'])['formdata']
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
            datas[key]['input_param'] = json.loads(datas[key]['input_param'])['formdata']
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
    #function variable
    require_field = ['app_id']
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    app_id = postdata.get('app_id','')
    if checker.get('status') == 'success':
        flow_id_list = undeployActiveApplication(app_id, request.user)
        flow_uuid_list = list(FlowActive.objects.filter(id__in=flow_id_list).values_list('flow_uuid',flat=True))
        new_flow_uuid_list = []
        for i in flow_uuid_list:
            new_flow_uuid_list.append(i.hex)
        removeSidebar(new_flow_uuid_list, app_id)
        info(request ,'%s undeploy ActiveApplication success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('下線成功')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


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
    postdata = request.POST
    lside_pid = postdata.get('lside_pid','')
    new_app_id = postdata.get('new_app_id','')
    ex_app_id = postdata.get('ex_app_id','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        try:
            if ex_app_id:
                ex_aa = ActiveApplication.objects.get(id=ex_app_id)
                if not ex_aa.undeploy_flag:
                    #下架現有流程
                    flow_id_list = undeployActiveApplication(ex_app_id, request.user)
                    flow_uuid_list = list(FlowActive.objects.filter(id__in=flow_id_list).values_list('flow_uuid',flat=True))
                    new_flow_uuid_list = []
                    for i in flow_uuid_list:
                        new_flow_uuid_list.append(i.hex)
                    #移除側邊選單
                    removeSidebar(new_flow_uuid_list, ex_app_id)
                else:
                    status = False
            if status:
                #重新上架應用
                aa = ActiveApplication.objects.get(id=new_app_id)
                aa.undeploy_flag = False
                aa.save()
                FlowActiveGlobalObject.setAppNameDict(aa.app_name, aa.id)
                #重新上架流程
                flow_list = list(FlowActive.objects.filterformat('id','flow_uuid','flow_name',flow_app_id=aa.id))
                for fa in flow_list:
                    flow_id = fa['id']
                    redeployFlow(flow_id)
                #重新建立側邊選單
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
    postdata = request.POST
    datatable = postdata.get('datatable',None)
    if datatable:
        #function variable
        field_list=['app_name__icontains','user_id__username__icontains']
        query = ''
        #get post data
        postdata = request.POST
        app_attr = postdata.getlist('app_attr[]',['user','cloud','lib'])
        updatetime = postdata.get('updatetime','')
        undeploy_flag = postdata.getlist('undeploy_flag[]',['0'])
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
            result = list(ActiveApplication.objects.filterformat('id','app_name',undeploy_flag=False))
        info(request ,'%s list ActiveApplication success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('查詢成功'), result).returnJSON()


def getCloudFlowAjax(request):
    result = getRepository('')
    return ResponseAjax(statusEnum.success, _('查詢成功'), result).returnJSON()
    
    
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
        debug(e.__str__())
        status = False
        message = e.__str__()
    finally:
        result['status'] = status
        result['message'] = message
        return result


def removeSidebar(flow_uuid_list,app_id):
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
            if item['flow_uuid'] in flow_uuid_list:
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
    #get post data
    postdata = request.POST
    flow_uuid = postdata.get('flow_uuid','')
    if request.user.has_perm('omformmodel.Omdata_' + flow_uuid + '_Add') or request.user.has_perm('omformflow.OmFormFlow_Manage'):
        #server side rule check
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            try:
                fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                flowobject = json.loads(fa.flowobject)
                result['flow_name'] = fa.flow_name
                result['formobject'] = fa.formobject
                result['attachment'] = fa.attachment
                result['start_input'] = []
                if fa.formcounter == '0':
                    items = flowobject['items']
                    for i in items:
                        if i['type'] == 'start':
                            result['start_input'] = i['config']['input']
                            break
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
    postdata = request.POST
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
    require_field = ['app_id_list[]']
    app = {}
    #get post data
    postdata = request.POST
    app_id_list = postdata.getlist('app_id_list[]','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        try:
            for app_id in app_id_list:
                flow_list = []
                app_name = ActiveApplication.objects.get(id=app_id).app_name
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
                    config['title_field'] = flowactive['title_field']
                    config['status_field'] = flowactive['status_field']
                    config['display_field'] = flowactive['display_field']
                    config['search_field'] = flowactive['search_field']
                    config['subflow'] = subflow
                    config['permission'] = flowactive['permission']
                    flow['flow_name'] = flowactive['flow_name']
                    flow['description'] = flowactive['description']
                    flow['flowobject'] = json.loads(flowactive['flowobject'])
                    flow['config'] = config
                    flow_list.append(flow)
                app[app_name] = flow_list
            info(request ,'%s export ActiveApplication success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('匯出成功。'), app).returnJSON()
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
    postdata = request.POST
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
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        if action == 'update':
            if checkOmDataPermission(request.user, postdata.get('flow_uuid',''), postdata.get('data_id',''), '_Modify'):
                result = updateOmData(postdata, request.user.username)
            else:
                per = False
        elif action == 'delete':
            if request.user.has_perm('omformmodelOmdata_' + flow_uuid + '_Delete'):
                result = deleteOmData(postdata, request.user.username)
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
                info(request ,'%s edit OmData success.' % request.user.username)
                return ResponseAjax(statusEnum.success, result['message']).returnJSON()
            else:
                info(request ,'%s edit OmData error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
        else:
            info(request ,'%s has no permission.' % request.user.username)
            return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
    else:
        info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    

def checkOmDataPermission(user, flow_uuid, data_id, per_type):
    '''
    檢查使用者是否有編輯權限，或是該使用者為該單的受派人
    '''
    try:
        result = False
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        omdata = omdata_model.objects.get(id=data_id)
        group = omdata.group
        if group:
            group = json.loads(group)
        user_groups = list(user.groups.all().values_list('id',flat=True))
        if user.has_perm('omformmodel.Omdata_' + flow_uuid + per_type):
            result = True
        elif group:
            if group['user'] == str(user.id):
                result = True
            elif int(group['group']) in user_groups and not group['user']:
                result = True
        elif user.is_superuser:
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
    form_pass = True
    message = ''
    status = False
    formdata = {}
    #get postdata
    flow_uuid = param.get('flow_uuid','')
    outflow_content = json.loads(param.get('outflow_content','{}'))
    start_input = json.loads(param.get('start_input','{}'))
    formdata_list = param.get('formdata','')
    if formdata_list:
        formdata_list = json.loads(formdata_list)
        for item in formdata_list:
            item_id = item['id'].lower()
            value = item['value']
            if isinstance(value, dict):
                new_value = json.dumps(value)
            elif isinstance(value, list):
                new_value = json.dumps(value)
            elif isinstance(value, str):
                new_value = value
            elif value == None:
                new_value = ''
            else:
                new_value = str(value)
            formdata[item_id] = new_value
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
                    message = _('開單失敗：') + omengine_result
                else:
                    message = _('開單成功。')
                    status = True
        else:
            message = _('該流程目前為停用狀態。')
    except ObjectDoesNotExist:
        message = _('該流程沒有已部署的版本')
    except Exception as e:
        message = e.__str__()
    finally:
        result['message'] = message
        result['status'] = status
        debug(message)
        return result
    
 
def updateOmData(param,user='system'):
    '''
    update ticket.
    input: param,user
    return: json
    author: Kolin Hsu
    '''
    #function variable
    result = {}
    formdata = {}
    message = ''
    status = False
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
                    flowactive = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                    #check this flow is active
                    if flowactive.is_active:
                        stop_uuid = omdata.stop_uuid.split('-')[-1]
                        flowobject = json.loads(flowactive.flowobject)
                        flowobject_items = flowobject['items']
                        for item in flowobject_items:
                            if item['id'] == stop_uuid:
                                if item['type'] == 'form':
                                    is_form = True
                                    if not item['config']['form_object']:
                                        formobject = json.loads(flowactive.formobject)
                                    else:
                                        if isinstance(item['config']['form_object'], dict):
                                            formobject = item['config']['form_object']
                                        elif isinstance(item['config']['form_object'], str):
                                            formobject = json.loads(item['config']['form_object'])
                                    items = formobject['items']
                                else:
                                    is_form = False
                        if is_form:
                            #把快速操作的輸入組合成formdata_list格式
                            if quick_action:
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
                                        elif '$' in value:
                                            input_value = flow_value.get(value[2:-1],'')
                                        elif '#' in value:
                                            table_field = value[2:-1].lower()
                                            input_value = omdata_dict[table_field]
                                        else:
                                            input_value = value
                                        #確認填入的欄位類型
                                        for item in items:
                                            if item['id'] == name:
                                                FormatToFormdataList(item, input_value, quick_formdata_list)
                                                break
                                    #把表單中的欄位值都帶入formdata_list
                                    for item in items:
                                        if item['id'][:8] == 'FORMITM_' and item['id'] not in action_input_name_list:
                                            omdata_value = omdata_dict.get(item['id'].lower(),'')
                                            FormatToFormdataList(item, omdata_value, quick_formdata_list)
                                    formdata_list = json.dumps(quick_formdata_list)
                            #組合formdata
                            if formdata_list:
                                formdata_list = json.loads(formdata_list)
                                for item in formdata_list:
                                    item_id = item['id'].lower()
                                    value = item['value']
                                    if isinstance(value, dict):
                                        new_value = json.dumps(value)
                                    elif isinstance(value, list):
                                        new_value = json.dumps(value)
                                    elif isinstance(value, str):
                                        new_value = value
                                    elif value == None:
                                        new_value = ''
                                    else:
                                        new_value = str(value)
                                    formdata[item_id] = new_value
                            if formdata:
                                #check the required field have value in postdata
                                item_list = formobject.get('items',[])
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
                                    #update omdata
                                    omdata_model.objects.filter(id=data_id).update(**formdata)
                                    #set mission history
                                    setMission('history', flow_uuid, None, data_id, user)
                                    #om engine
                                    data = json.loads(omdata_dict['data_param'])
                                    data['data_id'] = data_id
                                    data['chart_id_from'] = None
                                    data['error'] = False
                                    omengine_result = OmEngine(flow_uuid, data).checkActive()
                                    if omengine_result:
                                        message = _('更新失敗：') + omengine_result
                                    else:
                                        message = _('更新成功。')
                                        status = True
                                else:
                                    message = _('缺少必填欄位。')
                            else:
                                if quick_action:
                                    message = _('因流程版本更新，此操作無法執行。')
                                else:
                                    message = _('表單錯誤。')
                        else:
                            message = _('該流程目前並未處於人工處理點，無法人工推進流程。')
                    else:
                        message = _('該流程目前為停用狀態。')
                except MultipleObjectsReturned:
                    message = _('該流程有多個已部署的版本，請聯絡系統管理員協助處理。')
                except ObjectDoesNotExist:
                    message = _('該流程沒有已部署的版本')
            else:
                message = _('該單目前為執行狀態，無法進行更新/刪除。')
        else:
            message = _('找不到該資料庫：Omdata_')+flow_uuid
    except Exception as e:
        debug(e.__str__())
        message = _('找不到該筆資料，或是該筆資料已經關閉。')
    finally:
        result['message'] = message
        result['status'] = status
        return result
    

def deleteOmData(param,user='system'):
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
                message = _('刪除成功。')
                status = True
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
    postdata = request.POST
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    if checkOmDataPermission(request.user, flow_uuid, data_id, '_Modify'):
        uploadOmdataFiles(files, flow_uuid, data_no, data_id, request.user.username)
        info(request ,'%s upload OmData file success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('上傳成功。')).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


def uploadOmdataFiles(files, flow_uuid, data_no, data_id, user):
    try:
        #儲存上傳的檔案
        OmdataFiles.objects.bulk_create([OmdataFiles(flow_uuid=flow_uuid,data_no=data_no,data_id=data_id,file=file,size=file.size,file_name=file.name,upload_user_id=user) for file in files])
        #修改mission
        Missions.objects.filter(flow_uuid=flow_uuid,data_no=data_no,attachment=False).update(attachment=True)
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
    postdata = request.POST
    flow_uuid = postdata.get('flow_uuid','')
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    if checkOmDataPermission(request.user, flow_uuid, data_id, '_View'):
        field = ['id','file','size','delete','createtime','file_name']
        if data_id:
            files = list(OmdataFiles.objects.filterformat(*field,flow_uuid=flow_uuid,data_no=data_no,data_id=data_id))
        else:
            files = list(OmdataFiles.objects.filterformat(*field,flow_uuid=flow_uuid,data_no=data_no).order_by('-createtime'))
        for file in files:
            file_path = os.path.join(settings.MEDIA_ROOT, file['file'])
            if not file['delete'] and not os.path.exists(file_path):
                file['delete'] = True
                delete_id_list.append(file['id'])
        if delete_id_list:
            OmdataFiles.objects.filter(id__in=delete_id_list).update(delete=True)
        info(request ,'%s load OmData file success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), files).returnJSON()
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
    default_field = ['data_no','status','error','error_message','stop_chart_text','updatetime','create_user_id']
    require_field = ['flow_id']
    result = {}
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_id = postdata.get('flow_id','')
    if checker.get('status') == 'success':
        try:
            flowactive = FlowActiveGlobalObject.IDSearch(flow_id)
            flow_uuid = flowactive.flow_uuid.hex
            items = json.loads(flowactive.formobject)['items']
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
                        result[item['id'].lower()] = item['config']['group_title']
                    else:
                        result[item['id'].lower()] = item['config']['title']
            result['display_field'] = flowactive.display_field
#                 result['init_data_id__createtime'] = _('建立時間')
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
    postdata = request.POST
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
    postdata = request.POST
    flow_uuid = postdata.get('flow_uuid','')
    updatetime = postdata.get('updatetime','')
    closed = postdata.getlist('closed[]',[0])
    display_field_list = []
    search_field_list = []
    if request.user.has_perm('omformmodel.Omdata_' + flow_uuid + '_View'):
        #get field setting
        flowactive = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
        display_field_dict = json.loads(flowactive.display_field)
        for key in display_field_dict:
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
    postdata = request.POST
    flow_uuid = postdata.get('flow_uuid','')
    createtime = postdata.get('createtime','')
    closed = postdata.getlist('closed[]',[1,0])
    manage = int(postdata.get('manage',1))
    data_no = postdata.get('data_no','')
    data_id = postdata.get('data_id','')
    if checkOmDataPermission(request.user, flow_uuid, data_id, '_View') or request.user.has_perm('omformflow.OmFormFlow_Manage'):
        if manage:
            display_field = ['data_no','history','stop_uuid','stop_chart_text','error','error_message','createtime','update_user','id']
        else:
            display_field = ['level','status','createtime','update_user','id']
        #get model
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        if data_no:
            query = omdata_model.objects.filter(Q(data_no=data_no) & Q(createtime__lte=createtime) & (Q(history=True) | (Q(history=False) & Q(closed=True)))).values(*display_field)
        else:
            query = omdata_model.objects.filter(closed__in=closed,createtime__lte=createtime).values(*display_field)
        result = DatatableBuilder(request, query, field_list)
        info(request ,'%s list OmDataHistory success.' % request.user.username)
        return JsonResponse(result)
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


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
    json_type_list = ['checkbox','h_group']
    quick_action = None
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    data_id = postdata.get('data_id','')
    if checkOmDataPermission(request.user, flow_uuid, data_id, '_View'):
        if checker.get('status') == 'success':
            try:
                fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid)
                flowobject = json.loads(fa.flowobject)
                formobject = {}
                formdata = []
                config = {'fp_show':fa.fp_show,'worklog':fa.worklog,'history':fa.history,'attachment':fa.attachment,'relation':fa.relation}
                omdata_model = getModel('omformmodel', 'Omdata_' + flow_uuid)
                omdata = omdata_model.objects.get(id=data_id)
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
                                formobject = json.loads(fa.formobject)
                            else:
                                if isinstance(item['config']['form_object'], dict):
                                    formobject = item['config']['form_object']
                                elif isinstance(item['config']['form_object'], str):
                                    formobject = json.loads(item['config']['form_object'])
                        else:
                            formobject = json.loads(fa.formobject)
                        omdata_dict = omdata.__dict__
                        form_items = formobject['items']
                        for form_item in form_items:
                            form_dict = {}
                            item_id = form_item['id'].lower()
                            if item_id[:8] == 'formitm_':
                                if form_item['type'] in json_type_list:
                                    json_value = json.loads(omdata_dict[item_id])
                                else:
                                    json_value = omdata_dict[item_id]
                                form_dict['id'] = form_item['id']
                                form_dict['value'] = json_value
                                form_dict['type'] = form_item['type']
                                formdata.append(form_dict)
                        break
                result = {'formobject':formobject,'formdata':formdata,'config':config, 'flow_name':fa.flow_name, 'quick_action':quick_action, 'files':omdata_files}
                info(request ,'%s load OmData success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
            except:
                info(request ,'%s load OmData error.' % request.user.username)
                return ResponseAjax(statusEnum.not_found, _('找不到該流程。')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


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
    postdata = request.POST
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
    postdata = request.POST
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
                        if omengine_result:
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
    per = False
    #server side rule check
    postdata = request.POST
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_uuid = postdata.get('flow_uuid','')
    flow_name = postdata.get('flow_name','')
    flow_uid = postdata.get('flow_uid','')
    data_no = postdata.get('data_no','')
    flow_level = postdata.get('flow_level','')
    #檢查權限
    user_groups = list(request.user.groups.all().values_list('id',flat=True))
    omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
    omdata = list(omdata_model.objects.filter(data_no=data_no).values_list('group',flat=True))
    for group in omdata:
        if group:
            group = json.loads(group)
            if group['user'] == str(request.user.id):
                per = True
            elif int(group['group']) in user_groups and not group['user']:
                per = True
    if per or request.user.has_perm('omformmodel.Omdata_' + flow_uuid + '_View'):
        if checker.get('status') == 'success':
            try:
                if flow_uid: #子流程
                    fa = FlowActive.objects.filter(parent_uuid=flow_uuid,flow_uid=flow_uid).order_by('deploytime').reverse()[0]
                elif flow_name: #內部流程
                    app_id = FlowActive.objects.filter(flow_uuid=flow_uuid)[0].flow_app_id
                    fa = FlowActive.objects.filter(flow_app_id=app_id,flow_name=flow_name).order_by('deploytime').reverse()[0]
                else: #外部流程或主流程
                    fa = FlowActive.objects.filter(flow_uuid=flow_uuid).order_by('deploytime').reverse()[0]
                inoutput = listFlowInOutput(flow_uuid, data_no, flow_level)
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


def listFlowInOutput(flow_uuid,data_no,flow_level):
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
            else:
                chart_id = stop_uuid[-1]
                his_level = len(stop_uuid)
            if his_level == int(flow_level):
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


def flowMaker(flow_uuid, flowobject, version, subflow_mapping_dict={}):
    '''
    create custom flow python file.
    input: json
    return: boolean
    author: Kolin Hsu
    '''
    try:
        if flowobject.__class__.__name__ == 'str':
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
            if chart['type'] == 'start':
                #start point has nothing to do
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'end':
                #end point has nothing to do
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
                file_content += code_space + "chart_input = data['chart_input']\n"
                file_content += code_space + "chart_input_str = json.dumps(chart_input)\n"
                file_content += code_space + "chart_input_c = json.loads(chart_input_str)\n"
                #get or set chart compile object
                file_content += code_space + "import_error = False\n"
                file_content += code_space + "package = ''\n"
                file_content += code_space + "key = flow_uuid + '_' + chart_id\n"
                file_content += code_space + "compileObj = GlobalObject.__chartCompileObj__.get(key,'')\n"
                file_content += code_space + "if not compileObj:\n"
                code_space += "    "
                file_content += code_space + "chart_file_path = os.path.join(file_path, chart_id + '.py')\n"
                file_content += code_space + "with open(chart_file_path,'r',encoding='UTF-8') as f:\n"
                code_space += "    "
                file_content += code_space + "chart_file = f.read()\n"
                file_content += code_space + "f.close()\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "import_str = ''\n"
                file_content += code_space + "chart_file_to_list = chart_file.split('\\n')\n"
                file_content += code_space + "loop_total_num = 0\n"
                file_content += code_space + "for line in chart_file_to_list:\n"
                code_space += "    "
                file_content += code_space + "line_lstrip = line.lstrip()\n"
                file_content += code_space + "if (line_lstrip[:7] == 'import ') or (line_lstrip[:5] == 'from '):\n"
                code_space += "    "
                file_content += code_space + "import_str += line + '\\n'\n"
                file_content += code_space + "loop_total_num += 1\n"
                code_space = code_space.replace("    ", "", 1)
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "compile_import_str = compile(import_str,'','exec')\n"
                file_content += code_space + "loop = True\n"
                file_content += code_space + "loop_num = 0\n"
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
                file_content += code_space + "loop_num += 1\n"
                file_content += code_space + "import subprocess\n"
                file_content += code_space + "import sys\n"
                file_content += code_space + "package = e.__str__()[17:-1]\n"
                file_content += code_space + "if loop_num > loop_total_num or (not autoinstall):\n"
                code_space += "    "
                file_content += code_space + "import_error = True\n"
                file_content += code_space + "loop = False\n"
                file_content += code_space + "data['error'] = True\n"
                file_content += code_space + "data['error_message'] = e.__str__()\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "else:\n"
                code_space += "    "
                file_content += code_space + "try:\n"
                code_space += "    "
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
                    elif '$' in value1 or '#' in value1:
                        if '$' in value1:
                            value1 = value1[2:-1]
                        else:
                            if re.match(r'#[A-Z][0-9]+\(.+\)', value1):
                                value1 = re.findall(r'#[A-Z][0-9]+\((.+)\)', value1)[0]
                            elif re.match(r'#\(.+\)', value1):
                                value1 = re.findall(r'#\((.+)\)', value1)[0]
                        if value2 == None:
                            file_content += code_space + "if chart_input['" + value1 + "'] " + rule + " '':\n"
                        elif '$' in value2:
                            file_content += code_space + "if chart_input['" + value1 + "'] " + rule + " chart_input['" + value2[2:-1] + "']:\n"
                        elif '#' in value2:
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
                        elif '$' in value2:
                            file_content += code_space + "if '" + value1 + "' " + rule + " chart_input['" + value2[2:-1] + "']:\n"
                        elif '#' in value2:
                            if re.match(r'#[A-Z][0-9]+\(.+\)', value2):
                                value2 = re.findall(r'#[A-Z][0-9]+\((.+)\)', value2)[0]
                            elif re.match(r'#\(.+\)', value2):
                                value2 = re.findall(r'#\((.+)\)', value2)[0]
                            file_content += code_space + "if '" + value1 + "' " + rule + " chart_input['" + value2 + "']:\n"
                        else:
                            file_content += code_space + "if '" + value1 + "' " + rule + " '" + value2 + "':\n"
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
            elif chart['type'] == 'collection':
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'form':
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'sleep':
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'setform':
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'outflow':
                file_content += code_space + "data['error'] = False\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "except Exception as e:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = ''\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
            elif chart['type'] == 'inflow':
                file_content += code_space + "data['error'] = False\n"
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
#             if config['分散運算']:
#                 pass
            if chart['type'] == 'switch':
                file_content += code_space + "if not data['chart_id_to']:\n"
                code_space += "    "
                file_content += code_space + "data['error_message'] = '" + switch_error_message + "'\n"
                file_content += code_space + "data['error'] = True\n"
                code_space = code_space.replace("    ", "", 1)
                file_content += code_space + "OmEngine(flow_uuid,data).checkActive()\n"
            elif chart['type'] == 'subflow':
                file_content += code_space + "OmEngine(data['flow_uuid'],data).checkActive()\n"
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