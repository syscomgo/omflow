'''
syscom omflow common mehod
@author: Pen Lin
'''
import re, operator, datetime, json
from django.db.models import Q
from _functools import reduce
from omuser.models import OmUser, OmGroup
from django.contrib.auth.models import Group
from omflow.syscom.message import ResponseAjax, statusEnum
from django.utils.translation import gettext as _
from omflow.syscom.default_logger import error
from omflow.syscom.constant import LOCAL_PORT
from omflow.global_obj import GlobalObject
from functools import wraps
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from omflow.syscom.license import getApps, getCustomer, getDevices, getUsers, getVersion, getVersionType, license_file_checker



def getPostdata(request):
    '''
    get postdata 
    input: request
    return: postdata 
    author: Kolin Hsu
    '''
    try:
        postdata = json.loads(request.body.decode("utf-8"))
    except:
        postdata = request.POST
    finally:
        return postdata


def checkEmailFormat(content = None):
    '''
    check content is email format
    input:content
    return: True , False
    author:Pen Lin
    '''
    if content == None:
        return False
    else:
        REGEX =  re.compile('[^@]+@[^@]+')
        if REGEX.match(content):
            return True
        else:
            return False


def DataChecker(data, req_list):
    '''
    check input data format
    input: postdata , require field list
    return: json
    author: Kolin Hsu
    '''
    def isRequired(content):
        if content and content != 'null':
            return True
        else:
            return False
    def isInt(content):
        if content:
            if isinstance(content, int):
                return True
            elif isinstance(content, str):
                try:
                    int(content)
                    return True
                except:
                    return False
            else:
                return False
        else:
            return True
    def isList(content):
        if content:
            if isinstance(content, list):
                return True
            else:
                return False
        else:
            return True
    def isEmail(content):
        if content:
            REGEX =  re.compile('[^@]+@[^@]+')
            if REGEX.match(content):
                return True
            else:
                return False
        else:
            return True
    def isDate(content):
        if content:
            date_format =  '%Y-%m-%d'
            try:
                datetime.datetime.strptime(content, date_format)
                return True
            except ValueError:
                return False
        else:
            return True
    def isBoolean(content):
        if content:
            if isinstance(content, bool):
                return True
            elif isinstance(content, int):
                if content == 1 or content == 0:
                    return True
                else:
                    return False
            elif isinstance(content, str):
                content = content.capitalize()
                if content == 'True' or content == 'False' or content == '0' or content == '1':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    def isWcode(content):
        if content:
            REGEX =  re.compile('[A-Z]{3}')
            if REGEX.match(content):
                return True
            else:
                return False
        else:
            return False
    
    #set variable
    result = {}
    require_null_list = []
    format_error_list = []
    #check post data has all required field
    key_list = list(data.keys())
    require_miss_list = list(set(req_list)-set(key_list))
    if len(require_miss_list) == 0:
        #check require field is not null
        for req_key in req_list:
            check = isRequired(data.get(req_key,''))
            if not check:
                require_null_list.append(req_key)
        if len(require_null_list) == 0:
            #check post data format
            for key in key_list:
                if '_$' in key:
                    check = isInt(data.get(key,''))
                elif '[]' in key:
                    check = isList(data.get(key,''))
                elif '_@' in key:
                    check = isEmail(data.get(key,''))
                elif '_%Y' in key:
                    check = isDate(data.get(key,''))
                elif '_%B' in key:
                    check = isBoolean(data.get(key,''))
                elif key == 'wcode':
                    check = isWcode(data.get(key,''))
                else:
                    check = True
                if not check:
                    format_error_list.append(key)
            if len(format_error_list) == 0:
                result['status'] = 'success'
            else:
                result['status'] = 'format error'
                result['result'] = format_error_list
                result['message'] = _('欄位格式錯誤，請修正後重新發送請求。')
        else:
            result['status'] = 'require null'
            result['result'] = require_null_list
            result['message'] = _('必要欄位為空，請填入後重新發送請求。')
    else:
        result['status'] = 'require missing'
        result['result'] = require_miss_list
        result['message'] = _('缺少必填欄位，請填入後重新發送請求。')
    return result


