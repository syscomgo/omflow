import json
from omformflow.views import createOmData
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext as _
from omflow.syscom.default_logger import info,error
from omflow.syscom.common import try_except, DataChecker, getPostdata
from omflow.syscom.message import ResponseAjax, statusEnum
from omservice.models import OmService, OmServiceDesign
from omformflow.models import FlowActive
from django.db.models import Max

@login_required
def servicePage(request):
    return render(request, 'list.html')


@permission_required('omservice.OmServiceDesign_Manage','/page/403/')
@login_required
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

            #static variable
            box_object = json.loads(postdata.get('content', ''))
            
            #service_design = OmServiceDesign.objects.get_or_create(id=1)[0]
            #setattr(service_design,"content",json.dumps(box_object))
            #service_design.save()
            
            OmServiceDesign.objects.create(content=json.dumps(box_object))
            
            OmService.objects.all().delete();
            
            ServiceList = []
            for key in box_object["list"]:
                thisSer = box_object["list"][key]
                if thisSer["type"]=="service":
                    ser = OmService(service_id=thisSer['id'],flow_uuid=thisSer['flow_uuid'],role=thisSer['setting']['setRole'],default_value=json.dumps(thisSer['default_value']))
                    ServiceList.append(ser)
            
            OmService.objects.bulk_create(ServiceList)
            
            info(request,'%s update Service success' % username)
            return ResponseAjax(statusEnum.success, _('儲存成功')).returnJSON()
        else:
            info(request,'%s update Service error' % username)
            return ResponseAjax(statusEnum.not_found, _(checker.get('message')), checker).returnJSON()
    else:
        info(request,'%s update Service with no permission' % username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


@try_except
def loadServiceAjax(request):
    '''
    load manager's service setting
    return: json
    author: Arthur
    '''
    
    #Server Side Rule Check
    username = request.user.username
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
                    if box_object["list"][idx]["flow_uuid"] in this_activeList:
                        box_object["list"][idx]["available"] = 1
                    else:
                        box_object["list"][idx]["available"] = 0
            
            result[0]["content"] = json.dumps(box_object)            

        return ResponseAjax(statusEnum.success , _('讀取成功'), result).returnJSON()
    else:
        error(request,'%s load Service with no permission' % username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()


#@permission_required('omservice.OmServiceDesign_Manage','/page/403/')         
@login_required
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
        thisQuery = list(FlowActive.objects.filterformat("flow_uuid","flow_name",undeploy_flag=False,parent_uuid__isnull=True))
        for thisRow in thisQuery:
            #result[re.findall("^Omdata_(.+)$", this_model.__name__)[0]] = this_model.table_name
            result[thisRow["flow_uuid"]] = thisRow["flow_name"]
        return ResponseAjax(statusEnum.success , _('讀取成功'), result).returnJSON()
    else:
        error(request,'%s load form_list with no permission' % username)
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
    #print(postdata)
    
    if username:
        require_field = ['flow_uuid']
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            thisQuery = list(FlowActive.objects.filter(flow_uuid=postdata.get('flow_uuid'),undeploy_flag=False).values('formobject','attachment'))
            if len(thisQuery):
                result = thisQuery[0]
                
        return ResponseAjax(statusEnum.success , _('讀取成功'), result).returnJSON()
    else:
        error(request,'%s get form_object with no permission' % username)
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
        require_field = ['flow_uuid','service_id','formdata']
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            #判斷權限
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
                info(request,'%s update Service error' % username)
                return ResponseAjax(statusEnum.error, _('查無此服務')).returnJSON()
            
            result = createOmData(postdata,request.user.username,files)
            if result['status']:
                return ResponseAjax(statusEnum.success, result['message']).returnJSON()
            else:
                return ResponseAjax(statusEnum.not_found, result['message']).returnJSON()
        else:
            return ResponseAjax(statusEnum.not_found, _('缺少必填欄位')).returnJSON()
    else:
        error(request,'%s request_service with no permission' % username)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
         

    
    