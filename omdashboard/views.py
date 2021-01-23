import re, json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.utils.translation import gettext as _
from omflow.syscom.default_logger import info,error
from omflow.syscom.common import try_except, DataChecker, getPostdata, checkMigrate
from omflow.syscom.message import ResponseAjax, statusEnum
from omflow.global_obj import FlowActiveGlobalObject
from omformflow.models import ActiveApplication
from django.apps import apps
from django.utils.translation import get_language
#APP
from omdashboard.models import OmDashboard
from omformflow.models import FlowActive
import datetime
from django.db.models import Count,Max,Min,Avg,Sum,Q
from calendar import monthrange
from omflow.syscom.common import Translator
    


@login_required
@try_except
def saveDashboardAjax(request):
    '''
    save user's omdashboard setting
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
            dashboard = OmDashboard.objects.get_or_create(user=request.user)[0]
            setattr(dashboard,"content",postdata.get('content', ''))
            dashboard.save()
            info('%s update Dashboard success' % username,request)
            return ResponseAjax(statusEnum.success, _('儲存成功')).returnJSON()
        else:
            info('%s update Dashboard error' % username,request)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info('%s update Dashboard with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
       
@login_required
@try_except
def loadDashboardAjax(request):
    '''
    load user's dashboard settinomdashboardput: request
    return: json
    author: Arthur
    '''
    #Server Side Rule Check
    checkMigrate()
    username = request.user.username
    result = {}
    if username:
        #static variable
        if OmDashboard.objects.filter(user=request.user).count()>0:
            result = list(OmDashboard.objects.filter(user=request.user).values('content'))
            #result = list(OmDashboard.objects_d.filter('content',user=request.user))
        else :
            result = [{"content":'{"index":44,"list":{"3":{"id":3,"type":"box3","setting":{"setTitle":"","setColor":"box-default"}},"4":{"id":4,"type":"box3","setting":{"setTitle":"","setColor":"box-default"}},"5":{"id":5,"type":"box3","setting":{"setTitle":"","setColor":"box-default"}},"6":{"id":6,"type":"box3","setting":{"setTitle":"","setColor":"box-default"}},"7":{"id":7,"type":"box12","setting":{"setTitle":"全球產量分布","setColor":"box-primary"}},"9":{"id":9,"type":"box4","setting":{"setTitle":"","setColor":"box-default"}},"10":{"id":10,"type":"box4","setting":{"setTitle":"","setColor":"box-default"}},"11":{"id":11,"type":"box4","setting":{"setTitle":"","setColor":"box-default"}},"12":{"id":12,"type":"box4","setting":{"setTitle":"","setColor":"box-default"}},"15":{"id":15,"type":"word","setting":{"setTitle":"","setTip":"","setIcon":"fa fa-file-text","setColor":"bg-blue","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"16":{"id":16,"type":"word","setting":{"setTitle":"","setTip":"","setIcon":"fa fa-envelope","setColor":"bg-yellow","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"17":{"id":17,"type":"word","setting":{"setTitle":"","setTip":"","setIcon":"fa fa-thumbs-up","setColor":"bg-green","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"18":{"id":18,"type":"word","setting":{"setTitle":"","setTip":"","setIcon":"fa fa-line-chart","setColor":"bg-red","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"20":{"id":20,"type":"meter-bar","setting":{"setTitle":"","setTip":"台北","setColor":"progress-bar-blue","setMax":"100","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"21":{"id":21,"type":"meter-bar","setting":{"setTitle":"","setTip":"東京","setColor":"progress-bar-aqua","setMax":"100","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"22":{"id":22,"type":"meter-bar","setting":{"setTitle":"","setTip":"首爾","setColor":"progress-bar-green","setMax":"100","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"23":{"id":23,"type":"meter-bar","setting":{"setTitle":"","setTip":"紐約","setColor":"progress-bar-yellow","setMax":"100","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"24":{"id":24,"type":"meter-bar","setting":{"setTitle":"","setTip":"曼谷","setColor":"progress-bar-red","setMax":"100","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"25":{"id":25,"type":"meter-bar","setting":{"setTitle":"","setTip":"新加坡","setColor":"color-purple","setMax":"100","setUnit":"單位","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"26":{"id":26,"type":"tube","setting":{"setTitle":"","setTip":"","setIcon":"fa fa-heartbeat","setColor":"bg-red","setUnit":"單位","setMax":"100","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"27":{"id":27,"type":"tube","setting":{"setTitle":"","setTip":"","setIcon":"fa fa-leaf","setColor":"bg-green","setUnit":"單位","setMax":"100","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"28":{"id":28,"type":"tube","setting":{"setTitle":"","setTip":"","setIcon":"fa fa-car","setColor":"bg-blue","setUnit":"單位","setMax":"100","setForm":"","setColumn":[""],"setTime":"all","setType":["static"]}},"30":{"id":30,"type":"bar","setting":{"setTitle":"","setColor":"1","setHeight":"240","setYstart":"0","setForm":"","setColumn":[""],"setTime":"all","setType":["static"],"setGroup":[""]}},"31":{"id":31,"type":"box12","setting":{"setTitle":"","setColor":"box-default"}},"39":{"id":39,"type":"box4","setting":{"setTitle":"","setColor":"box-default"}},"40":{"id":40,"type":"box4","setting":{"setTitle":"","setColor":"box-default"}},"41":{"id":41,"type":"pie","setting":{"setTitle":"","setColor":"0","setUnit":"","setHeight":"320","setForm":"","setColumn":[""],"setTime":"all","setType":["static"],"setGroup":[""]}},"43":{"id":43,"type":"pie","setting":{"setTitle":"","setColor":"3","setUnit":"","setHeight":"320","setForm":"","setColumn":[""],"setTime":"all","setType":["static"],"setGroup":[""]}}},"tree":[{"id":"3","tree":[{"id":"15"}]},{"id":"4","tree":[{"id":"17"}]},{"id":"5","tree":[{"id":"16"}]},{"id":"6","tree":[{"id":"18"}]},{"id":"7","tree":[{"id":"9","tree":[{"id":"20"},{"id":"21"},{"id":"22"},{"id":"23"},{"id":"24"},{"id":"25"}]},{"id":"40","tree":[{"id":"41"}]},{"id":"39","tree":[{"id":"43"}]}]},{"id":"10","tree":[{"id":"26"}]},{"id":"11","tree":[{"id":"27"}]},{"id":"12","tree":[{"id":"28"}]},{"id":"31","tree":[{"id":"30"}]}]}'}]
        
        return ResponseAjax(statusEnum.success , _('讀取成功'), result).returnJSON()
    else:
        error('%s load Dashboard with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
         
@login_required
@try_except
def updateGridAjax(request):
    '''
    update grid information
    input: request
    return: json
    author: Arthur
    '''
    username = request.user.username
    postdata = getPostdata(request)
    
    #判斷必填
    require_field = ['content']
    checker = DataChecker(postdata, require_field)
    result = {}
    result["labels"] = []
    result["dataset"] = []
    
    if username and checker.get('status') == 'success':
        #static variable
        error_message = ""
        QueryJson = json.loads(postdata.get('content'))
        
#         QueryJson = {
#             "type":"word",
#             "form":"OmUser_View",
#             "column":[
#                     {
#                         "column":"department",
#                         "value":"max"
#                     },
#                 ],
#             "time_range":"this_year",
#             #"groupby":["gender"],
#             "orderby":[]
#         }
        #thisQuery = OmUser.objects.filter(updatetime__lte=datetime.date.today()).aggregate(**{"max":Max("department")})

        has_group = False
        if "groupby" in QueryJson:
            for key in QueryJson["groupby"]:
                if len(key):
                    has_group = True
        
        gte_list=[]
        lt_list=[]
        #判斷圖片類型
        
        if "type" in QueryJson and "form" in QueryJson : 
            #判斷時間格式
            if "time_range" in QueryJson:
                today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
                #print(today.strftime("%Y-%m-%d %H:%M:%S"))
                if QueryJson["time_range"]=="today":
                    gte_list.append(today)
                    #if has_group:
                    lt_list.append(gte_list[0] + datetime.timedelta(hours=1))
                    #print((gte_list[0] + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                    result["labels"].append('00:00')
                    for i in range(23):
                        gte_list.append(lt_list[i])
                        lt_list.append(lt_list[i] + datetime.timedelta(hours=1))
                        
                        result["labels"].append(switch00(i+1)+':00')
                    #else:
                        #lt_list.appecnd(gte_list[0] + datetime.timedelta(days=1))
                        #result["labels"].append(_('今日'))
                elif QueryJson["time_range"]=="yesterday":
                    gte_list.append(today - datetime.timedelta(days=1))
                    #if has_group:
                    lt_list.append(gte_list[0] + datetime.timedelta(hours=1))
                    result["labels"].append('00:00')
                    for i in range(23):
                        gte_list.append(lt_list[i])
                        lt_list.append(lt_list[i] + datetime.timedelta(hours=1))
                        result["labels"].append(switch00(i+1)+':00')
                    #else:
                        #lt_list.append(today)
                        #result["labels"].append(_('昨日'))
                elif QueryJson["time_range"]=="this_week":
                    gte_list.append(today - datetime.timedelta(days=today.weekday()))
                    #if has_group:
                    lt_list.append(gte_list[0] + datetime.timedelta(days=1))
                    result["labels"].append(translateW(1))
                    for i in range(6):
                        gte_list.append(lt_list[i])
                        lt_list.append(lt_list[i] + datetime.timedelta(days=1))
                        result["labels"].append(translateW(i+2))
                    #else:
                        #lt_list.append(today + datetime.timedelta(days=-today.weekday(), weeks=1))
                        #result["labels"].append(_('本周'))
                elif QueryJson["time_range"]=="last_week":
                    gte_list.append(today - datetime.timedelta(days=today.weekday(), weeks=1))
                    #if has_group:
                    lt_list.append(gte_list[0] + datetime.timedelta(days=1))
                    result["labels"].append(translateW(1))
                    for i in range(6):
                        gte_list.append(lt_list[i])
                        lt_list.append(lt_list[i] + datetime.timedelta(days=1))
                        result["labels"].append(translateW(i+2))
                    #else:
                        #lt_list.append(today - datetime.timedelta(days=today.weekday()))
                        #result["labels"].append(_('上周'))
                elif QueryJson["time_range"]=="this_month":
                    gte_list.append(today.replace(day=1))
                    #if has_group:
                    lt_list.append(gte_list[0] + datetime.timedelta(days=1))
                    result["labels"].append(str(gte_list[0].month)+'/'+str(gte_list[0].day))
                    for i in range(monthrange(today.year, today.month)[1]-1):
                        gte_list.append(lt_list[i])
                        lt_list.append(lt_list[i] + datetime.timedelta(days=1))
                        result["labels"].append(str(lt_list[i].month)+'/'+str(lt_list[i].day))
                    #else: 
                        #lt_list.append(gte_list[0] + datetime.timedelta(days=monthrange(gte_list[0].year, gte_list[0].month)[1]))
                        #result["labels"].append(_('今月'))
                elif QueryJson["time_range"]=="last_month":
                    if today.month==1:
                        gte_list.append(today.replace(day=1,month=switchM(today.month-1)),year=today.year-1)
                    else:
                        gte_list.append(today.replace(day=1,month=switchM(today.month-1)))
                    #if has_group:
                    lt_list.append(gte_list[0] + datetime.timedelta(days=1))
                    result["labels"].append(str(gte_list[0].month)+'/'+str(gte_list[0].day))
                    for i in range(monthrange(today.year, switchM(today.month-1))[1]-1):
                        gte_list.append(lt_list[i])
                        lt_list.append(lt_list[i] + datetime.timedelta(days=1))
                        result["labels"].append(str(lt_list[i].month)+'/'+str(lt_list[i].day))
                    #else:
                        #lt_list.append(today.replace(day=1))
                        #result["labels"].append(_('上月'))
                elif QueryJson["time_range"]=="this_year":
                    gte_list.append(today.replace(day=1,month=1))
                    #if has_group:
                    lt_list.append(gte_list[0].replace(month=2))
                    result["labels"].append(translateM(1))
                    for i in range(11):
                        gte_list.append(lt_list[i])
                        result["labels"].append(translateM(i+2))
                        if i !=11:
                            lt_list.append(lt_list[i].replace(month=switchM(i+3)))
                        else:
                            lt_list.append(today.replace(year=today.year+1,day=1,month=1))
                    #else:
                        #lt_list.append(today.replace(year=today.year+1,day=1,month=1))
                        #result["labels"].append(_('今年'))
                elif QueryJson["time_range"]=="last_year":
                    gte_list.append(today.replace(year=today.year-1,day=1,month=1))
                    #if has_group:
                    lt_list.append(gte_list[0].replace(month=2))
                    result["labels"].append(translateM(1))
                    for i in range(11):
                        gte_list.append(lt_list[i])
                        result["labels"].append(translateM(i+2))
                        if i !=11:
                            lt_list.append(lt_list[i].replace(month=switchM(i+3)))
                        else:
                            lt_list.append(today.replace(day=1,month=1))
                    #else:
                        #lt_list.append(today.replace(day=1,month=1))
                        #result["labels"].append(_('去年'))
                else:
                    gte_list.append(today.replace(year=1970))
                    lt_list.append(today + datetime.timedelta(days=1))
                    result["labels"].append(_('Labels'))
                
                #print(gte_list)
                #print(lt_list)
                #print(result["labels"])
                
            #解析json
            #permission = QueryJson["form"]
            permission = "Omdata_"+QueryJson["form"]+"_View"
            this_model = list(filter(lambda x: x.__name__==re.findall("^(.+)_View", permission)[0],apps.get_models()))
            getModel = False
            isPolicy = False
            if len(this_model) and request.user.has_perm(str(this_model[0]._meta.app_label)+"."+permission):
                getModel = True
            else:
                this_model = list(filter(lambda x: x.__name__==QueryJson["form"],apps.get_models()))
                if len(this_model) and request.user.has_perm("OmMonitor_Manage"):
                    getModel = True
                    isPolicy = True
                    
            if getModel:
                #setCondition
                filter_count = 0
                for i in range(len(gte_list)):
                    #print(gte_list[i].strftime("%Y-%m-%d %H:%M:%S"))
                    if isPolicy:
                        QueryJson["condition"]=[
                            {
                                "column":"createtime__gte",
                                "value":gte_list[i]
                            },{
                                "column":"createtime__lt",
                                "value":lt_list[i]
                            }]
                    else:
                        QueryJson["condition"]=[
                            {
                                "column":"updatetime__gte",
                                "value":gte_list[i]
                            },{
                                "column":"updatetime__lt",
                                "value":lt_list[i]
                            }]
                        
                    if not isPolicy:
                        #取得各ticket最新id_List
                        value_list = ["data_no"]
                        thisQuery = this_model[0].objects.all().values(*tuple(value_list))
                        thisQuery = thisQuery.annotate(New=Max('id'))
                        thisQuery = thisQuery.filter(id__in=list(thisQuery.values_list('New', flat=True)))
                        #id_list = list(thisQuery.values_list('New', flat=True))
                        #print(id_list)
                    else:
                        thisQuery = this_model[0].objects.all()
                           
                    this_condition = Q()
                    for cObj in QueryJson["condition"]:
                        this_condition.add(Q(**{cObj["column"]: cObj["value"]}),Q.AND)
                        #a = OmUser.objects.filter(Q(email="peilin@peilin.com")).values('nick_name').order_by('nick_name').annotate(count=Count('username'))    
                    
                    #thisQuery = this_model[0].objects.filter(this_condition)
                    thisQuery = thisQuery.filter(this_condition)
                    
                    value_list = []
                    if has_group:
                        for key in QueryJson["groupby"]:
                            if len(key):
                                value_list.append(key)
                    
                    #產出        
                    thisQuery = thisQuery.values(*tuple(value_list)) #QuerySet
                    QueryList = [] #List物件
                    thisQueryJson = {} #aggregate產出
                    
                    for cObj in QueryJson["column"]:
                        #有分類
                        if has_group:
                            if cObj["value"] == "max":
                                thisQuery = thisQuery.annotate(**{cObj["column"]:Max(cObj["column"])})
                            elif cObj["value"] == "min":
                                thisQuery = thisQuery.annotate(**{cObj["column"]:Min(cObj["column"])})
                            elif cObj["value"] == "count":
                                thisQuery = thisQuery.annotate(**{cObj["column"]:Count(cObj["column"])})
                            elif cObj["value"] == "sum":
                                thisQuery = thisQuery.annotate(**{cObj["column"]:Sum(cObj["column"])})
                            elif cObj["value"] == "avg":
                                thisQuery = thisQuery.annotate(**{cObj["column"]:Avg(cObj["column"])})
                            else:
                                if isPolicy:
                                    thisQuery = thisQuery.annotate(New=Max('createtime'))
                                    thisQuery = thisQuery.filter(createtime__in=list(thisQuery.values_list('New', flat=True)))
                                else :
                                    thisQuery = thisQuery.annotate(New=Max('updatetime'))
                                    thisQuery = thisQuery.filter(updatetime__in=list(thisQuery.values_list('New', flat=True)))
                            
                            has_static = False
                            for cObj in QueryJson["column"]:
                                if cObj["value"] == "static":
                                    value_list.append(cObj["column"])
                                    has_static = True
                            if has_static:
                                thisQuery = thisQuery.values(*tuple(value_list))
                            
                            if "orderby" in QueryJson :
                                for key in QueryJson["orderby"]:
                                    thisQuery = thisQuery.order_by(key)
                                    
                            QueryList = list(thisQuery)
                            
                        #無分類
                        else:
                            if cObj["value"] == "max":
                                thisQueryJson = thisQuery.aggregate(**{cObj["column"]:Max(cObj["column"])})
                            elif cObj["value"] == "min":
                                thisQueryJson = thisQuery.aggregate(**{cObj["column"]:Min(cObj["column"])})
                            elif cObj["value"] == "count":
                                thisQueryJson = thisQuery.aggregate(**{cObj["column"]:Count(cObj["column"])})
                            elif cObj["value"] == "sum":
                                thisQueryJson = thisQuery.aggregate(**{cObj["column"]:Sum(cObj["column"])})
                            elif cObj["value"] == "avg":
                                thisQueryJson = thisQuery.aggregate(**{cObj["column"]:Avg(cObj["column"])})
    
                            QueryList = [thisQueryJson]
                            
                            if cObj["value"] == "static":
                                if isPolicy:
                                    thisQueryJson = thisQuery.aggregate(New=Max('createtime'))
                                    thisQuery = thisQuery.filter(createtime__in=list([thisQueryJson.get('New')]))
                                else:
                                    thisQueryJson = thisQuery.aggregate(New=Max('updatetime'))
                                    thisQuery = thisQuery.filter(updatetime__in=list([thisQueryJson.get('New')]))
                                
                                QueryList = list(thisQuery)

                    if QueryJson["type"] and QueryJson["type"]!="table":
                        for row in QueryList:

                            if has_group:
                                this_value_list = list(filter(lambda x: x['name']==row.get(QueryJson["groupby"][0],""), result["dataset"]))
                            else:
                                this_value_list = result["dataset"]
                            
                            if len(this_value_list)==0:
                                value_list = {}
                                value = []
                                for j in range(filter_count):
                                    value.append("")
                                for cObj in QueryJson["column"]:
                                    value.append(row.get(cObj["column"],""))
                                if has_group:
                                    value_list["name"] = row.get(QueryJson["groupby"][0],"")
                                value_list["data"] = value
                                result["dataset"].append(value_list)
                            else:
                                for cObj in QueryJson["column"]:
                                    this_value_list[0]['data'].append(row.get(cObj["column"],""))
                        filter_count = filter_count+1
                        for this_value_list in result["dataset"]:
                            if len(this_value_list['data'])<filter_count:
                                this_value_list['data'].append("")
                        
                    else: #表格查詢
                        result["dataset"] = QueryList
                        result["column"] = []
                        for k in thisQuery[0].keys():
                            this_field = list(filter(lambda x: x.name==k, this_model[0]._meta.fields))
                            if len(this_field)>0:
                                result["column"].append(this_field[0].verbose_name)
        
        #print(result)
        if error_message =="":
            if result:
                return ResponseAjax(statusEnum.success, _('查詢成功'), result).returnJSON()
            else:
                return ResponseAjax(statusEnum.error, _('查詢失敗')).returnJSON()
        else:
            return ResponseAjax(statusEnum.error, error_message).returnJSON()
    else:
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
         
@login_required
@try_except
def getFormListAjax(request):
    '''
    get user model-list with permission
    input: request
    return: json
    author: Arthur
    ''' 
    username = request.user.username
    if username:
        #已上架流程
        this_activeList = list(FlowActive.objects.filter(undeploy_flag=0,parent_uuid__isnull=True).values_list('flow_uuid', flat=True))
        this_activeList = [o.hex for o in this_activeList]
        
        #有權限流程清單
        per_list = []
        if request.user.is_superuser:
            p = list(Permission.objects.filter(codename__contains="_View").values())
        else: 
            p = list(Permission.objects.filter(group__in=request.user.groups.all(),codename__contains="_View").values())
        result = {}
        for i in p:
            this_model = list(filter(lambda x: x.__name__==re.findall("^(Om.+)_View", i.get("codename"))[0],apps.get_models()))
            if len(this_model):
                this_name = this_model[0].__name__
                this_flow_uuid = re.findall("^Omdata_(.+)", this_name)
                if len(this_flow_uuid) :
                    if this_flow_uuid[0] in this_activeList:
                        per_list.append(this_flow_uuid[0])
        
        #上線流程
        flow_list = list(FlowActive.objects.filterformat('id','flow_uuid','flow_name','flow_app_id',undeploy_flag=False,parent_uuid=None))
        app_list = list(ActiveApplication.objects.filterformat('id','app_name',undeploy_flag=False))
        
        #merge
        flow = [x for x in flow_list if x['flow_uuid'] in per_list]
        flow_app = [x['flow_app_id'] for x in flow_list]
        app =  [x for x in app_list if x['id'] in flow_app]
        result = {'app':app,'flow':flow}
        
        #翻譯
        lang = get_language()
        result['app'] = Translator('datatable_multi_app','active', lang, None,None).Do(result['app'])
        result['flow'] = Translator('datatable_multi_app','active', lang, None,None).Do(result['flow'])
        
        from omflow.syscom.common import License
        version_type = License().getVersionType()
        if version_type != 'C':
            from ommonitor.models import MonitorFlow
            #判斷有無資料收集權限
            if request.user.has_perms("OmMonitor_Manage"):
                result['app'].append({'id':'sch','app_name':_('收集器流程')})
                result['app'].append({'id':'api','app_name':_('收集器API')})
                this_monitorList = list(MonitorFlow.objects.filterformat('id','table_id','flow_name','attr',history=0))
                for this_monitor in this_monitorList:
                    result['flow'].append({'id':this_monitor['id'],'flow_uuid':'OmPolicy_'+this_monitor['table_id'],'flow_name':this_monitor['flow_name'],'flow_app_id':this_monitor['attr']})
        
        info('%s get Form-List success' % username,request)
        return ResponseAjax(statusEnum.success , _('讀取成功'), result).returnJSON()
    else:
        info('%s get Form-List with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
         
@login_required
@try_except
def getColumnListAjax(request):
    '''
    get model column-list with permission
    input: request
    return: json
    author: Arthur
    ''' 
    username = request.user.username
    postdata = getPostdata(request)

    if username:
        require_field = ['model']
        checker = DataChecker(postdata, require_field)
        if checker.get('status') == 'success':
            permission = "Omdata_"+postdata.get('model', '')+"_View"
            this_model = list(filter(lambda x: x.__name__==re.findall("^(.+)_View", permission)[0],apps.get_models()))
            result={}
            
            #isPolicy = False
            from omflow.syscom.common import License
            version_type = License().getVersionType()
            if version_type != 'C':
                from ommonitor.models import MonitorFlow
                if len(this_model) == 0 and request.user.has_perm("OmMonitor_Manage"):
                    policy_model = list(filter(lambda x: x.__name__==postdata.get('model', ''),apps.get_models()))
                    if len(policy_model) :
                        this_table_id = re.findall("OmPolicy_(.+)", postdata.get('model', ''))[0]
                        fa = list(MonitorFlow.objects.filter(table_id=this_table_id).values('flowobject'))
                        if len(fa):
                            fa = json.loads(fa[0]['flowobject'])
                            result["collector_id"] = "collectorID"
                            for item in fa['items']:
                                if item['type'] == "end":
                                    for output in item['config']['output']:
                                        field_name = re.findall('\$\((.+)\)',output['name'])[0]
                                        result[field_name] = output['des']
                
                
            if len(this_model) and request.user.has_perm(str(this_model[0]._meta.app_label)+"."+permission):
                if re.match('Omdata_.+_View', permission) :
                    flow_uuid = re.findall("Omdata_(.+)_View", permission)[0]#Omdata_5d3c2cbdcf4145c3a05affaf4a74345b_View
                    fa = FlowActiveGlobalObject.UUIDSearch(flow_uuid).merge_formobject
                    if len(fa):
                        fa = json.loads(fa)
                        for field in this_model[0]._meta.fields:
                            if 'formitm' in field.verbose_name:
                                if field.name.upper() in fa:
                                    if fa[field.name.upper()]["type"] == 'h_group':
                                        #result[field.name] = fa[field.name.upper]
                                        result[field.name] = fa[field.name.upper()]["config"]["group_title"]
                                    else:
                                        result[field.name] = fa[field.name.upper()]["config"]["title"]
                            else:
                                result[field.name] = field.verbose_name
                                
                    lang = get_language()
                    app_id = FlowActiveGlobalObject.UUIDSearch(flow_uuid).flow_app_id
                    result = Translator( 'single_app','active', lang, app_id, None ).Do( result )
            
            if result != {}:
                info('%s get Column-List success' % username,request)
                return ResponseAjax(statusEnum.success, _('讀取成功。'),result).returnJSON()
            else:
                info('%s get Column-List with no permission' % username,request)
                return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
        else:
            info('%s get Column-List error' % username,request)
            return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
    else:
        info('%s get Column-List with no permission' % username,request)
        return ResponseAjax(statusEnum.no_permission, _('您沒有權限進行此操作。')).returnJSON()
    
def switchM(num):
    if num%12==0:
        return 12
    else:
        return num%12
    
def switch00(num):
    if len(str(num))>2:
        return str(num)[-2:]
    elif len(str(num))==1:
        return '0'+str(num)
    else:
        return str(num)

def translateM(num):
    if str(num)=='1':
        return _("1")
    elif str(num)=='2':
        return _("2")
    elif str(num)=='3':
        return _("3")
    elif str(num)=='4':
        return _("4")
    elif str(num)=='5':
        return _("5")
    elif str(num)=='6':
        return _("6")
    elif str(num)=='7':
        return _("7")
    elif str(num)=='8':
        return _("8")
    elif str(num)=='9':
        return _("9")
    elif str(num)=='10':
        return _("10")
    elif str(num)=='11':
        return _("11")
    elif str(num)=='12':
        return _("12")
    else:
        return _("No identity")
    
def translateW(num):
    if str(num)=='1':
        return _("1")
    elif str(num)=='2':
        return _("2")
    elif str(num)=='3':
        return _("3")
    elif str(num)=='4':
        return _("4")
    elif str(num)=='5':
        return _("5")
    elif str(num)=='6':
        return _("6")
    elif str(num)=='7':
        return _("6")
    
    