def FormDataChecker(formdata_list, formobject_items):
    '''
    check form data.
    input: formdata , formobject_items
    return: json
    author: Kolin Hsu
    '''
    #set variable
    status = True
    if isinstance(formdata_list, str):
        formdata_list = json.loads(formdata_list)
    for form_item in formobject_items:
        if form_item['id'][:8] == 'FORMITM_':
            if form_item['type'] == 'h_group':
                config = form_item['config']
                group_req = config.get('require',False)
                user_req = config.get('user_require',False)
                if group_req or user_req :
                    status = False
                else:
                    status = True
                    
                for data_item in formdata_list:
                    if data_item['id'] == form_item['id']:
                        status = True
                        group = data_item['value']['group']
                        user = data_item['value']['user']
                        if user_req:
                            if user == None or user == '':
                                status = False
                        if group_req:
                            if group == None or group == '':
                                status = False
                        break
                
                if not status:
                    break
            else:
                config = form_item['config']
                require = config.get('require',False)
                regex = config.get('regex','')
                if require :
                    status = False
                else:
                    status = True
                for data_item in formdata_list:
                    if data_item['id'] == form_item['id']:
                        status = True
                        value = data_item['value']
                        if require:
                            if value or value == 0:
                                pass
                            else:
                                status = False
                        if regex:
                            REGEX = re.compile(regex)
                            if not REGEX.match(value):
                                status = False
                        break
                if not status:
                    break
    return status


def DatatableBuilder(request, queryset, filed_list):
    '''
    build response data for datatble
    input: request, module dict, total_records
    return: json
    author: Kolin Hsu
    '''
    #function variable
    datatable_temporary = {}
    result_change = {}
    ordercolumn_list = []
    #data from datatable
    
    postdata = json.loads(request.body.decode('UTF-8'))
    draw = postdata.get('draw')
#     order = 0
#     while order >= 0:
#         i = postdata.get('order['+ str(order) +'][column]','')    #排序欄位值  int
#         if i:
#             ordercolumn_list.append(postdata.get('columns['+i+'][data]'))  #排序欄位名稱  str
#             order += 1
#         else:
#             order = -999
    for col in postdata.get('order'):
        if col['dir'] == 'asc':
            ordercolumn_list.append(postdata['columns'][col['column']]['data'])
        elif col['dir'] == 'desc':
            ordercolumn_list.append('-'+postdata['columns'][col['column']]['data'])
    searchkey = postdata['search'].get('value','')             #搜尋關鍵字
#     orderdir = postdata.get('order[0][dir]')           #排序方式:asc,desc  str
    length = postdata.get('length')                     #列表顯示長度  int
    start = postdata.get('start')                       #列表顯示起始位置  int
    limit = start + length
    lst = SearchQueryBuilder(filed_list,searchkey)
#     if orderdir == "asc":                                   #判斷排序方式          Q搜尋包含search關鍵字
    thislist = list(queryset.filter(reduce(operator.or_, lst)).order_by(*ordercolumn_list)[start:limit])
#     else:
#         thislist = list(queryset.filter(reduce(operator.or_, lst)).order_by(*ordercolumn_list).reverse()[start:limit])
    
    totalrecords = queryset.count()                         #計算總共取出資料筆數
    pagenumber = start/length + 1                           #現在頁數
    recordsfiltered = queryset.filter(reduce(operator.or_, lst)).order_by(*ordercolumn_list).count()    #計算關鍵字過濾後資料筆數
#     paginator = Paginator(table_dict,length)                #資料以列表顯示長度length做分頁
#     try:
#         thislist = paginator.page(pagenumber).object_list       #以現在頁數pagnumber取得資料清單
#     except:
#         thislist = 'page_null'
#     if thislist != 'page_null':
    recordsNum = len(thislist)
    thislist = DataFormat(thislist)
    #check draw is 1 or not
    if draw == 1:
        #set session data
        datatable_temporary['data'] = thislist
        datatable_temporary['pagenumber'] = pagenumber
        request.session['datatable_temporary'] = datatable_temporary
    else:
        #get session data
        datatable_temporary = request.session.get('datatable_temporary')
        #check datatable's page change or not. if changed, just return all records.
        if pagenumber == datatable_temporary['pagenumber']:
            #compare new data and ex-data in session. if equal, return null.
            if datatable_temporary['data'] == thislist:
                thislist = 'same'
            else:
                row_index = 0
                ex_records_num = len(datatable_temporary['data'])
                new_records_num = len(thislist)
                #check the numbers of record
                if ex_records_num - new_records_num < 0:
                    for row in datatable_temporary['data']:
                        #check every row is equal or not
                        if row == thislist[row_index]:
                            pass
                        else:
                            result_change[row_index] = thislist[row_index]
                        row_index += 1
                    #append the remaining part to result
                    for i in range(row_index, new_records_num):
                        result_change[i] = thislist[i]
                else:
                    for row in thislist:
                        #check every row is equal or not
                        if row == datatable_temporary['data'][row_index]:
                            pass
                        else:
                            result_change[row_index] = row
                        row_index += 1
                datatable_temporary['data'] = thislist.copy()
                request.session['datatable_temporary'] = datatable_temporary
                thislist = result_change
        else:
            #set session data
            datatable_temporary['data'] = thislist
            datatable_temporary['pagenumber'] = pagenumber
            request.session['datatable_temporary'] = datatable_temporary
    #datatable資料回傳內容
    result={
        'draw': draw,
        'recordsTotal': totalrecords,
        'recordsFiltered': recordsfiltered,
        'recordsNum' : recordsNum,
        'data': thislist                                    
    }
    return result


