import json, urllib.request,urllib.parse, ssl, platform, socket, re, uuid, os, time
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, permission_required
from omflow.syscom.common import try_except, DataChecker, DatatableBuilder, getPolicyAttr, getModel, License, getPostdata
from omflow.syscom.message import ResponseAjax, statusEnum
from omflow.syscom.omengine import OmEngine
from omflow.syscom.q_monitor import LoadBalanceMonitor
from omflow.global_obj import FlowActiveGlobalObject, GlobalObject
from omflow.views import checkLicense
from django.conf import settings
from django.http.response import JsonResponse
from omflow.syscom.default_logger import info,debug,error
from ommonitor.models import MonitorApplication, MonitorFlow, Collector, LoadBalanceQueueData, CollectorGroup, EventManagement, PolicyCollector, IncidentRule
from omformflow.models import OmParameter
from ompolicymodel.views import OMPolicyModel
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.db.models.aggregates import Max


#node管理
@csrf_exempt
@try_except
def editCollectorAjax(request):
    '''
    edit monitor node info.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    request_id = request.META.get('REMOTE_ADDR','')
    result = editCollector(postdata, request_id)
    if result['status']:
        info('%s edit Collector info success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, result['message']).returnJSON()
    else:
        info('%s edit Collector info error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()


def editCollector(postdata, request_id=None):
    try:
        status = True
        message = _('更新成功。')
        unique_id = postdata.get('unique_id','')
        field = ['unique_id','nick_name','host_name','os_type','os_release','os_version','ip_address','access_port','omflow_version','level','loadbalance','software','hardware','security','active']
        node = Collector.objects.filter(unique_id=unique_id)
        param = {}
        for key in field:
            if postdata.get(key, None) != None:
                param[key] = postdata.get(key,'')
        if node:
            if postdata.get('ip_address', None) == None:
                param['updatetime'] = datetime.now()
            node.update(**param)
        else:
            if checkLicense('collector', False):
                param['nick_name'] = param['host_name']
                param['nodegroup_id'] = 1
                param['ip_address'] = request_id
                Collector.objects.create(**param)
            else:
                status = False
                message = _('更新失敗: 收集器數量已達上限。')
    except Exception as e:
        status = False
        message = _('更新失敗: ') + e.__str__()
    finally:
        return {'status':status, 'message':message}
    

@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def deleteCollectorAjax(request):
    '''
    delete collector info.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['collector_ids']
    #get post data
    postdata = getPostdata(request)
    collector_id_list = postdata.get('collector_ids',[])
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        Collector.objects.filter(id__in=collector_id_list).delete()
        info('%s delete Collector info success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('刪除成功。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def groupCollectorAjax(request):
    '''
    move monitor node to group.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['node_id_list']
    #get post data
    postdata = getPostdata(request)
    nodegroup_id = postdata.get('group_id',None)
    node_id_list = postdata.get('node_id_list','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        if nodegroup_id:
            c_list = Collector.objects.filter(id__in=node_id_list)
            if c_list:
                if c_list[0].nodegroup_id == 2:
                    try:
                        for c in c_list:
                            GlobalObject.__loadbalanceMissionObj__.pop(c.id)
                    except:
                        pass
                c_list.update(nodegroup_id=nodegroup_id)
        info('%s group Collector info success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def loadCollectorAjax(request):
    '''
    load monitor node.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['node_id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    node_id = postdata.get('node_id','')
    if checker.get('status') == 'success':
        result = list(Collector.objects.filter(id=node_id).values('id','unique_id','nick_name','host_name','os_type','os_release','os_version','ip_address','access_port','omflow_version','updatetime','nodegroup_id','nodegroup_id__name'))[0]
        info('%s load Collector success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def listCollectorAjax(request):
    '''
    list collector.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['nick_name__icontains','host_name__icontains','ip_address__icontains']
    query = ''
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    nodegroup_id = postdata.get('nodegroup_id',None)
    if datatable:
        if nodegroup_id:
            #collector一般列表使用
            display_field =['id','nick_name','host_name','ip_address','os_type','active','level']
            query = Collector.objects.filter(nodegroup_id=nodegroup_id).values(*display_field)
            result = DatatableBuilder(request, query, field_list)
            #燈號
            data = result['data']
            id_list = []
            if isinstance(data, list):
                for row in data:
                    id_list.append(row['id'])
                em_list = list(EventManagement.objects.filter(collector_id__in=id_list,closed=False).values('collector_id').annotate(Max('critical')))
                for row in data:
                    for em in em_list:
                        if em['collector_id'] == row['id']:
                            row['level'] = em['critical__max']
                            break
            elif isinstance(data, dict):
                for key in data:
                    id_list.append(data[key]['id'])
                em_list = list(EventManagement.objects.filter(collector_id__in=id_list,closed=False).values('collector_id').annotate(Max('critical')))
                for key in data:
                    for em in em_list:
                        if em['collector_id'] == data[key]['id']:
                            data[key]['level'] = em['critical__max']
                            break
        else:
            #policy派送使用
            flow_name = postdata.get('flow_name','')
            dispatch = postdata.get('dispatch','A')
            display_field =['id','nick_name','unique_id','os_type','active','ip_address']
            field_list = ['nick_name__icontains','os_type__icontains']
            table_id = MonitorFlow.objects.get(flow_name=flow_name,history=False).table_id
            collector_list = list(PolicyCollector.objects.filter(table_id=table_id).values('node_id','policy_version'))
            collector_dict = {}
            collector_id_list = []
            for collector in collector_list:
                collector_dict[collector['node_id']] = collector['policy_version']
                collector_id_list.append(collector['node_id'])
            if dispatch == 'A':
                query = Collector.objects.all().values(*display_field)
            elif dispatch == 'T':
                query = Collector.objects.filter(id__in=collector_id_list).values(*display_field)
            elif dispatch == 'F':
                query = Collector.objects.filter().exclude(id__in=collector_id_list).values(*display_field)
            result = DatatableBuilder(request, query, field_list)
            if isinstance(result['data'], list):
                for row in result['data']:
                    row['version'] = collector_dict.get(row['id'],'')
            elif isinstance(result['data'], dict):
                for key in result['data']:
                    result['data'][key]['version'] = collector_dict.get(result['data'][key]['id'],'')
        info('%s list Collector success.' % request.user.username,request)
        return JsonResponse(result)
    else:
        result = list(Collector.objects.filter(nodegroup_id=nodegroup_id).values())
        info('%s list Collector success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def loadPolicyCollectorsAjax(request):
    '''
    load policy's collectors.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_name']
    #get post data
    postdata = getPostdata(request)
    flow_name = postdata.get('flow_name',None)
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        mf = MonitorFlow.objects.get(flow_name=flow_name,history=False)
        table_id = mf.table_id
        flowobject = json.loads(mf.flowobject)
        items = flowobject['items']
        output = []
        for item in items:
            if item['type'] == 'end':
                config = item['config']
                config_output_list = config.get('output','')
                for config_output in config_output_list:
                    if config_output['name']:
                        des = config_output['des']
                        name = config_output['name'][2:-1]
                        if not des:
                            des = name
                        output.append({'name':name,'des':des})
                break
        collectors = list(PolicyCollector.objects.filter(table_id=table_id).values('node_id__nick_name','node_id__unique_id'))
        result = {'nodes':collectors,'output':output}
        info('%s load policy collectors.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def listNodePolicysAjax(request):
    '''
    list collector's policys.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['policy_id__flow_name__icontains']
    query = ''
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    node_id = postdata.get('node_id',None)
    if datatable:
        display_field =['id','policy_id__flow_name','policy_version','createtime']
        query = PolicyCollector.objects.filter(node_id=node_id).values(*display_field)
        result = DatatableBuilder(request, query, field_list)
        info('%s list Collector success.' % request.user.username,request)
        return JsonResponse(result)
    else:
        result = list(PolicyCollector.objects.filter(node_id=node_id).values())
        info('%s list Collector success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


def checkNodeStatus(*args):
    try:
        now_time = datetime.now()
        start_time = GlobalObject.__statusObj__['server_start_time'] + timedelta(minutes=3)
        if now_time > start_time:
            off_time = now_time - timedelta(minutes=3,seconds=10)
            collector_list = list(Collector.objects.filter(active=True,updatetime__lte=off_time).values('id','nick_name'))
            id_list = []
            for collector in collector_list:
                param = {}
                param['title'] = collector['nick_name'] + _('斷線。')
                param['content'] = collector['nick_name'] + _('斷線。')
                param['critical'] = 5
                param['collector_id'] = collector['id']
                param['source'] = 'schedule'
                param['source2'] = 'server check Nodes status'
                id_list.append(collector['id'])
                #開失聯的事件單
                createEvent(param)
            #關已重新連線的事件單
            EventManagement.objects.filter(source='schedule',closed=False).exclude(collector_id__in=id_list).update(closed=True)
    except Exception as e:
        debug(e.__str__())


def registerToServer(*args):
    '''
    node register to server
    input: None
    return: None
    author: Kolin Hsu
    '''
    try:
        #function variable
        new_file = ''
        server_ip = settings.SERVER_IP
        server_port = settings.SERVER_PORT
        #組裝postdata
        postdata = {}
#         postdata['ip_address'] = settings.LOCAL_IP
        postdata['access_port'] = settings.LOCAL_PORT
        postdata['host_name'] = socket.getfqdn(socket.gethostname())
        postdata['os_type'] = platform.system()
        postdata['os_release'] = platform.release()
        postdata['os_version'] = platform.version()
        postdata['omflow_version'] = License().getVersion()
        if settings.UNIQUE_ID:
            unique_id = settings.UNIQUE_ID
        else:
            if GlobalObject.__statusObj__.get('unique_id',''):
                unique_id = GlobalObject.__statusObj__.get('unique_id','')
            else:
                config_path = os.path.join(settings.BASE_DIR, "omflow", "settings.py")
                with open(config_path,'r',encoding='UTF-8') as f:
                    for line in f:
                        if re.match(r'UNIQUE_ID.+', line):
                            unique_id = uuid.uuid4().hex
                            line = 'UNIQUE_ID = "' + unique_id + '"\n'
                        new_file += line
                    f.close()
                with open(config_path,"w",encoding="utf-8") as f:
                    f.write(new_file)
                    f.close()
                GlobalObject.__statusObj__['unique_id'] = unique_id
        postdata['security'] = unique_id
        postdata['unique_id'] = unique_id
        my_data = urllib.parse.urlencode(postdata).encode(encoding="utf-8")
        #set api token
        GlobalObject.__securityObj__[unique_id] = {"username":'system',"security":unique_id,"updatetime":datetime.now()}
        GlobalObject.__userObj__['system'] = GlobalObject.__securityObj__[unique_id]
        #組裝url
        url = 'http://' + server_ip + ':' + server_port + '/monitor/api/monitor-node/edit/'
        #通過restapi呼叫node
        gcontext = ssl.create_default_context()
        with urllib.request.urlopen(url, data=my_data, context=gcontext) as response:
            result = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        debug(e.__str__())


def sendPolicyDataToServer(flow_name, output_obj):
    '''
    node send policy data to server
    input: param
    author: Kolin Hsu
    '''
    try:
        #function variable
        server_ip = settings.SERVER_IP
        server_port = settings.SERVER_PORT
        unique_id = settings.UNIQUE_ID
        if not unique_id:
            unique_id = GlobalObject.__statusObj__.get('unique_id','')
        #組裝postdata
        postdata = {}
        postdata['flow_name'] = flow_name
        postdata['unique_id'] = unique_id
        postdata['policy_data'] = json.dumps(output_obj)
        my_data = urllib.parse.urlencode(postdata).encode(encoding="utf-8")
        #組裝url
        url = 'http://' + server_ip + ':' + server_port + '/monitor/api/policy-data/create/'
        #通過restapi呼叫node
        gcontext = ssl.create_default_context()
        with urllib.request.urlopen(url, data=my_data, context=gcontext) as response:
            result = json.loads(response.read().decode())
    except Exception as e:
        debug(e.__str__())



@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def monitorManagePage(request):
    return render(request, 'monitor_manage.html')


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def monitorAPIDesignPage(request, url):
    flow_id = url.split('/')[0]
    try: 
        flow_name = MonitorFlow.objects.get(id=flow_id).flow_name
    except:
        pass
    return render(request, 'monitor_api_design.html', locals())


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def monitorAPIManagePage(request):
    return render(request, 'monitor_api_manage.html')


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def monitorDesignPage(request, url):
    flow_id = url.split('/')[0]
    try: 
        flow_name = MonitorFlow.objects.get(id=flow_id).flow_name
    except:
        pass
    return render(request, 'monitor_design.html', locals())


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def monitorParameterPage(request, url):
    group_id = url.split('/')[0]
    try: 
        group_name = CollectorGroup.objects.get(id=group_id).name
    except:
        pass
    return render(request, 'monitor_parameter.html', locals())

@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def nodeGroupsManagePage(request):
    return render(request, 'node_groups_manage.html')

@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def nodeListManagePage(request, url):
    group_id = url.split('/')[0]
    try: 
        group_name = CollectorGroup.objects.get(id=group_id).name
    except:
        pass
    return render(request, 'node_list_manage.html', locals())

@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def nodeManagePage(request, url):
    node_id = url.split('/')[0]
    return render(request, 'node_manage.html', locals())

@login_required
@permission_required('ommonitor.OmMonitor_Manage','/page/403/')
def eventManagePage(request):
    return render(request, 'event_manage.html')


#policy管理
@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def exportMonitorApplicationAjax(request):
    '''
    export monitor application.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_name_list']
    result = []
    #get post data
    postdata = getPostdata(request)
    flow_name_list = postdata.get('flow_name_list','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        for flow_name in flow_name_list:
            app_dict = exportMonitorApplication(flow_name)
            result.append(app_dict)
        info('%s export WorkspaceApplication success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('匯出成功。'), result).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def exportMonitorApplication(flow_name):
    try:
        app_dict = {}
        flow_list = []
        ma = MonitorApplication.objects.get(app_name=flow_name)
        mf = list(MonitorFlow.objects.filter(flow_name=flow_name,history=False).values('flow_name','description','attr','flowobject','config','type','schedule','event_rule','os_type'))[0]
        mf['flowobject'] = json.loads(mf['flowobject'])
        mf['config'] = json.loads(mf['config']) 
        flow_list.append(mf)
        app_dict['app_name'] = ma.app_name
        app_dict['app_attr'] = ma.app_attr
        app_dict['flow_list'] = flow_list
    except Exception as e:
        debug(e.__str__())
    finally:
        return app_dict
    

@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def importMonitorApplicationAjax(request):
    '''
    import monitor application.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['app_list']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    app_list = json.loads(postdata.get('app_list',[]))
    if checker.get('status') == 'success':
        ima_res = importMonitorApplication(app_list, request.user)
        if ima_res['status']:
            info('%s import WorkspaceApplication success.' % request.user.username,request)
            return ResponseAjax(statusEnum.success, _('匯入成功。')).returnJSON()
        else:
            info('%s export WorkspaceApplication error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, ima_res['message']).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def importMonitorApplication(app_list, user):
    try:
        status = True
        update = False
        message = ''
        for app in app_list:
            app_name = app['app_name']
            if not re.match(r'.*[\\<>/|].*',app_name):
                policy_attr = app['app_attr']
                flow_list = app['flow_list']
                ma_list = list(MonitorApplication.objects.filter(app_name=app_name))
                if ma_list:
                    update = True
                    ma = ma_list[0]
                else:
                    ma = MonitorApplication.objects.create(app_name=app_name,user=user,app_attr=policy_attr)
                for flow in flow_list:
                    flow['app_id'] = ma.id
                    flow['policy_attr'] = policy_attr
                    flow['formobject'] = json.dumps(flow['flowobject'].get('form_object',''))
                    flow['flowobject'] = json.dumps(flow['flowobject'])
                    flow['config'] = json.dumps(flow['config'])
                    #檢查end點變數名稱是否合規
                    var_check = checkEndPointVariableFormat(flow['flowobject'])
                    if var_check:
                        if update:
                            result = updateMonitorFlow(flow, user)
                        else:
                            result = createMonitorFlow(flow, user)
                        if not result:
                            status = False
                            message += _('流程匯入失敗。')
                            break
                    else:
                        status = False
                        message += _('流程匯入失敗，結束點輸出變數名只能是英數字。')
                        break
            else:
                status = False
                message += _('流程匯入失敗，名稱不得包含特殊符號(/,\,<,>,|)。')
                break
        if not status and not update:
            MonitorApplication.objects.filter(app_name=app_name).delete()
    except Exception as e:
        message += e.__str__()
        status = False
    finally:
        return {'status':status,'message':message}


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def createMonitorFlowAjax(request):
    '''
    create custom monitor flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    result = {}
    require_field = ['flow_name']
    #server side rule check
    postdata = getPostdata(request)
    data_checker = DataChecker(postdata, require_field)
    flow_name = postdata.get('flow_name','')
    policy_attr_num = postdata.get('policy_attr',1)
    policy_attr = getPolicyAttr(policy_attr_num)
    if data_checker.get('status') == 'success':
        flowobject_str = postdata.get('flowobject','{}')
        var_check = checkEndPointVariableFormat(flowobject_str)
        if var_check:
            if not re.match(r'.*[\\<>/|].*',flow_name):
                same_name = MonitorApplication.objects.filter(app_name=flow_name).count()
                if same_name == 0:
                    api_path = json.loads(postdata.get('config','{}')).get('api_path','')
                    api_check = checkAPIpath(api_path)
                    if api_check['status']:
                        m = MonitorApplication.objects.create(app_name=flow_name,user=request.user,app_attr=policy_attr)
                        postdata = postdata.copy() #不確定
                        postdata['app_id'] = m.id
                        postdata['policy_attr'] = policy_attr
                        result = createMonitorFlow(postdata, request.user)
                        if result:
                            info('%s create MonitorFlow success.' % request.user.username,request)
                            return ResponseAjax(statusEnum.success, _('建立成功。'), result).returnJSON()
                        else:
                            MonitorApplication.objects.filter(app_name=flow_name).delete()
                            MonitorFlow.objects.filter(flow_name=flow_name).delete()
                            info('%s create MonitorFlow error.' % request.user.username,request)
                            return ResponseAjax(statusEnum.success, _('建立失敗。')).returnJSON()
                    else:
                        info('%s create fail, api_path error.' % request.user.username,request)
                        return ResponseAjax(statusEnum.not_found, api_check['message']).returnJSON()
                else:
                    info('%s create fail, MonitorFlow has same name in this application.' % request.user.username,request)
                    return ResponseAjax(statusEnum.not_found, _('重複名稱。')).returnJSON()
            else:
                info('%s create fail, flow name can not include(/,\,<,>,|).' % request.user.username,request)
                return ResponseAjax(statusEnum.not_found, _('名稱不得包含特殊符號(/,\,<,>,|)')).returnJSON()
        else:
            info('%s update MonitorFlow error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, _('結束點輸出變數名只能是英數字。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


def createMonitorFlow(param,user):
    '''
    create custom monitor flow.
    input: param,user
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
        policy_attr = param.get('policy_attr','')
        os_type = param.get('os_type','')
        schedule = param.get('schedule','')
        event_rule = param.get('event_rule','')
        config_dict = json.loads(param.get('config','{}'))
        version = param.get('version',1)
        table_id = param.get('table_id','')
        policy_type = config_dict.get('type','')
        for i in ['fp_show','attachment','relation','worklog','history','mission','flowlog','api']:
            config_dict[i] = False
        if policy_attr == 'api':
            config_dict['api'] = True
        #map subflow object and config
        subflow_list = json.loads(flowobject).get('subflow','')
        subflow_config_list = config_dict.get('subflow','')
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
        config = json.dumps(config_dict)
        mf = MonitorFlow.objects.create(flow_name=flow_name,schedule=schedule,\
                                     create_user=user,formobject=formobject,\
                                     flowobject=flowobject,config=config,subflow=subflow,\
                                     description=description,type=policy_type,\
                                     flow_app_id=app_id,attr=policy_attr,os_type=os_type,\
                                     event_rule=event_rule,version=version,table_id=table_id)
        if not table_id:
            mf.table_id = mf.id
            mf.save()
        result['flow_id'] = mf.id
        result['flow_name'] = mf.flow_name
        return result
    except Exception as e:
        debug(e.__str__())
        return False


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def getOutsideFlowAjax(request):
    '''
    get outside's input and output
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
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
    info('%s load outside flow success.' % request.user.username,request)
    return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    

@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def updateMonitorFlowAjax(request):
    '''
    update custom monitor flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function varaible
    require_field = ['flow_name']
    #server side rule check
    postdata = getPostdata(request)
    data_checker = DataChecker(postdata, require_field)
    if data_checker.get('status') == 'success':
        api_path = json.loads(postdata.get('config','{}')).get('api_path','')
        api_check = checkAPIpath(api_path)
        if api_check['status']:
            flowobject_str = postdata.get('flowobject','{}')
            var_check = checkEndPointVariableFormat(flowobject_str)
            if var_check:
                umf_res = updateMonitorFlow(postdata, request.user)
                if umf_res['status']:
                    info('%s update MonitorFlow success.' % request.user.username,request)
                    return ResponseAjax(statusEnum.success, umf_res['message']).returnJSON()
                else:
                    info('%s update MonitorFlow error.' % request.user.username,request)
                    return ResponseAjax(statusEnum.not_found, umf_res['message']).returnJSON()
            else:
                info('%s update MonitorFlow error.' % request.user.username,request)
                return ResponseAjax(statusEnum.not_found, _('結束點輸出變數名只能是英數字。')).returnJSON()
        else:
            info('%s update fail, api_path error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, api_check['message']).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request,request)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


def checkEndPointVariableFormat(flowobject_str):
    var_check = True
    items = json.loads(flowobject_str).get('items','')
    for item in items:
        if item['type'] == 'end':
            output = item['config']['output']
            for o in output:
                name = o['name'][2:-1]
                if re.match(r'[A-Za-z0-9_]+', name):
                    pass
                else:
                    var_check = False
                    break
    return var_check
    


def updateMonitorFlow(param, user):
    '''
    update custom monitor flow.
    '''
    #function varaible
    message = _('更新成功。')
    check = True
    subflow = []
    new_flow_id = None
    try:
        #get post data
        flow_name = param.get('flow_name','')
        flow_id = param.get('flow_id','')
        flowobject = param.get('flowobject','')
        config = param.get('config','')
        schedule = param.get('schedule', '')
        event_rule = param.get('event_rule','')
        formobject = param.get('formobject','')
        description = param.get('description','')
        if not flow_id:
            monitorflow = MonitorFlow.objects.get(flow_name=flow_name,history=False)
        else:
            monitorflow = MonitorFlow.objects.get(id=flow_id,history=False)
        #確定是否已經派送過、是否更名以及重複名稱
        dispatch = PolicyCollector.objects.filter(table_id=monitorflow.table_id).exists()
        if monitorflow.flow_name != flow_name:
            change_name = True
            if dispatch:
                check = False
                message = _('已派送的流程無法更名。')
            else:
                has_same_name = MonitorFlow.objects.filter(flow_name=flow_name).exists()
                if has_same_name:
                    check = False
                    message = _('重複名稱。')
        else:
            change_name = False
        if check:
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
            subflow = json.dumps(subflow)
            #確認該版本是否已經派送過
            #已經派送過則將舊版轉為歷史，並建立新版
            if PolicyCollector.objects.filter(policy_id=monitorflow.id).exists():
                monitorflow.history = True
                monitorflow.save()
                version = MonitorFlow.objects.filter(table_id=monitorflow.table_id).aggregate(Max('version'))['version__max'] + 1
                new_mf = MonitorFlow.objects.create(flow_name=flow_name,schedule=schedule,\
                                     create_user=user,formobject=formobject,\
                                     flowobject=flowobject,config=config,subflow=subflow,\
                                     description=description,version=version,\
                                     flow_app_id=monitorflow.flow_app_id,attr=monitorflow.attr,\
                                     event_rule=event_rule,table_id=monitorflow.table_id)
                new_flow_id = new_mf.id
            else:
                monitorflow.flow_name = flow_name
                monitorflow.schedule = schedule
                monitorflow.formobject = formobject
                monitorflow.flowobject = flowobject
                monitorflow.config = config
                monitorflow.subflow = subflow
                monitorflow.description = description
                monitorflow.event_rule = event_rule
                monitorflow.save()
            #如果更名，需順便更新app
            if change_name:
                ma = MonitorApplication.objects.get(app_name=monitorflow.flow_name)
                ma.app_name = flow_name
                ma.save()
    except Exception as e:
        check = False
        message = e.__str__()
    finally:
        return {'status':check, 'message':message, 'flow_id':new_flow_id}


def checkAPIpath(api_path, flow_id=None):
    try:
        status = True
        message = ''
        if api_path:
            if flow_id:
                cs = list(MonitorFlow.objects.filter().exclude(id=flow_id).values('config'))
            else:
                cs = list(MonitorFlow.objects.filter().values('config'))
            for c in cs:
                if c.get('api_path','') == api_path:
                    status = False
                    message = _('api')
                    break
        else:
            status = False
            message = _('api路徑不得為空。')
    except Exception as e:
        status = False
        message = e.__str__()
    finally:
        return {'status':status, 'message':message}


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def listMonitorFlowAjax(request):
    '''
    list custom monitor flow.
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
    policy_attr_num = postdata.get('policy_attr',1)
    policy_attr = getPolicyAttr(policy_attr_num)
    if datatable:
        updatetime = postdata.get('updatetime','')
        display_field =['id','flow_name','updatetime','description','type','create_user_id__username','version']
        query = MonitorFlow.objects.filter(history=False,attr=policy_attr,updatetime__lte=updatetime).values(*display_field)
        result = DatatableBuilder(request, query, field_list)
        info('%s list MonitorFlow success.' % request.user.username,request)
        return JsonResponse(result)
    else:
        flow_id = postdata.get('flow_id',None)
        if flow_id == 'newflow':
            result = list(MonitorFlow.objects.filter(history=False,attr=policy_attr).values('flow_name'))
        elif flow_id:
            result = list(MonitorFlow.objects.filter(history=False,attr=policy_attr).exclude(id=flow_id).values('flow_name'))
        info('%s list MonitorFlow success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def loadMonitorFlowAjax(request):
    '''
    load custom monitor flow.
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
        result = list(MonitorFlow.objects.filter(id=flow_id).values('id','flow_name','type','description','formobject','flowobject','config','schedule','event_rule'))[0]
        info('%s load MonitorFlow success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def deleteMonitorFlowAjax(request):
    '''
    delete custom monitor flow.
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = getPostdata(request)
    flow_name_list = postdata.get('flow_name','')
    table_id_list = list(MonitorFlow.objects.filter(flow_name__in=flow_name_list,history=False).values_list('table_id',flat=True))
    dispatch_id_list = list(PolicyCollector.objects.filter(table_id__in=table_id_list).values_list('table_id',flat=True).distinct())
    if dispatch_id_list:
        dispatch_name_list = list(MonitorFlow.objects.filter(id__in=dispatch_id_list).values_list('flow_name',flat=True))
        info('%s delete MonitorFlow error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, _('刪除失敗，下列流程有已派送之節點：'), dispatch_name_list).returnJSON()
    else:
        MonitorApplication.objects.filter(app_name__in=flow_name_list).delete()
        info('%s delete MonitorFlow success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('刪除成功。')).returnJSON()


@login_required
@permission_required('omformflow.OmMonitor_Manage','/api/permission/denied/')
@try_except
def getMonitorFlowAPIFormatAjax(request):
    '''
    show flow api format.
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
    action = postdata.get('action','')
    if checker.get('status') == 'success':
        mf = MonitorFlow.objects.get(flow_name=flow_name,history=False)
        start_input = {}
        items = json.loads(mf.flowobject)['items']
        for item in items:
            if item['id'] == 'FITEM_1':
                break
        input_list = item['config']['input']
        for input_dict in input_list:
            name = input_dict['name']
            value = input_dict['value']
            start_input[name] = value
        result['security'] = '<security>'
        result['api_path'] = json.loads(mf.config).get('api_path','')
        result['action'] = action
        result['omflow_restapi'] = 1
        result['start_input'] = start_input
        info('%s list flow form point success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
        

@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def listMonitorFlowVersionAjax(request):
    '''
    list monitor flow version.
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
    flow_name = postdata.get('flow_name','')
    if datatable:
        updatetime = postdata.get('updatetime','')
        display_field =['id','updatetime','description','version']
        query = MonitorFlow.objects.filter(flow_name=flow_name,updatetime__lte=updatetime).values(*display_field)
        result = DatatableBuilder(request, query, field_list)
        info('%s list MonitorFlow success.' % request.user.username,request)
        return JsonResponse(result)
    else:
        #目前還沒有功能使用
        result = list(MonitorFlow.objects.filter(flow_name=flow_name).values('flow_name'))
        info('%s list MonitorFlow success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def loadMonitorFlowVersionAjax(request):
    '''
    load monitor flow version.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_name','version']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_name = postdata.get('flow_name','')
    version = postdata.get('version','')
    if checker.get('status') == 'success':
        result = list(MonitorFlow.objects.filter(flow_name=flow_name,version=version).values('id','flow_name','type','description','formobject','flowobject','config','schedule','event_rule'))[0]
        info('%s load MonitorFlow success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def deleteMonitorFlowVersionAjax(request):
    '''
    delete monitor flow version.
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = getPostdata(request)
    flow_name = postdata.get('flow_name','')
    version_list = postdata.get('version','')
    #找出該流程勾選的舊版本
    policys = MonitorFlow.objects.filter(flow_name=flow_name,history=True,version__in=version_list)
    policy_list = list(policys)
    policy_id_list = []
    #組成id list並檢查是否有派送過的節點
    for i in policy_list:
        policy_id_list.append(i.id)
    dispatch_id_list = list(PolicyCollector.objects.filter(policy_id__in=policy_id_list).values_list('policy_id',flat=True).distinct())
    #如果已經派送，找出派送過的版本列表並回傳
    #如果沒有派送，刪除這些版本
    if dispatch_id_list:
        dispatch_version_list = list(MonitorFlow.objects.filter(id__in=dispatch_id_list).values_list('flow_name',flat=True))
        for i in policy_list:
            if i.id in dispatch_id_list:
                dispatch_version_list.append(i.version)
        info('%s delete MonitorFlow error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, _('刪除失敗，下列版本有已派送之節點：'), dispatch_version_list).returnJSON()
    else:
        policys.delete()
        info('%s delete MonitorFlow success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('刪除成功。')).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def copyMonitorFlowAjax(request):
    '''
    copy custom form, flow, setting.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_name','new_name']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_name = postdata.get('flow_name','')
    new_name = postdata.get('new_name','')
    policy_attr_num = postdata.get('policy_attr',1)
    policy_attr = getPolicyAttr(policy_attr_num)
    updatetime = datetime.now()
    if checker.get('status') == 'success':
        flag = MonitorFlow.objects.filter(flow_name=new_name).exists()
        if not flag:
            mf_list = list(MonitorFlow.objects.filter(flow_name=flow_name).values())
            if mf_list:
                mf = mf_list[0]
                m = MonitorApplication.objects.create(app_name=flow_name,user=request.user,app_attr=policy_attr)
                mf.pop('id')
                mf['flow_name'] = new_name
                mf['flow_app_id'] = m.id
                mf['create_user_id'] = request.user.id
                mf['updatetime'] = updatetime
                mf['version'] = 1
                n_mf = MonitorFlow.objects.create(**mf)
                n_mf.table_id = n_mf.id
                n_mf.save()
                info('%s copy MonitorFlow success.' % request.user.username,request)
                return ResponseAjax(statusEnum.success, _('複製成功。')).returnJSON()
            else:
                info('%s copy MonitorFlow error.' % request.user.username,request)
                return ResponseAjax(statusEnum.not_found, _('名稱錯誤。')).returnJSON()
        else:
            info('%s copy MonitorFlow error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, _('重複名稱。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def dispatchMonitorFlowAjax(request):
    '''
    dispatch custom monitor flow to node.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_name','unique_id']
    message = ''
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_name = postdata.get('flow_name','')
#     version = postdata.get('version','')
    collector_unique_id = postdata.get('unique_id','')
    if checker.get('status') == 'success':
        try:
            node = Collector.objects.get(unique_id=collector_unique_id)
        except:
            node = None
            message = _('找不到收集器。')
        if node:
            #建立或更新policy的模型
            variable_list = []
            mf = MonitorFlow.objects.get(flow_name=flow_name,history=False)
#             mf = MonitorFlow.objects.get(flow_name=flow_name,version=version)
            items = json.loads(mf.flowobject)['items']
            for item in items:
                if item['type'] == 'end':
                    output_list = item['config']['output']
                    break
            for output in output_list:
                if output['name']:
                    variable_list.append(output['name'][2:-1])
            OMPolicyModel.deployModel(mf.table_id, flow_name, variable_list)
            #取得policy流程的匯出格式
            export_dict = exportMonitorApplication(flow_name)
            #取得派送的系統參數
            op_sys = list(OmParameter.objects.filter(group_id=None).values('name','value','description','type','shadow'))
            op_group = list(OmParameter.objects.filter(group_id=node.nodegroup_id).values('name','value','description','type','shadow'))
            #組裝formdata
            my_data = {}
            my_data['security'] = node.security
            my_data['dispatch_policy'] = json.dumps(export_dict)
            my_data['app_attr'] = 4
            my_data['app_name'] = flow_name
            my_data['schedule'] = mf.schedule
            my_data['omparameter_sys'] = json.dumps(op_sys)
            my_data['omparameter_group'] = json.dumps(op_group)
            my_data['omflow_restapi'] = True
            my_data = urllib.parse.urlencode(my_data).encode(encoding="utf-8")
            #組裝url
            url = 'http://' + node.ip_address + ':' + node.access_port + '/rest/flowmanage/api/node-policy/receive/'
            #通過restapi呼叫node
            gcontext = ssl.create_default_context()
#             new_request = urllib.request.Request(url = url,data = my_data,method = 'POST')
            with urllib.request.urlopen(url, data=my_data, context=gcontext) as response:
                result = json.loads(response.read().decode('utf-8'))
            if result['status'] == 200:
                #刪除node與該policy舊版本的關聯
                PolicyCollector.objects.filter(node=node,table_id=mf.table_id).delete()
                #建立node與policy的關聯
                PolicyCollector.objects.create(node=node,policy=mf,table_id=mf.table_id,policy_version=mf.version)
                info('%s dispatch MonitorFlow success.' % request.user.username,request)
                return ResponseAjax(statusEnum.success, _('派送成功。')).returnJSON()
            else:
                info('%s dispatch MonitorFlow error.' % request.user.username,request)
                return ResponseAjax(statusEnum.not_found, _('派送失敗：') + result['message']).returnJSON()
        else:
            info('%s dispatch MonitorFlow error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, _('派送失敗：') + message).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def removePolicyCollectorAjax(request):
    '''
    undeploy policy.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_name','unique_id']
    message = ''
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_name = postdata.get('flow_name','')
    collector_unique_id = postdata.get('unique_id','')
    if checker.get('status') == 'success':
        try:
            node = Collector.objects.get(unique_id=collector_unique_id)
        except:
            node = None
            message = _('找不到收集器。')
        if node:
            mf = MonitorFlow.objects.get(flow_name=flow_name,history=False)
            #組裝postdata
            my_data = {'app_name':flow_name,'security':node.security,'omflow_restapi':True}
            my_data = urllib.parse.urlencode(my_data).encode(encoding="utf-8")
            #組裝url
            url = 'http://' + node.ip_address + ':' + node.access_port + '/rest/flowmanage/api/flow-active-app/undeploy/'
            #通過restapi呼叫node
            gcontext = ssl.create_default_context()
            with urllib.request.urlopen(url, data=my_data, context=gcontext) as response:
                result = json.loads(response.read().decode('utf-8'))
            if result['status'] == 200:
                #刪除node與該policy舊版本的關聯
                PolicyCollector.objects.filter(node=node,table_id=mf.table_id).delete()
                info('%s dispatch MonitorFlow success.' % request.user.username,request)
                return ResponseAjax(statusEnum.success, _('下架成功。')).returnJSON()
            else:
                info('%s dispatch MonitorFlow error.' % request.user.username,request)
                return ResponseAjax(statusEnum.not_found, _('下架失敗：') + result['message']).returnJSON()
        else:
            info('%s dispatch MonitorFlow error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, _('下架失敗：') + message).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@csrf_exempt
@try_except
def createPolicyDataAjax(request):
    '''
    receive nodes policy data.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['flow_name','unique_id']
    message = ''
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    flow_name = postdata.get('flow_name','')
    collector_unique_id = postdata.get('unique_id','')
    policy_data = postdata.get('policy_data','{}')
    if isinstance(policy_data, str):
        policy_data = json.loads(policy_data)
    if checker.get('status') == 'success':
        try:
            collector = Collector.objects.get(unique_id=collector_unique_id)
        except:
            collector = None
            message = _('找不到主機。')
        if collector:
            #在policy table寫入資料
            mf = MonitorFlow.objects.get(flow_name=flow_name,history=False)
            table_id = mf.table_id
            policy_type = mf.type
            model_name = 'OmPolicy_' + str(table_id)
            model = getModel('ompolicymodel', model_name)
            policy_data['collector_id'] = collector.id
            model.objects.create(**policy_data)
            #判斷是否需要開/關事件
            mf = PolicyCollector.objects.get(node=collector,table_id=table_id).policy
            if mf.event_rule:
                event_rule_list = json.loads(mf.event_rule).get('event_result',[])
                for event_rule in event_rule_list:
                    conditions = event_rule['event_result_compare']
                    ec = evalCondition(policy_type, conditions, policy_data)
                    if ec:
                        param = {}
                        param['title'] = event_rule['title']
                        param['content'] = event_rule['content']
                        param['critical'] = event_rule['critical']
                        param['collector_id'] = collector.id
                        param['source'] = 'policy'
                        #基礎監控<CPU過高><syscomitsmap01>
                        param['source2'] = mf.flow_name + '<' + event_rule['event_name'] + '><' + collector.nick_name + '>'
                        createEvent(param)
                    else:
                        source2 = mf.flow_name + '<' + event_rule['event_name'] + '><' + collector.nick_name + '>'
                        em = EventManagement.objects.filter(source='policy',source2=source2,closed=False)
                        if em.exists():
                            em.update(closed=True)
            info('%s create Policy data success.' % request.user.username,request)
            return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()
        else:
            info('%s create Policy data error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, _('更新失敗：') + message).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def evalCondition(con_type, conditions, data):
    try:
        if isinstance(conditions, str):
            conditions = json.loads(conditions)
        result = False
        combine_str = "lambda : "
        for con in conditions:
            keynum = re.findall(r'[a-z]+_([0-9]+)',list(con.keys())[0])[0]
            switch = ' ' + con.get('switch_'+keynum,'') + ' '
            combine_str += switch
            output = data.get(con.get('output_'+keynum,''),'')
            rule = con.get('rule_'+keynum,'')
            value = con.get('value_'+keynum,'')
            if con_type == 'num':
                if rule == '=':
                    rule = '=='
                if output and rule and value:
                    combine_str += str(output) + rule + str(value)
                else:
                    combine_str += 'False'
            elif con_type == 'INC':
                if rule == 'include':
                    combine_str += '"' + str(value) + '" in "' + str(output) + '"'
                elif rule == 'exclude':
                    combine_str += '"' + str(value) + '" not in "' + str(output) + '"'
                elif rule == '=':
                    combine_str += '"' + str(output) + '" == "' + str(value) + '"'
                elif rule == '!=':
                    combine_str += '"' + str(output) + '" != "' + str(value) + '"'
                else:
                    combine_str += str(output) + rule + str(value)
            else:
                combine_str += 'False'
        result = eval(combine_str)()
    except:
        pass
    finally:
        return result


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def listPolicyDataAjax(request):
    '''
    list nodes policy data.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['error_message__icontains']
    query = ''
    # get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    flow_name = postdata.get('flow_name','')
    try:
        mf = MonitorFlow.objects.get(flow_name=flow_name)
        model_name = 'OmPolicy_' + str(mf.id)
        model = getModel('ompolicymodel', model_name)
        if datatable:
            createtime = postdata.get('createtime','').split(',')
            query = model.objects.filter(createtime__range=createtime).values()
            result = DatatableBuilder(request, query, field_list)
            info('%s list policy data success.' % request.user.username,request)
            return JsonResponse(result)
        else:
            result = list(model.objects.all())
            info('%s list policy data success.' % request.user.username,request)
            return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()
    except Exception as e:
        info('%s list Policy data error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, _('查詢失敗：') + e.__str__()).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def loadPolicyDataAjax(request):
    '''
    load nodes policy data.
    input: request
    return: json
    author: Kolin Hsu
    '''
    require_field = ['unique_id','flow_name','data_name','time_range']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    unique_id = postdata.get('unique_id','')
    flow_name = postdata.get('flow_name','')
    data_name = postdata.get('data_name','')
    time_range = postdata.get('time_range','')
    time_start = re.findall("(.+) - .+", time_range)[0]
    time_stop = re.findall(".+ - (.+)", time_range)[0]
    if checker.get('status') == 'success':
        mf = MonitorFlow.objects.get(flow_name=flow_name,history=False)
        model_name = 'OmPolicy_' + str(mf.table_id)
        model = getModel('ompolicymodel', model_name)
        
        val_list = list(model.objects.filter(collector_id__unique_id=unique_id,createtime__gte=time_start,createtime__lt=time_stop).values_list(data_name, flat=True))
        time_list = list(model.objects.filter(collector_id__unique_id=unique_id,createtime__gte=time_start,createtime__lt=time_stop).values_list('createtime', flat=True))
        
        result = {}
        result['value'] = val_list
        result['time'] = time_list
        
        info('%s load policy data success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
        
    
#server分散處理，collector執行python檔    
def sendPython(flow_uuid, data, chart_file):
    '''
    分散式運算預留
    '''
    try:
        #篩選可用collector
        lose_c_id_list = list(EventManagement.objects.filter(critical=5,closed=False).values_list('collector_id',flat=True).distinct())
        collector_list = list(Collector.objects.filter(nodegroup_id=2).exclude(id__in=lose_c_id_list))
        if collector_list:
            #給予一組uid作為辨識
            queue_id = flow_uuid + str(data.get('data_id','')) + str(data.get('chart_id_from',''))
            uid = str(time.mktime(datetime.now().timetuple()))
            GlobalObject.__loadbalanceObj__[queue_id] = uid
            #條件判斷選擇collector(任務數量最少者)
            for node in collector_list:
                loadbalance_mission = GlobalObject.__loadbalanceMissionObj__.get(node.id,None)
                if loadbalance_mission == None:
                    GlobalObject.__loadbalanceMissionObj__[node.id] = []
            md = GlobalObject.__loadbalanceMissionObj__
            sort_mission_dict = {k: v for k, v in sorted(md.items(), key=lambda item: len(item[1]))}
            api_status = 0
            for key in sort_mission_dict:
                try:
                    for collector in collector_list:
                        if collector.id == int(key):
                            break
                    #組裝postdata
                    data_str = json.dumps(data)
                    postdata = {}
                    postdata['uid'] = uid
                    postdata['security'] = collector.security
                    postdata['flow_uuid'] = flow_uuid
                    postdata['data'] = data_str
                    postdata['chart_file'] = chart_file
                    postdata['omflow_restapi'] = True
                    my_data = urllib.parse.urlencode(postdata).encode(encoding="utf-8")
                    #組裝url
                    url = 'http://' + collector.ip_address + ':' + collector.access_port + '/rest/monitor/api/python/receive/'
                    #通過restapi呼叫node
                    gcontext = ssl.create_default_context()
                    with urllib.request.urlopen(url, data=my_data, context=gcontext) as response:
                        result = json.loads(response.read().decode('utf-8'))
                    api_status = result['status']
                except:
                    pass
                if api_status == 200:
                    #成功回傳後放置任務
                    GlobalObject.__loadbalanceMissionObj__[node.id].append(uid)
                    break
            if api_status != 200:
                data['error_message'] = _('所有分散群組中的collector皆回傳失敗。')
                data['error'] = True
                OmEngine(flow_uuid,data).checkActive()
        else:
            data['error_message'] = _('分散式運算群組沒有Collector可使用。')
            data['error'] = True
            OmEngine(flow_uuid,data).checkActive()
    except Exception as e:
        data['error_message'] = _('分散式運算錯誤：') + e.__str__()
        data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    

@csrf_exempt
@try_except
def receivePythonResultAjax(request):
    postdata = getPostdata(request)
    uid = postdata.get('uid','')
    flow_uuid = postdata.get('flow_uuid','')
    data = postdata.get('data','')
    if isinstance(data, str):
        data = json.loads(data)
    queue_id = flow_uuid + str(data.get('data_id','')) + str(data.get('chart_id_from',''))
    if uid == GlobalObject.__loadbalanceObj__.get(queue_id,''):
        OmEngine(flow_uuid,data).checkActive()
        GlobalObject.__loadbalanceObj__.pop(queue_id)
        #移除collector任務列表
        for key in GlobalObject.__loadbalanceMissionObj__:
            if uid in GlobalObject.__loadbalanceMissionObj__[key]:
                GlobalObject.__loadbalanceMissionObj__[key].remove(uid)
                break
        info('%s receive load balance data success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()
    else:
        info('%s receive load balance data error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, _('更新失敗：該筆資料對應之uid錯誤。')).returnJSON()


@try_except
def receivePythonAjax(request):
    '''
    node receive python.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    postdata = getPostdata(request)
    flow_uuid = postdata.get('flow_uuid','')
    data = postdata.get('data','')
    uid = postdata.get('uid','')
    chart_file = postdata.get('chart_file','')
    if isinstance(data, str):
        data = json.loads(data)
    module_name = 'ommonitor.views'
    method_name = 'sendPythonResult'
    input_param = {'uid':uid,'flow_uuid':flow_uuid,'data':data,'chart_file':chart_file}
    input_param_str = json.dumps(input_param)
    LoadBalanceQueueData.objects.create(queue_id=uid,input_param=input_param_str,module_name=module_name,method_name=method_name)
    #put queue
    LoadBalanceMonitor.putQueue(module_name, method_name, input_param)
    info('%s receive load balance data success.' % request.user.username,request)
    return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()


def sendPythonResult(param):
    try:
        flow_uuid = param.get('flow_uuid','')
        data = param.get('data','')
        chart_file = param.get('chart_file','')
        uid = param.get('uid','')
        #處理、執行python
        execPython(data, chart_file)
        new_data = json.dumps(data)
        postdata = {}
        postdata['flow_uuid'] = flow_uuid
        postdata['data'] = new_data
        postdata['uid'] = uid
        my_data = urllib.parse.urlencode(postdata).encode(encoding="utf-8")
        #完成後發送結果回server
        server_ip = settings.SERVER_IP
        server_port = settings.SERVER_PORT
        #組裝url
        url = 'http://' + server_ip + ':' + server_port + '/monitor/api/python-result/receive/'
        #通過restapi呼叫server
        gcontext = ssl.create_default_context()
        with urllib.request.urlopen(url, data=my_data, context=gcontext) as response:
            result = json.loads(response.read().decode('utf-8'))
        #如果回傳200移除queue db
        if result['status'] == 200:
            LoadBalanceQueueData.objects.filter(queue_id=uid).delete()
    except Exception as e:
        debug(e.__str__())
        

def execPython(data, chart_file):
    try:
        autoinstall = data.get('autoinstall',False)
        chart_input = data['chart_input']
        chart_input_str = json.dumps(chart_input)
        chart_input_c = json.loads(chart_input_str)
        import_error = False
        package = ''
        import_str = ''
        chart_file_to_list = chart_file.split('\n')
        for line in chart_file_to_list:
            line_lstrip = line.lstrip()
            if (line_lstrip[:7] == 'import ') or (line_lstrip[:5] == 'from '):
                import_str += line_lstrip + '\n'
        compile_import_str = compile(import_str,'','exec')
        loop = True
        last_package = ''
        while loop:
            try:
                exec(compile_import_str)
                compileObj = compile(chart_file,'','exec')
                loop = False
                package = ''
            except Exception as e:
                if 'No module named ' in e.__str__():
                    import subprocess
                    import sys
                    package = e.__str__()[17:-1]
                    if package == last_package or (not autoinstall):
                        import_error = True
                        loop = False
                        data['error'] = True
                        data['error_message'] = e.__str__()
                    else:
                        last_package = package
                        try:
                            if settings.PYTHON_PATH:
                                subprocess.check_call([settings.PYTHON_PATH, '-m', 'pip', 'install', package])
                            else:
                                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                        except Exception as e:
                            import_error = True
                            loop = False
                            data['error'] = True
                            data['error_message'] = e.__str__()
                else:
                    import_error = True
                    loop = False
                    data['error'] = True
                    data['error_message'] = e.__str__()
        if not import_error:
            exec(compileObj,chart_input_c)
            for key in list(chart_input.keys()):
                output_value = chart_input_c[key]
                if isinstance(output_value, list) or isinstance(output_value, dict):
                    output_value_str = json.dumps(output_value)
                else:
                    output_value_str = str(output_value)
                chart_input[key] = output_value_str
            data['error'] = False
    except:
        if package:
            data['error_message'] = '找不到符合的條件。' + package
        else:
            data['error_message'] = e.__str__()
        data['error'] = True
    

#Node群組
@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def createCollectorGroupAjax(request):
    postdata = getPostdata(request)
    name = postdata.get('name', '')
    description = postdata.get('description', '')
    group_type = postdata.get('group_type', '')
    if name:
        check = CollectorGroup.objects.filter(name=name).count()
        if check == 0:
            CollectorGroup.objects.create(name=name, description=description, type=group_type)
            return ResponseAjax(statusEnum.success, _('建立成功。')).returnJSON()
        else:
            return ResponseAjax(statusEnum.not_found, _('群組名稱重複。')).returnJSON()
    else:
        return ResponseAjax(statusEnum.error, _('請輸入群組名稱。')).returnJSON()
    
    
@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def updateCollectorGroupAjax(request):
    require_field = ['id','name']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    group_id = postdata.get('id', '')
    name  = postdata.get('name', '')
    description = postdata.get('description', '')
    group_type = postdata.get('group_type', '')
    if checker.get('status') == 'success':
        try:
            CollectorGroup.objects.filter(id=group_id).update(name=name, description=description, type=group_type)
            return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()
        except:
            return ResponseAjax(statusEnum.error, _('更新失敗。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def deleteCollectorGroupAjax(request):
    require_field = ['id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    group_id_list = postdata.get('id', '')
    if checker.get('status') == 'success':
        if not Collector.objects.filter(nodegroup_id__in=group_id_list):
            if '1' not in group_id_list:
                try:
                    CollectorGroup.objects.filter(id__in=group_id_list).delete()
                    OmParameter.objects.filter(group_id__in=group_id_list).delete()
                    return ResponseAjax(statusEnum.success, _('刪除成功。')).returnJSON()
                except:
                    return ResponseAjax(statusEnum.error, _('刪除失敗。')).returnJSON()
            else:
                return ResponseAjax(statusEnum.error, _('刪除失敗：未分類群組無法刪除。')).returnJSON()
        else:
            return ResponseAjax(statusEnum.error, _('刪除失敗：所選群組中還有尚未移出的收集器，請移至其他群組再進行刪除。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def listCollectorGroupAjax(request):
    field_list = ['name__icontains']
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    if datatable:
        display_field =['id','name','description','type']
        query = CollectorGroup.objects.filter().values(*display_field)
        result = DatatableBuilder(request, query, field_list)
        #燈號
        data = result['data']
        group_id_list = []
        group_dict = {}
        collector_id_list = []
        collector_dict = {}
        if not isinstance(data, str):
            for k in data:
                if isinstance(k, int):
                    row = data[k]
                else:
                    row = k
                group_id_list.append(row['id'])
                group_dict[row['id']] = []
            collector_list = list(Collector.objects.filter(nodegroup_id__in=group_id_list).values('id','nodegroup_id'))
            for collector in collector_list:
                collector_id_list.append(collector['id'])
                collector_dict[collector['id']] = collector['nodegroup_id']
            em_list = list(EventManagement.objects.filter(collector_id__in=collector_id_list,closed=False).values('collector_id').annotate(Max('critical')))
            for em in em_list:
                group_dict[collector_dict[em['collector_id']]].append(em['critical__max'])
            for k in data:
                if isinstance(k, int):
                    row = data[k]
                else:
                    row = k
                if group_dict[row['id']]:
                    row['level'] = max(group_dict[row['id']])
                else:
                    row['level'] = 1
        info('%s list CollectorGroup success.' % request.user.username,request)
        return JsonResponse(result)
    else:
        result = list(CollectorGroup.objects.filter().values())
        info('%s list CollectorGroup success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


#事件管理
@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def createEventAjax(request):
    '''
    create event.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #server side rule check
    require_field = ['source']
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        ce_res = createEvent(postdata)
        if ce_res['status']:
            info('%s create Event success.' % request.user.username,request)
            return ResponseAjax(statusEnum.success, ce_res['message']).returnJSON()
        else:
            info('%s create Event error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, ce_res['message']).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def  createEvent(param):
    '''
    建立事件方法
    '''
    try:
        #function variable
        status = True
        message = _('建立成功。')
        title = param.get('title','')
        content = param.get('content','')
        critical = param.get('critical','')
        collector_id = param.get('collector_id','')
        source = param.get('source','')
        source2 = param.get('source2','')
        EventManagement.objects.create(title=title,content=content,critical=critical,collector_id=collector_id,source=source,source2=source2)
        #如果是sla，發信件
        if source == 'sla':
            users = param.get('users','')
            sendEmail(title, content, users)
        #轉開事故
        inc = FlowActiveGlobalObject.NameSearch('事故管理', None, '服務管理')
        model = getModel('omformmodel', 'Omdata_' + inc.flow_uuid.hex)
        inc_rule = json.loads(loadIncidentRule())['event_result']
        for row in inc_rule:
            conditions = row['event_result_compare']
            #首先判斷條件是否成立
            ec = evalCondition('INC', conditions, param)
            if ec:
                #接著判斷是否符合時間內開多少張單
                event_unit = row.get('event_unit','')
                event_freq = row.get('event_freq','')
                event_time = row.get('event_time','')
                if event_freq and event_time and event_unit:
                    if event_unit == 'sec':
                        search_time = datetime.now() - timedelta(seconds=int(event_time))
                    elif event_unit == 'min':
                        search_time = datetime.now() - timedelta(minutes=int(event_time))
                    elif event_unit == 'hour':
                        search_time = datetime.now() - timedelta(hours=int(event_time))
                    else:
                        search_time = datetime.now() - timedelta(days=int(event_time))
                    em_c = EventManagement.objects.filter(source2=source2,createtime__gte=search_time).count()
                    if em_c == int(event_freq):
                        check = True
                    else:
                        check = False
                else:
                    check = True
                if check:
                    inc_source = row['event_name'] + '<' + source2 + '>'
                    if model.objects.filter(formitm_26=inc_source).exists():
                        pass
                    else:
                        from omformflow.views import createOmData
                        formdata = []
                        formdata.append({'id':'FORMITM_25','type':'inputbox','value':'system'})
                        formdata.append({'id':'FORMITM_28','type':'h_title','value':row['title']})
#                         formdata.append({'id':'title','type':'header','value':row['title']})
                        formdata.append({'id':'FORMITM_2','type':'areabox','value':row['content']})
                        formdata.append({'id':'FORMITM_14','type':'list','value':row['impact']})
                        formdata.append({'id':'FORMITM_15','type':'list','value':row['urgency']})
                        formdata.append({'id':'FORMITM_16','type':'list','value':row['priority']})
                        formdata.append({'id':'FORMITM_10','type':'h_level','value':row['critical']})
#                         formdata.append({'id':'level','type':'header','value':row['critical']})
                        formdata.append({'id':'FORMITM_17','type':'list','value':'event_esc'})
                        formdata.append({'id':'FORMITM_3','type':'h_status','value':0})
#                         formdata.append({'id':'status','type':'header','value':'新建'})
                        formdata.append({'id':'FORMITM_4','type':'h_group','value':{'group': row['group'], 'user': row['user']}})
#                         formdata.append({'id':'group','type':'header','value':{'group': row['group'], 'user': row['user']}})
                        formdata.append({'id':'FORMITM_26','type':'inputbox','value':inc_source})
                        omdata = {}
                        omdata['flow_uuid'] = inc.flow_uuid.hex
                        omdata['formdata'] = formdata
                        createOmData(omdata)
                    break
    except Exception as e:
        status = False
        message = _('建立失敗：') + e.__str__()
    finally:
        return {'status':status,'message':message}


def sendEmail(title, content, users):
    try:
        mail = FlowActiveGlobalObject.NameSearch('發送流程', None, '內建流程')
        from omformflow.views import createOmData
        formdata = []
        formdata.append({'id':'FORMITM_2','type':'inputbox','value':users})
        formdata.append({'id':'FORMITM_3','type':'inputbox','value':title})
        formdata.append({'id':'FORMITM_8','type':'areabox','value':content})
        omdata = {}
        omdata['flow_uuid'] = mail.flow_uuid.hex
        omdata['formdata'] = formdata
        createOmData(omdata)
    except Exception as e:
        error(e.__str__())


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def closeEventAjax(request):
    '''
    close event.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #server side rule check
    require_field = ['source']
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        source = postdata.get('source','')
        node_list = postdata.get('node',[])
        ce_res = closeEvent(node_list, source)
        if ce_res['status']:
            info('%s create Event success.' % request.user.username,request)
            return ResponseAjax(statusEnum.success, ce_res['message']).returnJSON()
        else:
            info('%s create Event error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, ce_res['message']).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def  closeEvent(collector_list, source):
    '''
    關閉事件方法
    '''
    try:
        #function variable
        status = True
        message = _('更新成功。')
        if isinstance(collector_list, str):
            collector_list = json.loads(collector_list)
        EventManagement.objects.filter(collector_id__in=collector_list,source=source,closed=False).update(closed=True)
    except Exception as e:
        status = False
        message = _('更新失敗：') + e.__str__()
    finally:
        return {'status':status,'message':message}
        return ResponseAjax(statusEnum.error, _('請輸入群組名稱')).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def listEventAjax(request):
    '''
    list event.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    field_list=['title__icontains','source__icontains']
    query = ''
    #get post data
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    createtime = postdata.get('createtime','')
    closed = postdata.get('closed',[1,0])
    if datatable:
#         display_field =['id','title','critical','content','source','createtime']
        query = EventManagement.objects.filter(closed__in=closed,createtime__lte=createtime).values()
        result = DatatableBuilder(request, query, field_list)
        info('%s list event success.' % request.user.username,request)
        return JsonResponse(result)
    else:
        #尚無功能使用
        result = list(EventManagement.objects.filter(closed__in=closed).values())
        info('%s list event success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功。'), result).returnJSON()


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def editIncidentRuleAjax(request):
    '''
    edit incident rule.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #server side rule check
    require_field = ['rule']
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        eir = editIncidentRule(postdata)
        if eir['status']:
            info('%s edit incident rule success.' % request.user.username,request)
            return ResponseAjax(statusEnum.success, eir['message']).returnJSON()
        else:
            info('%s edit incident rule error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, eir['message']).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()


def editIncidentRule(param):
    '''
    編輯事件轉開事故規則
    '''
    try:
        #function variable
        status = True
        message = _('更新成功。')
        rule = param.get('rule','{}')
        incidentrule = IncidentRule(id=1,rule=rule)
        incidentrule.save()
    except Exception as e:
        status = False
        message = _('更新失敗：') + e.__str__()
    finally:
        return {'status':status,'message':message}


@login_required
@permission_required('ommonitor.OmMonitor_Manage','/api/permission/denied/')
@try_except
def loadIncidentRuleAjax(request):
    '''
    load incident rule.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #server side rule check
    result = loadIncidentRule()
    info('%s load incident rule success.' % request.user.username,request)
    return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()


def loadIncidentRule():
    '''
    讀取事件轉開事故規則
    '''
    result = list(IncidentRule.objects.all().values_list('rule',flat=True))
    if result:
        result = result[0]
    else:
        result = '{}'
    return result