import re, json, operator
from omformflow.views import createOmData
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext as _
from omflow.syscom.default_logger import info,error
from omflow.syscom.common import try_except, DataChecker, getPostdata, Translator
from omflow.syscom.message import ResponseAjax, statusEnum
from omservice.models import OmService, OmServiceDesign
from omformflow.models import FlowActive
from django.db.models import Max
from omflow.global_obj import FlowActiveGlobalObject
from omformflow.models import ActiveApplication
from django.utils.translation import get_language

#SubQuery
from omflow.syscom.common import searchConditionBuilder, DatatableBuilder, getModel
from _functools import reduce
from omflow.syscom.common import datatableValueToText
from django.http.response import JsonResponse

@login_required
def servicePage(request):
    return render(request, 'list.html')


@login_required
@permission_required('omservice.OmServiceDesign_Manage','/api/permission/denied/')
@try_except
def saveServiceAjax(request):
    '''
    save manager's service setting
    input: request
    return: json
    author: Arthur
    '''
    #Server Side Rule Check
    username = request.user.username
    postdata = getPostdata(request)

    if username:
        require_field = ['content']
        checker = DataChecker(postdata, require_field)

        if checker.get('status') == 'success':

            #是否存入翻譯
            lan_package = postdata.get('lan_package', None)
            if lan_package:
                FlowActiveGlobalObject.setSysLanDict("service", None, lan_package)
            
            #static variable
            box_object = json.loads(postdata.get('content', ''))
            OmServiceDesign.objects.create(content=json.dumps(box_object),language_package=json.dumps(FlowActiveGlobalObject.getSysLanDict('service')))
            
            OmService.objects.all().delete();
            
            ServiceList = []
            for key in box_object["list"]:
                thisSer = box_object["list"][key]
                if thisSer["type"]=="service":
                    flow_uuid = FlowActiveGlobalObject.APIgetUUID(thisSer['api_path'])
                    ser = OmService(service_id=thisSer['id'],flow_uuid=flow_uuid,role=thisSer['setting']['setRole'],default_value=json.dumps(thisSer['default_value']))
                    ServiceList.append(ser)
            
            OmService.objects.bulk_create(ServiceList)
            
            info('%s update Service success' % username,request)
            return ResponseAjax(statusEnum.success, _('儲存成功。')).returnJSON()
        else:
            info('%s update Service error' % username,request)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info('%s update Service with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


@login_required
@try_except
def loadServiceAjax(request):
    '''
    load manager's service setting
    return: json
    author: Arthur
    '''
    
    #Server Side Rule Check
    username = request.user.username
    postdata = getPostdata(request)
    result = {}
    if username:
        #static variable
#         result['structure'] = OmServiceDesign.objects.all()
#         if request.user.has_perm('omservice.OmServiceDesign_Manager'):
#             result['objects'] = OmService.objects.all()
#         else:
#             #等待修改
#             user_role_list = list(request.user.groups.all().values_list('id', flat=True))
#             for service_obj in OmService.objects.all():
#                 service_role_list = json.loads(service_obj.get('role','[]'))
#                 if len(set(user_role_list) & set(service_role_list)):
#                     result['objects'].append(service_obj)
        #print(OmServiceDesign.objects.all().count())
        if OmServiceDesign.objects.all().count()>0:
            max = OmServiceDesign.objects.all().aggregate(Max('id')).get('id__max')
            result = list(OmServiceDesign.objects.filter(id=max).values('content'))

            box_object = json.loads(result[0]["content"])
            
            #檢查權限
            if request.user.has_perm('omservice.OmServiceDesign_Manage'):
                pass;
            else: 
                Service_List = list(OmService.objects.all())
                Group_List = list(request.user.groups.all().values_list('id', flat=True))
                if len(Group_List):
                    Group_List.append(-1)
                else:
                    Group_List = [-1]
                for thisSer in Service_List:
                    if len(set(json.loads(thisSer.role)) & set(Group_List))==0:
                        del box_object["list"][str(thisSer.service_id)]
                
            #檢查是否過期
            this_activeList = list(FlowActive.objects.filter(undeploy_flag=0,parent_uuid__isnull=True).values_list('flow_uuid', flat=True))
            this_activeList = [o.hex for o in this_activeList]
            for idx in box_object["list"]:
                #print(box_object["list"][idx])
                if box_object["list"][idx]["type"]=="service" :
                    if 'api_path' in box_object["list"][idx]:
                        flow_uuid = FlowActiveGlobalObject.APIgetUUID(box_object["list"][idx]["api_path"])
                    else:
                        flow_uuid = box_object["list"][idx]["flow_uuid"]
                        box_object["list"][idx]["api_path"] = FlowActiveGlobalObject.UUIDgetAPI(flow_uuid)
                        
                    if flow_uuid in this_activeList:
                        box_object["list"][idx]["available"] = 1
                    else:
                        box_object["list"][idx]["available"] = 0
            
            #翻譯語言
            if postdata.get('type') != "source":
                language_type = get_language()
                #print(FlowActiveGlobalObject.getSysLanDict('service'))
                lan_package = FlowActiveGlobalObject.getSysLanDict('service').get(language_type,None)
                
                if lan_package:
                    for idx in box_object["list"]:
                        this_service = box_object["list"][idx]
                        if this_service["setting"]["setTitle"] :
                            this_service["setting"]["setTitle"] = lan_package[this_service["setting"]["setTitle"]] if checkJsonKey( lan_package, this_service["setting"]["setTitle"]) else this_service["setting"]["setTitle"]
                            
                        if this_service["type"]=="service" :
                            if this_service["setting"]["setTip"]:
                                this_service["setting"]["setTip"] = lan_package[this_service["setting"]["setTip"]] if checkJsonKey( lan_package, this_service["setting"]["setTip"]) else this_service["setting"]["setTip"]
                            for sup_idx in this_service["service"]["list"]:
                                this_step = this_service["service"]["list"][sup_idx]
                                if this_step["name"]:
                                    this_step["name"] = lan_package[this_step["name"]] if checkJsonKey( lan_package, this_step["name"] ) else this_step["name"]
                                if this_step["tip"]:
                                    this_step["tip"] = lan_package[this_step["tip"]] if checkJsonKey( lan_package, this_step["tip"] ) else this_step["tip"]
            
            #print(result[0]["content"])
            result[0]["content"] = json.dumps(box_object)            

        return ResponseAjax(statusEnum.success , _('讀取成功。'), result).returnJSON()
    else:
        error('%s load Service with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()

 
@login_required
#@permission_required('omservice.OmServiceDesign_Manage','/page/403/')        
@try_except
def getFormListAjax(request):
    '''
    load form_list
    return: json
    author: Arthur
    '''
    #Server Side Rule Check
    username = request.user.username
    result = {}
    if username:
        #static variable
        #omdata_list = list(filter(lambda x: re.match("^Omdata_.{32}$", x.__name__), apps.get_models()))
                 
        app = list(ActiveApplication.objects.filterformat('id','app_name',undeploy_flag=False))
        flow = list(FlowActive.objects.filterformat('id','flow_uuid','api_path','flow_name','flow_app_id',undeploy_flag=False,parent_uuid=None))
        result = {'app':app,'flow':flow}
        
        #翻譯
        lang = get_language()
        result['app'] = Translator('datatable_multi_app','active', lang, None,None).Do(result['app'])
        result['flow'] = Translator('datatable_multi_app','active', lang, None,None).Do(result['flow'])

        return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
    else:
        error('%s load form_list with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


@login_required
@try_except
def getFormObjAjax(request):
    '''
    load service_object's form_object
    return: json
    author: Arthur
    '''
    username = request.user.username
    postdata = getPostdata(request)
    result = {}
    
    if username:
        require_field = ['api_path']
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            flow_uuid = FlowActiveGlobalObject.APIgetUUID(postdata.get('api_path'))
            thisQuery = list(FlowActive.objects.filter(flow_uuid=flow_uuid,undeploy_flag=False).values('formobject','attachment'))
            if len(thisQuery):
                result = thisQuery[0]
                language = get_language()
                app_id = FlowActiveGlobalObject.UUIDSearch(flow_uuid).flow_app_id
                formobject = Translator('formobject','active', language, app_id, None).Do(result['formobject'])
                result['formobject'] = json.dumps(formobject)
        return ResponseAjax(statusEnum.success , _('讀取成功。'), result).returnJSON()
    else:
        error('%s get form_object with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()

         
@login_required
@try_except
def requestAjax(request):
    '''
    send user's service request
    return: json
    author: Arthur
    '''
    username = request.user.username
    postdata = request.POST.copy()
    files = request.FILES.getlist('files','')
    result = {}
    #print(postdata)
    if username:
        require_field = ['api_path','service_id','formdata']
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            #判斷權限
            postdata['flow_uuid'] = FlowActiveGlobalObject.APIgetUUID(postdata.get('api_path'))
            thisQuery = list(OmService.objects.filter(service_id=postdata.get('service_id')))
            if len(thisQuery):
                service_obj = thisQuery[0]
                #print(service_obj.default_value)
                service_obj = json.loads(service_obj.default_value)
                
                postdata["formdata"] = json.loads(postdata["formdata"])
                for default_col in service_obj:
                    postdata["formdata"].append(default_col)
                    
                postdata["formdata"] = json.dumps(postdata["formdata"])
            else:
                info('%s update Service error' % username,request)
                return ResponseAjax(statusEnum.error, _('查無此服務。')).returnJSON()
            
            result = createOmData(postdata,request.user.username,files)
            if result['status']:
                return ResponseAjax(statusEnum.success, result['message']).returnJSON()
            else:
                return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
        else:
            return ResponseAjax(statusEnum.not_found, _('缺少必填欄位。')).returnJSON()
    else:
        error('%s request_service with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
         
@login_required
@permission_required('omservice.OmServiceDesign_Manage','/api/permission/denied/')
@try_except
def importTranslationAjax(request):
    '''
    import service language package
    input: request
    return: json
    author: Arthur
    '''
    #function variable
    require_field = ['language']
    #server side rule check
    postdata = getPostdata(request)
    language_str = postdata.get('language_list','')
    language = postdata.get('language','')
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        #wa = WorkspaceApplication.objects.get(id=app_id)
        #language_dict = json.loads(wa.language_package)
        max = OmServiceDesign.objects.all().aggregate(Max('id')).get('id__max')
        this_service = OmServiceDesign.objects.get(id=max)
        language_dict = json.loads(this_service.language_package)
        
        temp_dict = {}
        language_list = language_str.split('\r\n')
        for line in language_list:
            if line:
                sp_index = line.find(':')
                if line[:sp_index] == 'original':
                    key = line[sp_index+1:]
                else:
                    temp_dict[key] = line[sp_index+1:]
        language_dict[language] = temp_dict
        language_str = json.dumps(language_dict)
        this_service.language_package = language_str
        this_service.save()
        #set global
        FlowActiveGlobalObject.setSysLanDict("service", language, temp_dict)
        info('%s import language package success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('匯入成功。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message',''), checker).returnJSON()
    

@login_required
@permission_required('omservice.OmServiceDesign_Manage','/api/permission/denied/')
@try_except
def exportTranslationAjax(request):
    '''
    export workspace application language package
    '''
    #function variable
    require_field = ['language']
    #get postdata
    postdata = getPostdata(request)
    language_type = postdata.get('language','')
    #server side rule check
    checker = DataChecker(postdata, require_field)
    if checker.get('status') == 'success':
        export = ''
        export_list = []
        if OmServiceDesign.objects.all().count()>0:
            max = OmServiceDesign.objects.all().aggregate(Max('id')).get('id__max')
            result = list(OmServiceDesign.objects.filter(id=max).values('content'))

            box_object = json.loads(result[0]["content"])

            #翻譯語言
            #language_type = get_language()
            lan_package = FlowActiveGlobalObject.getSysLanDict('service').get(language_type,{})
            
            #翻譯「全部」
            #export = check2addExport('全部',export,export_list,lan_package,language_type)
            for idx in box_object["list"]:
                this_service = box_object["list"][idx]
                #翻譯「服務名稱」
                export = check2addExport(this_service["setting"]["setTitle"],export,export_list,lan_package,language_type)
                      
                if this_service["type"]=="service" :
                    #翻譯「服務說明」
                    export = check2addExport(this_service["setting"]["setTip"],export,export_list,lan_package,language_type)
                    for sup_idx in this_service["service"]["list"]:
                        this_step = this_service["service"]["list"][sup_idx]
                        #翻譯「服務步驟名稱」
                        export = check2addExport(this_step["name"],export,export_list,lan_package,language_type)
                        #翻譯「服務步驟說明」
                        export = check2addExport(this_step["tip"],export,export_list,lan_package,language_type)
        
        info('%s export language package success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('匯出成功。'), export).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message',''), checker).returnJSON()

@login_required
@permission_required('omservice.OmServiceDesign_Manage','/api/permission/denied/')
@try_except
def exportServcieAjax(request):
    if OmServiceDesign.objects.all().count()>0:
        max = OmServiceDesign.objects.all().aggregate(Max('id')).get('id__max')
        box_object = list(OmServiceDesign.objects.filter(id=max).values('content'))
        box_object = json.loads(box_object[0]["content"])

        #翻譯語言
        lan_package = FlowActiveGlobalObject.getSysLanDict('service')
        result = { "box_object":box_object, "lan_package":lan_package }
        
        info(request ,'%s export language package success.' % request.user.username)
        return ResponseAjax(statusEnum.success, _('匯出成功。'), result).returnJSON()

def check2addExport( keyword, export, export_list, lan_package, language_type ):
    if len(keyword) and not keyword in export_list :
        if keyword in lan_package:
            export += 'original:'+ keyword + '\r\n'
            export += '' + language_type + ':' + lan_package[keyword] + '\r\n'
            export += '\r\n'
        else:
            export += 'original:'+ keyword + '\r\n'
            export += '' + language_type + ':\r\n'
            export += '\r\n'
        export_list.append(keyword)
    return export

def checkJsonKey( thisJson, thisKey ):
    if thisKey in thisJson and len(thisJson[thisKey]):
        return True
    else:
        return False
    
#自訂應用--子查詢
#查詢列表
@login_required
@try_except
def SubQueryHeaderAjax(request):
    '''
    list omdata for subquery.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    display_field_list = ['id','data_no','stop_uuid','stop_chart_text','error','error_message','closed','running']
    #get post data
    postdata = getPostdata(request)
    app_name = postdata.get('app_name','')
    flow_name = postdata.get('flow_name','')
    condition = postdata.get('condition',[])
    service_id = postdata.get('service_id',[])
    flowactive = FlowActiveGlobalObject.NameSearch(flow_name, None, app_name)
    flow_uuid = flowactive.flow_uuid.hex
    
    if True:
        #get field setting
        display_field_dict = json.loads(flowactive.display_field)
        for key in display_field_dict:
            if '-' in key:
                key = 'group'
            if key == 'create_user_id' or key == 'create_user':
                key = 'create_user_id__nick_name'
            elif key == 'update_user_id' or key == 'update_user':
                key = 'update_user_id__nick_name'
            display_field_list.append(key)
        search_field_list = display_field_list.copy()
        #暫時先使用display_field當作search_field
        field_list = list(map(lambda search_field : search_field + '__icontains', search_field_list))
        
        #sp conditions
        search_conditions = [{'column':'history','condition':'=','value':False}]
        exclude_conditions = []
        for con in condition:
            if con['condition'] == '!=':
                con['condition'] = '='
                exclude_conditions.append(con)
            elif con['condition'] == 'exclude':
                con['condition'] = 'contains'
                exclude_conditions.append(con)
            else:
                search_conditions.append(con)
        
        
        sc = searchConditionBuilder(search_conditions)
        ec = searchConditionBuilder(exclude_conditions)
        #get model
        omdata_model = getModel('omformmodel','Omdata_' + flow_uuid)
        if ec:
            query = omdata_model.objects.filter(reduce(operator.and_, sc)).exclude(reduce(operator.and_, ec)).values(*display_field_list)
        else:
            query = omdata_model.objects.filter(reduce(operator.and_, sc)).values(*display_field_list)
        
        result = DatatableBuilder(request, query, field_list)
        
        #轉換字與值
        result['data'] = datatableValueToText(result['data'], flow_uuid)
        
        #載入語言包
        language = get_language()
        result['data'] = Translator('datatable_single_app', 'active', language, flowactive.flow_app_id, None).Do(result['data'])
        
        info(request ,'%s list OmData success.' % request.user.username)
        return JsonResponse(result)
    else:
        info('%s has no permission.' % request.user.username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()

@login_required
@try_except
def SubQueryDataAjax(request):
    '''
    load omdata.
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['app_name','flow_name','data_id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    app_name = postdata.get('app_name','')
    flow_name = postdata.get('flow_name','')
    data_id = postdata.get('data_id','')
    field_list = postdata.get('fields',[])
    service_id = postdata.get('service_id',[])
    
    if True:
        if checker.get('status') == 'success':
            #get model
            fa = FlowActiveGlobalObject.NameSearch(flow_name, None, app_name)
            omdata_model = getModel('omformmodel', 'Omdata_' + fa.flow_uuid.hex)
            #整理欄位
            new_field_list = []
            group_user = []
            group_user_id = None
            for f in field_list:
                if re.match(r'formitm_[0-9]+-.+', f):
                    group_user_id = re.findall(r'(.+)-.+', f)[0]
                    group_user.append(f)
                    new_field_list.append(group_user_id)
                else:
                    new_field_list.append(f)
            
            #取得資料
            omdata = list(omdata_model.objects.filterformat(*new_field_list,id=data_id))
            
            if omdata:
                result = omdata[0]
                if group_user_id:
                    group_user_dict = json.loads(result.pop(group_user_id))
                    for g_u in group_user:
                        key = re.findall(r'.+-(.+)', g_u)[0]
                        result[g_u] = group_user_dict.get(key,'')
            else:
                result = {}
            
            info('%s load OmData success.' % request.user.username,request)
            return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()
        else:
            info('%s missing some require variable or the variable type error.' % request.user.username,request)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info('%s has no permission.' % request.user.username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