def SearchQueryBuilder(filed_list,searchkey):
    '''
    search user method
    input: filed_list,searchkey
    return: json
    author: Kolin Hsu
    '''
    lst = []
    for filed in filed_list:
        q_obj = Q(**{filed: searchkey})
        lst.append(q_obj)
    return lst


def DataFormat(model_dict):
    '''
    format UUID and datetime field to string
    input: model_dict
    return: model_dict
    author: Kolin Hsu
    '''
    for search_item in model_dict:
        for field in search_item:
            field_class = search_item[field].__class__.__name__
            if field_class == 'datetime':
                search_item[field] = str(search_item[field])
            elif field_class == 'UUID':
                search_item[field] = search_item[field].hex
    return model_dict


def UserSearch(filed_list,searchkey,ordercolumn):
    '''
    search user method
    input: filed_list,searchkey,ordercolumn
    return: json
    author: Kolin Hsu
    '''
    if searchkey:
        lst = SearchQueryBuilder(filed_list,searchkey)
        result = list(OmUser.objects.filter(delete=False).exclude(id=1).filter(reduce(operator.or_, lst)).values('id','username','nick_name').distinct().order_by(ordercolumn))
    else:
        result = list(OmUser.objects.filter(delete=False).exclude(id=1).values('id','username','nick_name').distinct().order_by(ordercolumn))
    return result


def GroupSearch(filed_list,searchkey,ordercolumn,adGroup):
    '''
    search group method
    input: filed_list,searchkey,ordercolumn,adGroup
    return: json
    author: Kolin Hsu
    '''
    lst = SearchQueryBuilder(filed_list,searchkey)
    result = list(Group.objects.filter(reduce(operator.or_, lst),omgroup__functional_flag=False,omgroup__ad_flag__in=adGroup).values('id','name','omgroup__display_name').distinct().order_by(ordercolumn))
    return result
    
    
