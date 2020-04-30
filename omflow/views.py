'''
django view for omflow
@author: Pen Lin
'''
import json, logging, os, shutil, threading
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from omflow.syscom.message import ResponseAjax, statusEnum
from omflow.global_obj import GlobalObject
from omflow.models import SystemSetting
from django.http.response import JsonResponse, StreamingHttpResponse
from django.contrib import auth
from datetime import datetime, timedelta
from importlib import import_module
from django.urls.base import resolve
from ommessage.models import MessageHistoryFiles
from omflow.syscom.common import try_except, DatatableBuilder, DataChecker,check_ldap_app
from django.conf import settings
from omflow.syscom.default_logger import critical, info, error, debug
from django.http import QueryDict
from omuser.models import OmUser
from omformflow.models import OmdataFiles
from ommission.models import Missions
from django.db.models import Q
from django.db.models.aggregates import Max

#app variable
default_folder = ['syssetting','staffmgmt','flowmgmt','mymission','servicemanage','servermanage','service']


@login_required
def home(request):
    '''
    omflow home page
    input:request
    return: home.html
    author:Pen Lin
    '''
    return render(request, "home.html")


@login_required
def filePage(request):
    '''
    omflow file page
    input:request
    return: file_manage.html
    author:Pei lin
    ''' 
    if request.user.is_superuser:
        file_app = {'ommessage','omformflow'}
        app_name = settings.INSTALLED_APPS
        app_name = [e for e in app_name if e in file_app]
        return render(request, "file_manage.html", locals())
    else:
        return render(request,"403.html")


@login_required
def sidebarManagementPage(request):
    '''
    omflow sidebar management page
    input:r equest
    return: sidebar_design.html
    author: Kolin Hsu
    ''' 
    return render(request, "sidebar_design.html")


@csrf_exempt
def restapi(request,url):
    '''
    omflow api home page
    input: request
    return: json
    author: Kolin Hsu
    ''' 
    #check url
    try:
        if url[-1] == '/':
            new_url = '/'+url
        else:
            new_url = '/'+url+'/'
        module_name = resolve(new_url).func.__module__
        method = resolve(new_url).url_name
    except:
        return ResponseAjax(statusEnum.no_permission ,  _('網址錯誤，請確認後重新發送請求')).returnJSON()
    #get post data
    postdata = json.loads(request.body.decode("utf-8"))
    security = postdata.pop('security')
    #postdata = inputJson.get('postdata', '')
    if security is not None:
        securityObj = GlobalObject.__securityObj__.get(security)
        if securityObj is not None:
            #check security expired or not
            expired_datetime = securityObj['updatetime'] + timedelta(minutes=5)
            if datetime.now() < expired_datetime:
                #get user name and password
                username = securityObj['username']
                #update security expired_datetime
                GlobalObject.__securityObj__[security]['updatetime'] = datetime.now()
                GlobalObject.__userObj__[username] = GlobalObject.__securityObj__[security]
                #user login
                user = OmUser.objects.get(username__icontains=username)
                auth.login(request, user)
                #trans dict to query dict
                query_dict_postdat = QueryDict('', mutable=True)
                query_dict_postdat.update(postdata)
                #cover request post
                request.POST=query_dict_postdat
                module = import_module(module_name)
                output = getattr(module, method)(request)
                #logout user when api down
                auth.logout(request)
                return output
            else:
                return ResponseAjax(statusEnum.no_permission ,  _('授權碼過期，請重新登入')).returnJSON()
        else:
            return ResponseAjax(statusEnum.no_permission ,  _('授權碼錯誤，請確認授權碼或重新登入取得新的授權碼')).returnJSON()
    else:
        return ResponseAjax(statusEnum.no_permission ,  _('取得授權碼失敗，請提供授權碼或登入取得授權碼')).returnJSON()
    
 
