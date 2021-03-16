import json, re
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, permission_required
from omflow.syscom.common import try_except, DataChecker, DatatableBuilder, getPostdata
from omflow.global_obj import GlobalObject
from omorganization.models import Organization, Position
from omflow.syscom.message import ResponseAjax, statusEnum
from omflow.syscom.default_logger import info,debug,error
from django.http.response import JsonResponse



@login_required
@permission_required('omuser.OmGroup_View','/page/403/')
def organizationPage(request):
    '''
    show organization page
    input: request
    return: organization page
    author: Kolin Hsu
    '''
    return render(request,'organization_manage.html')


@login_required
@permission_required('omuser.OmGroup_View','/page/403/')
def positionPage(request):
    '''
    show position page
    input: request
    return: position page
    author: Kolin Hsu
    '''
    return render(request,'position_manage.html')


@login_required
@try_except    
def updateOrganizationAjax(request):
    '''
    update organization
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = getPostdata(request)
    org_str = postdata.get('org','{}')
    o = Organization.objects.filter(name='organization')
    if o:
        o.update(value=org_str)
    else:
        Organization.objects.create(name='organization',value=org_str)
    setOrgToGlobal(org_str)
    info('%s update organization success.' % request.user.username,request)
    return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()


def checkOrgGlobal():
    result = True
    if not GlobalObject.__OrganizationObj__:
        org = loadOrganization()
        result = setOrgToGlobal(org)
    return result


def setOrgToGlobal(org):
    '''
    拆解organization物件並放至global
    '''
    try:
        #function variable
        
        line_source = {}
        line_target = {}
        people_dict = {}
        role_dict = {}
        dept_dict = {}
        status = True
        if org and isinstance(org, str):
            org = json.loads(org)
        items = org['items']
        for item in items:
            item_type = item['type']
            if item_type == 'line':
                source_item = item['config']['source_item']
                target_item = item['config']['target_item']
                #用來找下層
                if line_source.get(source_item,''):
                    line_source[source_item].append(target_item)
                else:
                    targets = [target_item]
                    line_source[source_item] = targets
                #用來找上層
                if line_target.get(target_item,''):
                    line_target[target_item].append(source_item)
                else:
                    sources = [source_item]
                    line_target[target_item] = sources
            elif item_type == 'dept':
                dept_dict[item['config']['noid']] = item['id']
            elif item_type == 'role':
                role_dict[item['id']] = item['text']
            elif item_type == 'people':
                people_dict[item['id']] = item['config']['noid']
        line_dict = {'source':line_source, 'target':line_target}
        GlobalObject.__OrganizationObj__['dept'] = dept_dict
        GlobalObject.__OrganizationObj__['role'] = role_dict
        GlobalObject.__OrganizationObj__['people'] = people_dict
        GlobalObject.__OrganizationObj__['line'] = line_dict
    except Exception as e:
        debug(e.__str__())
        status = False
    finally:
        return status
        

@login_required
@try_except    
def loadOrganizationAjax(request):
    '''
    load organization
    input: request
    return: json
    author: Kolin Hsu
    ''' 
    result = loadOrganization()
    info('%s load organization success.' % request.user.username,request)
    return ResponseAjax(statusEnum.success, _('讀取成功。'), result).returnJSON()


def loadOrganization():
    '''
    load organization
    '''
    org = list(Organization.objects.filter(name='organization'))
    if org:
        result = org[0].value
    else:
        result = ''
    return result
        

@login_required
@try_except    
def createPositionAjax(request):
    '''
    create position
    input: request
    return: json
    author: Kolin Hsu
    '''
    #get post data
    postdata = getPostdata(request)
    display_name = postdata.get('display_name','')
    description = postdata.get('description','')
    Position.objects.create(display_name=display_name,description=description)
    info('%s create position success.' % request.user.username,request)
    return ResponseAjax(statusEnum.success, _('建立成功。')).returnJSON()
        

@login_required
@try_except    
def updatePositionAjax(request):
    '''
    update position
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    pos_id = postdata.get('id','')
    display_name = postdata.get('display_name','')
    description = postdata.get('description','')
    if checker.get('status') == 'success':
        Position.objects.filter(id=pos_id).update(display_name=display_name,description=description)
        info('%s update position success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('更新成功。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
        

@login_required
@try_except    
def deletePositionAjax(request):
    '''
    delete position
    input: request
    return: json
    author: Kolin Hsu
    '''
    #function variable
    require_field = ['id']
    #server side rule check
    postdata = getPostdata(request)
    checker = DataChecker(postdata, require_field)
    #get post data
    id_list = postdata.get('id','')
    if checker.get('status') == 'success':
        Position.objects.filter(id__in=id_list).delete()
        info('%s update position success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('刪除成功。')).returnJSON()
    else:
        info('%s missing some require variable or the variable type error.' % request.user.username,request)
        return ResponseAjax(statusEnum.not_found, checker.get('message'), checker).returnJSON()
        

@login_required
@try_except    
def listPositionAjax(request):
    '''
    list position
    input: request
    return: json
    author: Kolin Hsu
    '''
    postdata = getPostdata(request)
    datatable = postdata.get('datatable',None)
    if datatable:
        #function variable
        field_list=['display_name__icontains','description__icontains']
        query = ''
        #get post data
        postdata = getPostdata(request)
        query = Position.objects.all().values('id','display_name','description')
        result = DatatableBuilder(request, query, field_list)
        info('%s list position success.' % request.user.username,request)
        return JsonResponse(result)
    else:
        result = list(Position.objects.all().values('id','display_name','description'))
        info('%s list position success.' % request.user.username,request)
        return ResponseAjax(statusEnum.success, _('查詢成功'), result).returnJSON()


def getRootPosition(group_id, position_name):
    '''
    取得同系角色
    '''
    try:
        user_id = None
        get_user = False
        group_id = str(group_id)
        dept_dict = GlobalObject.__OrganizationObj__['dept']
        role_dict = GlobalObject.__OrganizationObj__['role']
        people_dict = GlobalObject.__OrganizationObj__['people']
        source_dict = GlobalObject.__OrganizationObj__['line']['source']
        #取得起點部門的item id
        if re.match(r'FITEM_.+', group_id):
            g_item_id = group_id
        else:
            g_item_id = dept_dict.get(group_id,'')
        if g_item_id:
            #取得該部門的下層物件陣列
            target_list = source_dict.get(g_item_id,'')
            if target_list:
                #將物件陣列依照id由小至大排序，並迴圈取得role物件
                target_list.sort(key=lambda x: int(x[6:]))
                for t_id in target_list:
                    r_item_name = role_dict.get(t_id,'')
                    #確認物件是否為目標role物件
                    if r_item_name == position_name:
                        #找該物件的下層物件陣列
                        role_target_list = source_dict.get(t_id,'')
                        if role_target_list:
                            #排序陣列並取第一個物件id
                            target_list.sort(key=lambda x: int(x[6:]))
                            #取得使用者id
                            user_id = people_dict.get(role_target_list[0])
                        #只要找到role物件，無論是否找到使用者，都不會繼續找下去
                        get_user = True
                        break
            #如果該部門下層並無此職位，往上層物件找尋
            if not get_user:
                target_dict = GlobalObject.__OrganizationObj__['line']['target']
                #取得上層物件列表
                source_list = target_dict.get(g_item_id,'')
                if source_list:
                    #將物件陣列依照id由小至大排序，並迴圈取得dept物件
                    source_list.sort(key=lambda x: int(x[6:]))
                    for new_g_item_id in source_list:
                        #呼叫自己並把dept物件id帶入
                        grp_res = getRootPosition(new_g_item_id, position_name)
                        #找到物件後脫離迴圈
                        if grp_res['get_user']:
                            user_id = grp_res['user_id']
                            get_user = grp_res['get_user']
                            break
    except Exception as e:
        debug(e.__str__())
    finally:
        return {'user_id':user_id, 'get_user':get_user}


def getDeptPosition(group_id, position_name):
    '''
    取得部門角色
    '''
    try:
        user_id = None
        get_user = False
        group_id = str(group_id)
        dept_dict = GlobalObject.__OrganizationObj__['dept']
        role_dict = GlobalObject.__OrganizationObj__['role']
        people_dict = GlobalObject.__OrganizationObj__['people']
        source_dict = GlobalObject.__OrganizationObj__['line']['source']
        #取得起點部門的item id
        if re.match(r'FITEM_.+', group_id):
            g_item_id = group_id
        else:
            g_item_id = dept_dict.get(group_id,'')
        if g_item_id:
            #取得該部門的下層物件陣列
            target_list = source_dict.get(g_item_id,'')
            if target_list:
                #將物件陣列依照id由小至大排序，並迴圈取得role物件
                target_list.sort(key=lambda x: int(x[6:]))
                for t_id in target_list:
                    r_item_name = role_dict.get(t_id,'')
                    #確認物件是否為目標role物件
                    if r_item_name == position_name:
                        #找該物件的下層物件陣列
                        role_target_list = source_dict.get(t_id,'')
                        if role_target_list:
                            #排序陣列並取第一個物件id
                            role_target_list.sort(key=lambda x: int(x[6:]))
                            #取得使用者id
                            user_id = people_dict.get(role_target_list[0])
                        #只要找到role物件，無論是否找到使用者，都不會繼續找下去
                        get_user = True
                        break
            #如果該部門下層並無此職位，往下層物件找尋
            if not get_user:
                if target_list:
                    for new_g_item_id in target_list:
                        #呼叫自己並把dept物件id帶入
                        grp_res = getRootPosition(new_g_item_id, position_name)
                        #找到物件後脫離迴圈
                        if grp_res['get_user']:
                            user_id = grp_res['user_id']
                            get_user = grp_res['get_user']
                            break
    except Exception as e:
        debug(e.__str__())
    finally:
        return {'user_id':user_id, 'get_user':get_user}