def try_except(fun):
    '''
    exception decorator
    author: Kolin Hsu
    '''
    @wraps(fun)
    def handle_problems(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            if not args:
                error('Parameter is None',e)
            else:
                error(args[0],e)
            return ResponseAjax(statusEnum.error, e.__str__()).returnJSON()
    return handle_problems


def get_file_path(instance,filename):
    return '{0}/{1}/{2}'.format(instance.__module__.replace(".models",""),instance.main.id, filename)


def getModel(app_name, model_name):
    try:
        result = apps.get_registered_model(app_name,model_name)
        return result
    except:
        return False


def valueListLenReverse(ValueList,keys,reverses):
    if ValueList != []:
        if isinstance(ValueList[0], list):
            ValueList.sort(key=keys,reverse=reverses)
            return ValueList
            #### key = len ####
        elif isinstance(ValueList[0], tuple):
            ValueList.sort(key=keys,reverse=reverses)
            return ValueList
            #### key = len ####
        elif isinstance(ValueList[0], dict):
            reverseList =sorted(ValueList, key=lambda x: len(x[keys]), reverse=reverses)
            return reverseList
    else:
        ValueList = []
        return ValueList


def FormatToFormdataList(item, input_value, formdata_list):
    formdata_dict = {}
    formdata_dict['id'] = item['id']
    formdata_dict['type'] = item['type']
    if item['type'] == 'checkbox':
        if input_value == None or input_value == '':
            formdata_dict['value'] = input_value
        #如果是自動填入 格式為xxx,xxx,xxx
        elif '[' in input_value:
            formdata_dict['value'] = json.loads(input_value)
        #如果是前端回傳 格式為['xxx','xxx','xxx']
        else:
            formdata_dict['value'] = input_value.split(',')
    elif item['type'] == 'h_group':
        if input_value == None or input_value == '':
            group = ''
            user = ''
        elif '{' in input_value:
            json_input_value = json.loads(input_value)
            group = json_input_value['group']
            user = json_input_value['user']
        elif isinstance(input_value, list):
            if len(input_value) == 1:
                group = input_value[0]
                user = ''
            elif len(input_value) == 2:
                group = input_value[0]
                user = input_value[1]
            else:
                group = ''
                user = ''
        else:
            group, user = input_value.split(',')
        formdata_dict['value'] = {'group': group, 'user': user}
        group_dict = {'id':'group','type':'header','value':{'group': group, 'user': user}}
        formdata_list.append(group_dict)
    elif item['type'] == 'h_title':
        title_dict = {'id':'title','type':'header','value':input_value}
        formdata_list.append(title_dict)
        formdata_dict['value'] = input_value
    elif item['type'] == 'h_level':
        level_dict = {'id':'level','type':'header','value':input_value}
        formdata_list.append(level_dict)
        formdata_dict['value'] = input_value
    elif item['type'] == 'h_status':
        text = ''
        lists = item['config']['lists']
        for l in lists:
            if l['value'] == input_value:
                text = l['text']
                break
        status_dict = {'id':'status','type':'header','value':text}
        formdata_list.append(status_dict)
        formdata_dict['value'] = input_value
    else:
        formdata_dict['value'] = input_value
    formdata_list.append(formdata_dict)


def FormatFormdataListToFormdata(formdata_list):
    formdata = {}
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
    return formdata


def merge_formobject_items(items_list):
    try:
        merge_dict = {}
        for items in items_list:
            for item in items:
                item_id = item['id']
                if item_id[:8] == 'FORMITM_':
                    if item['type'] in ['h_status','h_group','list','checkbox']:
                        if merge_dict.get(item_id,''):
                            ex_item = merge_dict.get(item_id,'')
                            ex_item_list = ex_item['config']['lists']
                            now_item_list = item['config']['lists']
                            ex_value_list = []
                            for el in ex_item_list:
                                ex_value_list.append(el['value'])
                            for l in now_item_list:
                                if l['value'] not in ex_value_list:
                                    ex_item_list.append(l)
                    merge_dict[item_id] = item
    except:
        merge_dict = {}
    finally:
        return merge_dict

    
def check_app(app_name):
    app_list = settings.INSTALLED_APPS
    if app_name in app_list:
        return True
    else:
        return False


def getAppAttr(app_attr_num):
    try:
        s = 'user'
        if isinstance(app_attr_num, str):
            app_attr_num = int(app_attr_num)
        if app_attr_num == 1:
            s = 'sys'
        elif app_attr_num == 2:
            s = 'lib'
        elif app_attr_num == 3:
            s = 'cloud'
        elif app_attr_num == 4:
            s = 'policy'
    except:
        pass
    finally:
        return s


def getPolicyAttr(policy_attr_num):
    try:
        if isinstance(policy_attr_num, str):
            policy_attr_num = int(policy_attr_num)
        if policy_attr_num == 1:
            s = 'sch'
        elif policy_attr_num == 2:
            s = 'api'
        else:
            s = 'sch'
    except:
        pass
    finally:
        return s


def getUserName(user_id):
    try:
        nick_name = OmUser.objects.get(id=user_id).nick_name
    except:
        nick_name = ''
    finally:
        return nick_name


def getGroupName(group_id):
    try:
        display_name = OmGroup.objects.get(id=group_id).display_name
    except:
        display_name = ''
    finally:
        return display_name


def checkMigrate():
    if GlobalObject.__statusObj__.get('first_migrate',False):
        pass
    else:
        GlobalObject.__statusObj__['first_migrate'] = True
        call_command('migrate', app_label='omformmodel')


class License():
    def __init__(self):
        if license_file_checker() == LOCAL_PORT:
            self.check = True
        else:
            self.check = False
    
    
    def getVersionType(self):
        if self.check:
            return getVersionType()
        else:
            return 'C'
    
    
    def getUsers(self):
        if self.check:
            return getUsers()
        else:
            return 5
    
    
    def getApps(self):
        if self.check:
            return getApps()
        else:
            return 2
    
    
    def getDevices(self):
        if self.check:
            return getDevices()
        else:
            return 0
    
    
    def getCustomer(self):
        if self.check:
            return getCustomer()
        else:
            return ''
    
    
    def getVersion(self):
        if self.check:
            return getVersion()
        else:
            return getVersion()
        
    