@login_required
def systemPage(request):
    '''
    system config page
    input:request
    return: system.html
    author:Jia Liu
    ''' 
    if request.user.is_superuser:
        is_ldap = check_ldap_app
        return render(request, "system_config.html", locals())
    else:
        return render(request,"403.html")
   

@login_required
@try_except
def loadSystemConfigAjax(request):
    '''
    show system log level
    input: request
    return: log level
    author: Kolin Hsu
    '''
    if request.user.is_superuser:
        result = {}
        POOL_MAX_WORKER = SystemSetting.objects.get(name='pool_max_worker').value
        PI_agree = SystemSetting.objects.get(name='PI_agree').value
        SU_agree = SystemSetting.objects.get(name='SU_agree').value
        loglevel = logging.getLevelName(logging.getLogger('django').getEffectiveLevel())
        ldapstr = SystemSetting.objects.get(name='ldap_config').value
        ldap_config = json.loads(ldapstr)
        settingsloglevel = settings.LOG_LEVEL
        result['LOG_LEVEL'] = loglevel
        result['POOL_MAX_WORKER'] = POOL_MAX_WORKER
        result['settings_log_level'] = "Log level is already changed,settings LEVEL is " +settingsloglevel
        result['ldap_config'] = ldap_config
        result['PI_agree'] = PI_agree
        result['SU_agree'] = SU_agree
        #told front end which field has been modified
        if loglevel != settings.LOG_LEVEL:
            result['Level_Change'] = True
        else:
            result['Level_Change'] = False
        info(request ,'%s load SystemConfig success.' % request.user.username)
        return ResponseAjax(statusEnum.success , _('讀取成功'), result).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission , _('您沒有權限進行此操作。'), result).returnJSON()

@login_required
@try_except
def updateSystemConfigAjax(request):
    '''
    change system log level
    input: request
    return: log level
    author: Jia Liu
    '''
    if GlobalObject.__statusObj__["ldapRunning"] == False:
        GlobalObject.__statusObj__["ldapRunning"] = True
        #function variable
        ldapdata = {}
        #get postdata
        postdata = request.POST
        POOL_MAX_WORKER = postdata.get('POOL_MAX_WORKER', '')
        PI_agree = postdata.get('PI_agree', '')
        SU_agree = postdata.get('SU_agree', '')
        ldap_client_server = postdata.get('ldap_client_server','')
        ldap_client_server_port = postdata.get('ldap_client_server_port','')
        ldap_base_dn = postdata.get('ldap_base_dn','')
        ldap_bind_user = postdata.get('ldap_bind_user','')
        ldap_bind_user_password = postdata.get('ldap_bind_user_password','')
        ldap_client_domain = postdata.get('ldap_client_domain','')
        loglevel = postdata.get('LOG_LEVEL', '')
        #set log level
        loglevel_ex = logging.getLevelName(logging.getLogger('django').getEffectiveLevel())
        if loglevel and loglevel != loglevel_ex:
            #設定django log level
            logging.getLogger('django').setLevel(loglevel)
            #設定omflow log level
            logging.getLogger('omflowlog').setLevel(loglevel)
            critical(request,'LOG等級已經改為 %s' % loglevel)
        #set pool max worker
        SystemSetting.objects.filter(name='pool_max_worker').update(value=POOL_MAX_WORKER)
        SystemSetting.objects.filter(name='PI_agree').update(value=PI_agree)
        SystemSetting.objects.filter(name='SU_agree').update(value=SU_agree)
        #set ldap
        ldapdata['ldap_client_server'] = ldap_client_server
        ldapdata['ldap_client_server_port'] = ldap_client_server_port
        ldapdata['ldap_base_dn'] = ldap_base_dn
        ldapdata['ldap_bind_user'] = ldap_bind_user
        ldapdata['ldap_bind_user_password'] = ldap_bind_user_password
        ldapdata['ldap_client_domain'] = ldap_client_domain
        GlobalObject.__ldapObj__['ldap_client_server'] = ldap_client_server
        GlobalObject.__ldapObj__['ldap_client_server_port'] = ldap_client_server_port
        GlobalObject.__ldapObj__['ldap_client_domain'] = ldap_client_domain
        ldapdata_str = json.dumps(ldapdata)
        ldap_config = SystemSetting.objects.filter(name="ldap_config")
        if ldap_config[0].value != ldapdata_str:
            ldap_config.update(value=ldapdata_str)
            #sync ldap
            if check_ldap_app():
                from omldap.ldap_config import syncLDAP
                t = threading.Thread(target=syncLDAP)
                t.start()
        else:
            GlobalObject.__statusObj__["ldapRunning"] = False
        info(request ,'%s update SystemConfig success.' % request.user.username)
        return ResponseAjax(statusEnum.success , _('更新成功')).returnJSON()
    else:
        info(request ,'%s update SystemConfig error.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission , _('LDAP更新正在執行')).returnJSON()


@login_required
@try_except
def listFilesAjax(request):
    '''
    list files
    input: request
    return: list
    author: Kolin Hsu
    '''
    if request.user.is_superuser:
        #function variable
        field_list = []
        query = ''
        #server side rule check
        require_field = ['app_name']
        postdata = request.POST
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            #get post data
            app_name = postdata.get('app_name','')
            createtime = postdata.get('createtime','')
            if app_name == 'ommessage':
                field_list=['file__icontains']
                query = MessageHistoryFiles.objects.filter(delete=False,createtime__lte=createtime).values('file','size','createtime','main_id')
            if app_name == 'omformflow':
                field_list=['file__icontains']
                query = OmdataFiles.objects.filter(delete=False,createtime__lte=createtime).values('file','size','createtime')
            if field_list or query:
                result = DatatableBuilder(request, query, field_list)
                info(request ,'%s list file success.' % request.user.username)
                return JsonResponse(result)
            else:
                info(request ,'%s list file error.' % request.user.username)
                return ResponseAjax(statusEnum.error, _('請提供正確的APP名稱')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


@login_required
@try_except
def deleteFilesAjax(request):
    '''
    delete files
    input: request
    return: status
    author: Kolin Hsu
    '''
    if request.user.is_superuser:
        #server side rule check
        require_field = ['app_name','path[]']
        postdata = request.POST
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            #get post data
            app_name = postdata.get('app_name','')
            path_list = postdata.getlist('path[]','')
            if app_name == 'ommessage':
                for path in path_list:
                    file_path = os.path.join(settings.MEDIA_ROOT, path)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        messagehistoryfile = MessageHistoryFiles.objects.get(file=path)
                        messagehistoryfile.delete = True
                        messagehistoryfile.save()
            info(request ,'%s delete file success.' % request.user.username)
            return ResponseAjax(statusEnum.success, _('檔案刪除成功')).returnJSON()
        else:
            info(request ,'%s missing some require variable or the variable type error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


@login_required
@try_except
def getDiskStatusAjax(request):
    '''
    check server disk space enough or not
    input: request
    return: boolean
    author: Kolin Hsu
    '''
    file_size = int(request.POST.get('file_size','0'))
    disk_obj = shutil.disk_usage("/")
    disk_free = disk_obj.free // (2**20)
    if disk_free - file_size > 10:
        result = True
    else:
        result = False
    info(request ,'%s get disk status success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('請求成功'), result).returnJSON()
    
    
def noPermissionPage(request):
    '''
    403 page
    input: request
    return: 403.html
    author: Kolin Hsu
    '''
    return render(request, '403.html')


def permissionDenied(request):
    '''
    return permission denied
    input: request
    return: json
    author: Kolin Hsu
    '''
    info(request ,'%s has no permission.' % request.user.username)
    return ResponseAjax(statusEnum.no_permission ,  _('您沒有權限進行此操作。')).returnJSON()


@login_required
@try_except
def loadWorkinfoAjax(request):
    '''
    show workinfo
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get new workinfo data
    messages = request.user.messagebox_set.filter(read=0).count()
    #mission
    #取得我(群組)曾經處理過的任務
    my_group_id_list = list(request.user.groups.all().values_list('id',flat=True))
    mission_list = list(Missions.objects.filter((Q(assignee_id=request.user.id) | (Q(assign_group_id__in=my_group_id_list) & Q(assignee_id=None)) | Q(create_user_id=request.user.username) | Q(update_user_id=request.user.username)) & Q(history=True)).values('flow_uuid','data_no'))
    #將查詢結果分為兩個list  建立對照的dict--(以flow_uuid為KEY，該流程的單號組成list為VALUE)
    flow_uuid_list = []
    data_no_list = []
    mapping_dict = {}
    for i in mission_list:
        mapping_data_no_list = mapping_dict.get(i['flow_uuid'],[])
        mapping_data_no_list.append(i['data_no'])
        if len(mapping_data_no_list) == 1:
            mapping_dict[i['flow_uuid']] = mapping_data_no_list
        flow_uuid_list.append(i['flow_uuid'])
        data_no_list.append(i['data_no'])
    #將所有flow_uuid_list、data_no_list組合的max id查出來
    max_mission_list = list(Missions.objects.filter(flow_uuid__in=flow_uuid_list,data_no__in=data_no_list).values('flow_uuid','data_no').annotate(max_id=Max('id')))
    #透過對照dict找出真正該撈出來的max id
    max_id_list = []
    for m in max_mission_list:
        mapping_no_list = mapping_dict.get(m['flow_uuid'],None)
        if m['data_no'] in mapping_no_list:
            max_id_list.append(m['max_id'])
    missions = Missions.objects.filter(id__in=max_id_list).count()
    result = {'messages':messages, 'missions':missions}
    debug(request ,'%s load workinfo success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('更新成功'), result).returnJSON()



@login_required
@try_except
def loadSidebarDesignAjax(request):
    '''
    load left side bar design json
    input: request
    return: json
    author: Kolin Hsu
    '''
    if request.user.is_superuser:
        #function variable
        result = {}
        count = 0
        sidebar_design = GlobalObject.__sidebarDesignObj__['sidebar_design']
        #get item id count
        for item in sidebar_design:
            flow_uuid = item['flow_uuid']
            if flow_uuid == 'custom':
                item_id = int(item['id'][7:])
                if item_id > count:
                    count = item_id
        result['sidebar_design'] = sidebar_design
        result['count'] = count
        info(request ,'%s load SidebarDesign success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功'), result).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
    

@login_required
@try_except
def updateSidebarDesignAjax(request):
    '''
    update left side bar design json
    input: request
    return: json
    author: Kolin Hsu
    '''
    if request.user.is_superuser:
        #function variable
        default_count = 0
        name_list = []
        check = True
        error_message = '參數錯誤：'
        #server side rule check
        postdata = request.POST
        #get postdata
        format_str = postdata.get('format','')
        format_list = json.loads(format_str)
        #check server has install app or not
        for format_obj in format_list:
            format_id = format_obj.get('id')
            format_name = format_obj.get('name')
            p_id = format_obj.get('p_id')
            flow_uuid = format_obj.get('flow_uuid')
            if flow_uuid == 'default' or flow_uuid == 'custom':
                if format_name in name_list:
                    check = False
                    error_message += '重複名稱 -- ' + format_name
                    break
                else:
                    name_list.append(format_name)
            else:
                name_list.append(format_name)
            if flow_uuid == 'default':
                if p_id:
                    check = False
                    error_message += '無法移動預設選單至選單第二層。'
                    break
                if format_id not in default_folder:
                    check = False
                    error_message += '無法新增預設類型選單。'
                    break
                default_count += 1
            elif flow_uuid == 'custom':
                if p_id in default_folder:
                    check = False
                    error_message += '無法在預設選單內新增選項。'
                    break
        if check:
            if default_count == len(default_folder):
                systemsetting = SystemSetting.objects.get(name='sidebar_design')
                #取得舊的設計，並取得所有flow
                flow_list = []
                ex_sidebar_design = json.loads(systemsetting.value)
                for ex_sidebar_item in ex_sidebar_design:
                    if ex_sidebar_item['id'][:8] == 'formflow':
                        flow_list.append(ex_sidebar_item)
                #把flow丟入新的設計
                new_sidebar_design = []
                for new_sidebar_item in format_list:
                    new_sidebar_design.append(new_sidebar_item)
                    if new_sidebar_item['flow_uuid'] == 'app':
                        for flow in flow_list:
                            if flow['p_id'] == new_sidebar_item['id']:
                                new_sidebar_design.append(flow)
                #update database
                sidebar_design_str = json.dumps(new_sidebar_design)
                systemsetting.value = sidebar_design_str
                systemsetting.save()
                #update global object
                updatetime = datetime.now()
                GlobalObject.__sidebarDesignObj__['sidebar_design'] = new_sidebar_design
                GlobalObject.__sidebarDesignObj__['design_updatetime'] = updatetime
                info(request ,'%s update SidebarDesign success.' % request.user.username)
                return ResponseAjax(statusEnum.success, _('更新成功')).returnJSON()
            else:
                info(request ,'%s update SidebarDesign error.' % request.user.username)
                error_message += '無法刪除預設項目。'
                return ResponseAjax(statusEnum.not_found, error_message).returnJSON()
        else:
            info(request ,'%s update SidebarDesign error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, error_message).returnJSON()
    else:
        info(request ,'%s has no permission.' % request.user.username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
    

@login_required
@try_except
def loadLSideAjax(request):
    '''
    load left side bar design json for request user
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['draw_$']
    mission = []
    sidebar = []
    request.session.set_expiry(130)
    #server side rule check
    postdata = request.POST
    data_checker = DataChecker(postdata, require_field)
    if data_checker.get('status') == 'success':
        #get mission
        group_id_list = list(request.user.groups.all().values_list('id',flat=True))
        level_list = list(Missions.objects.filter((Q(assignee_id=request.user.id) | (Q(assign_group_id__in=group_id_list) & Q(assignee_id=None))) & Q(history=False)).values_list('level',flat=True))
        green = 0
        red = 0
        yellow = 0
        for i in level_list:
            if i == 'green':
                green += 1
            elif i == 'yellow':
                yellow += 1
            elif i == 'red':
                red += 1
            elif i == None or i == '':
                green +=1
        mission.append(red)
        mission.append(yellow)
        mission.append(green)
        #get sidebar
        draw = int(postdata.get('draw_$',''))
        sidebar_design = GlobalObject.__sidebarDesignObj__['sidebar_design']
        if draw == 1:
            reviseLside(request, sidebar, sidebar_design)
        else:
            #get session object
            lside_design = request.session.get('lside_design','')
            session_updatetime = request.session.get('design_updatetime','')
            #get global object
            design_updatetime = GlobalObject.__sidebarDesignObj__['design_updatetime']
            permission_updatetime = GlobalObject.__sidebarDesignObj__['permission_updatetime']
            #compare updatetime
            if session_updatetime < str(design_updatetime) or session_updatetime < str(permission_updatetime):
                #compare two json array equal or not
                if lside_design != sidebar_design:
                    reviseLside(request, sidebar, sidebar_design)
                else:
                    sidebar = ''
            else:
                sidebar = ''
        result = {'sidebar':sidebar,'mission':mission}
        debug(request ,'%s load LSide success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('讀取成功'), result).returnJSON()
    else:
        debug(request ,'%s missing some require variable or the variable type error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found, data_checker.get('message'), data_checker).returnJSON()


def reviseLside(request, sidebar, sidebar_design):
    updatetime = str(datetime.now())
    temp = []
    app_id_list = []
    #把所有app custom default以及符合權限的flow都放入temp
    for item in sidebar_design:
        flow_uuid = str(item['flow_uuid'])
        permission_code_name = 'omformmodel.Omdata_' + flow_uuid + '_View'
        if flow_uuid == 'default' or flow_uuid == 'custom' or flow_uuid == 'app':
            temp.append(item)
        elif request.user.has_perm(permission_code_name):
            temp.append(item)
            p_id = item['p_id']
            app_id_list.append(p_id)
    #把沒有flow的app從temp移除
    for i in temp:
        flow_uuid = str(i['flow_uuid'])
        if flow_uuid == 'app':
            if i['id'] in app_id_list:
                sidebar.append(i)
        else:
            sidebar.append(i)
    #set session object
    request.session['lside_design'] = sidebar
    request.session['design_updatetime'] = updatetime


@login_required
@try_except
def listSidebarDesignAjax(request):
    '''
    list left side bar custom item
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    result = []
    sidebar_design = GlobalObject.__sidebarDesignObj__['sidebar_design']
    for item in sidebar_design:
        if item['flow_uuid'] == 'custom':
            result.append(item)
    info(request ,'%s list SidebarDesign success.' % request.user.username)
    return ResponseAjax(statusEnum.success, _('讀取成功'), result).returnJSON()


@login_required
@try_except
def ldapCheckConnectAjax(request):
    '''
    use ldap3 check connection
    input: use bind_user to connect LDAP 
    return: connection status
    author: Jia Liu
    ''' 
    if check_ldap_app():
        from omldap.views import ldapCheckConnect 
        result = ldapCheckConnect(request)
        if result["status"] == "success":
            info(request ,'%s ldap Check Connect success.' % request.user.username)
            return ResponseAjax(statusEnum.success, result['message']).returnJSON()
        else:
            info(request ,'%s ldap Check Connect error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
    else:
        info(request ,'%s ldap Check Connect error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found , _('您尚未安裝omldap APP,請聯絡原廠')).returnJSON()       


@login_required
@try_except    
def ldapManualSyncAjax(request):
    '''
    LDAP manual Sync
    input: execute LDAP functions
    return: messages
    author: Pei Lin
    ''' 
    if check_ldap_app():
        from omldap.views import ldapManualSync 
        result = ldapManualSync(request)
        if result["status"] == "success":
            info(request ,'%s ldap Check Connect success.' % request.user.username)
            return ResponseAjax(statusEnum.success, result['message']).returnJSON()
        elif result["status"] == "fail":
            info(request ,'%s ldap Check Connect error.' % request.user.username)
            return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
        else:
            info(request ,'%s ldap Check Connect error.' % request.user.username)
            return ResponseAjax(statusEnum.no_permission, result['message']).returnJSON()
    else:
        info(request ,'%s ldap Check Connect error.' % request.user.username)
        return ResponseAjax(statusEnum.not_found , _('您尚未安裝omldap APP,請聯絡原廠')).returnJSON() 


@login_required
def myformpage(request, url):
    '''
    system config page
    input:request
    return: system.html
    author:Jia Liu
    ''' 
    flow_uuid = url.split('/')[0]
    data_no = url.split('/')[1]
    data_id = url.split('/')[2]
    return render(request, "myform.html", locals())


@login_required
@try_except
def downloadHistoryFilesAjax(request, path):
    '''
    download file
    input: request
    return: file
    author: Kolin Hsu
    '''
    def file_iterator(file_path, chunk_size=1024*512):
        with open(file_path, 'rb') as file:
            while True:
                c_file = file.read(chunk_size)
                if c_file:
                    yield c_file
                else:
                    break
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream' 
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
