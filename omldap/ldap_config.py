from omuser.models import OmGroup,OmUser
from django.db.models import Count
from omflow.syscom.default_logger import info,error,debug
from django.utils.translation import gettext as _
from omflow.global_obj import GlobalObject
from omflow.models import SystemSetting
import json,ast,time
from omflow.syscom.license import getUsers
ldpadata_json = {}
from omflow.syscom.common import check_app
if check_app('omldap'):
    try:
        from ldap3 import Server, Connection, ALL
    except Exception as e:
        error("LDAP error：" + str(e))

def create_LDAP_user(ldap_client_server,ldap_client_server_port,ldap_base_dn,ldap_bind_user,ldap_bind_user_password):
    '''
    use ldap3 create user
    input: connect LDAP objectClass=user
    return: create user time
    author: Jia Liu
    ''' 
    start = time.time()
    server = Server(host=ldap_client_server,port=int(ldap_client_server_port),get_info=ALL,connect_timeout=2)
    conn = Connection(server, ldap_bind_user, ldap_bind_user_password, auto_bind=True,receive_timeout=2)
    conn.search(ldap_base_dn, '(&(objectCategory=person)(objectClass=user))', attributes=['distinguishedName','sAMAccountName','cn','userPrincipalName','userAccountControl','objectSID'])
    result = conn.entries
    AD_List = list(filter(lambda x: not "CN=Users"  in str(x['distinguishedName']).split(','), result))
    DN_User_List = []
    AD_User_List= []
    AD_User_SID = []
    Disable_User_List = []
    Enable_User_List = []
    diffAddUserList = []
    diffDeleteUserList = []
    ADduplicateUserList = []
    ad_flag = True
    #Get user DN, user account, user user Account to lists.
    for ldap in AD_List:
        ldapJson = json.loads(ldap.entry_to_json())
        getUserList = ldapJson
        getUsername = ldapJson['attributes']['sAMAccountName']
        disableUser = ldapJson['attributes']['userAccountControl']
        getUserSID = ldapJson['attributes']['objectSid']
        AD_User_List.extend(getUsername)
        DN_User_List.append(getUserList)
        AD_User_SID.extend(getUserSID)
        if disableUser[0] == 514:
            Disable_User_List.extend(getUsername)
        else:
            Enable_User_List.extend(getUsername)
  
    #Get OmUserList from LDAP created.
    OmUserList = list(OmUser.objects.filter(ad_flag=ad_flag).values_list('ad_sid',flat=True))
    OmUserNonADList = list(OmUser.objects.filter(ad_flag=False).values_list('username',flat=True))
    duplicateUserList = list(set(AD_User_List) & set(OmUserNonADList))
    AD_Exclude_Duplicate_User_List = list(filter(lambda x: not x['attributes']['sAMAccountName'][0] in duplicateUserList, DN_User_List))
    AD_Duplicate_User_List = list(filter(lambda x: x['attributes']['sAMAccountName'][0] in duplicateUserList, DN_User_List))
    
    for ADduplicateUserdict in AD_Duplicate_User_List:
        User_sid =  ADduplicateUserdict['attributes']['objectSid']
        ADduplicateUserList.extend(User_sid)
    if len(OmUserList) == 0:
        OmUser.objects.bulk_create([
            OmUser(
                username = userList['attributes']['sAMAccountName'][0],
                nick_name = userList['attributes']['cn'][0],
                email = userList['attributes']['userPrincipalName'][0],
                ad_sid = userList['attributes']['objectSid'][0],
                ad_flag = ad_flag,
                is_active = False,
                ) for userList in AD_Exclude_Duplicate_User_List])
        diffAddUserList = ["all users are created."]
    elif OmUserList == AD_User_SID:
        pass
    elif OmUserList != AD_User_SID:
        diffAddUserList = list(set(AD_User_SID).difference(set(OmUserList)))
        diffDeleteUserList = list(set(OmUserList).difference(set(AD_User_SID)))
        excludeDuplicateAddUserList = list(set(diffAddUserList).difference(set(ADduplicateUserList)))
        excludeDuplicateDeleteUserList = list(set(diffDeleteUserList).difference(set(ADduplicateUserList)))
        if len(diffAddUserList) > 0 :
            try:
                #From AD_User_List get user account name,if user account name is equal to diffAddUserList,create AddUser from AddUserList.
                OmUser.objects.bulk_create([
                    OmUser(
                        username = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['sAMAccountName'][0],
                        nick_name = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['cn'][0],
                        email = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['userPrincipalName'][0],
                        ad_sid = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['objectSid'][0],
                        ad_flag = ad_flag,
                    ) for add_user in excludeDuplicateAddUserList])
            except Exception as e:
                for add_user in excludeDuplicateAddUserList:
                    username_ad = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['sAMAccountName'][0]
                    try:
                        user_get = OmUser.objects.get(username = username_ad)
                        user_get.username = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['sAMAccountName'][0]
                        user_get.nick_name = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['cn'][0]
                        user_get.email = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['userPrincipalName'][0]
                        user_get.ad_sid = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['objectSid'][0]
                        user_get.is_active = False
                        user_get.delete = False
                        user_get.ad_flag = ad_flag
                        user_get.save()
                    except:
                        add_username = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['sAMAccountName'][0]
                        add_nick_name = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['cn'][0]
                        add_email = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['userPrincipalName'][0]
                        add_ad_sid = list(filter(lambda user: user['attributes']['objectSid'][0] == add_user, DN_User_List))[0]['attributes']['objectSid'][0]
                        add_ad_flag = ad_flag
                        add_ad_is_active = False
                        OmUser.objects.create(username=add_username,nick_name=add_nick_name,email=add_email,ad_sid=add_ad_sid,ad_flag=add_ad_flag,is_active=add_ad_is_active)  
            debug("excludeDuplicateAddUserList: %s" % excludeDuplicateAddUserList)
        if len(diffDeleteUserList) > 0:
            OmUser.objects.filter(ad_sid__in=excludeDuplicateDeleteUserList).update(is_active=False,delete=True)
            debug("excludeDuplicateDeleteUserList: %s" % excludeDuplicateDeleteUserList)
    #execute enable user action.
    license_user_num = getUsers()
    now_users_num = OmUser.objects.filter(delete=False,is_active=True).exclude(username='system').count()
    now_users_list = list(OmUser.objects.filter(delete=False,is_active=True).exclude(username='system').values_list('username',flat=True))
    excludeDuplicateEnableUserList = list(set(Enable_User_List).difference(set(OmUserNonADList)))
    excludeDuplicateEnableUserList.sort()
#     if now_users_num < license_user_num:
    for pop_user in now_users_list:
        try:
            pop_index = excludeDuplicateEnableUserList.index(pop_user)
            excludeDuplicateEnableUserList.pop(pop_index)
        except Exception as e:
            pass
    enableusercount = license_user_num - now_users_num
    OmUser.objects.filter(username__in=excludeDuplicateEnableUserList[0:enableusercount]).update(is_active=True)
    OmUser.objects.filter(username__in=excludeDuplicateEnableUserList[enableusercount:]).update(is_active=False)
    #execute disable user action.
    excludeDuplicateDisableUserList = list(set(Disable_User_List).difference(set(OmUserNonADList)))
    OmUser.objects.filter(username__in=excludeDuplicateDisableUserList).update(is_active=False,delete=False)
   
    debug("excludeDuplicateDisableUserList: %s" % excludeDuplicateDisableUserList)
    debug("excludeDuplicateEnableUserList: %s" % excludeDuplicateEnableUserList)
    conn.unbind()
    end = time.time()
    execute_time = end-start
    return info("User create successful,execute time: %.4f second." % (execute_time))

def create_LDAP_group(ldap_client_server,ldap_client_server_port,ldap_base_dn,ldap_bind_user,ldap_bind_user_password):
    '''
    use ldap3 create group
    input: connect LDAP organization unit
    return: create group time
    author: Jia Liu
    ''' 
    start = time.time()
    # search LDAP organization unit return all result
    server = Server(host=ldap_client_server,port=int(ldap_client_server_port), get_info=ALL,connect_timeout=2)
    conn = Connection(server, ldap_bind_user, ldap_bind_user_password, auto_bind=True,receive_timeout=2)
    conn.search(ldap_base_dn, '(objectCategory=organizationalUnit)', attributes=['OU','distinguishedName'])
    result = conn.entries
    #Set default need parameter
    AD_OU_List = []
    diffAddTupleList = []
    diffdeleteTupleList = []
    functional_flag = False
    ad_flag = True
    OmGroupstr_List = list(OmGroup.objects.filter(ad_flag=ad_flag).values_list('name',flat=True))
    OmGroup_List = []
    #string type list to list type.
    for GroupList in OmGroupstr_List:
        OmGroup_List.append(ast.literal_eval(GroupList))
    #Get list[0] value,and value combine to OU list,append to AD_OU_List.
    for ldap in result:
        ldapJson = json.loads(ldap.entry_to_json())
        getOU = ldapJson['attributes']['distinguishedName'][0].split(',')
        AD_OU_List.append(getOU)
        #OmGroupList length is 0,create all group from LDAP AD_OU_List.
    if len(OmGroup_List) == 0:
        for oulist in AD_OU_List:
            group_name = str(oulist[0]).replace("OU=",'')
            #check OU count in list.
            oucount = sum('OU=' in count for count in oulist)
            #count = 1 is head group.
            if oucount == 1:
                OmGroup.objects.create(name=oulist,parent_group=None,functional_flag=functional_flag,display_name=group_name,ad_flag=ad_flag)
            #count > 1 is child group.
            elif oucount > 1:
                if oulist != AD_OU_List[0]:
                    parent_groupname = []
                    parent_groupname.extend(oulist)
                    parent_groupname.pop(0)
                    parent_group_name= parent_groupname
                    parent_group = OmGroup.objects.get(name=parent_group_name)
                    OmGroup.objects.create(name=oulist,parent_group=parent_group,functional_flag=functional_flag,display_name=group_name,ad_flag=ad_flag)
                else:
                    OmGroup.objects.create(name=oulist,parent_group=None,functional_flag=functional_flag,display_name=group_name,ad_flag=ad_flag)
                       
        diffAddTupleList = ["all organization units are created."]
    elif OmGroup_List == AD_OU_List:
        pass
    #Compare two lists,if true, execute add or delete group.
    elif OmGroup_List != AD_OU_List:
        set_AD_OU_List = set(map(tuple, AD_OU_List))
        set_OmGroup_List = set(map(tuple, OmGroup_List))
        intersectionTupleList = list(set(set_OmGroup_List).intersection(set(set_AD_OU_List)))
        diffAddTupleList = list(set_AD_OU_List.difference(set_OmGroup_List))
        diffdeleteTupleList = list(set_OmGroup_List.difference(set_AD_OU_List))
        diffAddTupleList.sort(key=len)
        diffdeleteTupleList.sort(key=len,reverse=True)
        intersectionTupleList.sort(key=len)
        if diffdeleteTupleList != []:
            for deletegroupTuple in diffdeleteTupleList:
                deletegroupList = list(deletegroupTuple)
                group = OmGroup.objects.get(name=deletegroupList)
                group.delete()
        if diffAddTupleList != []:
            for addgroupTuple in diffAddTupleList:
                addgroupList = list(addgroupTuple)
                group_name = str(addgroupList[0]).replace("OU=",'')
                oucount = sum('OU=' in count for count in addgroupList)
                if OmGroup.objects.filter(name=addgroupList).exists():
                    pass
                elif oucount == 1:
                    OmGroup.objects.create(name=addgroupList,parent_group=None,functional_flag=functional_flag,display_name=group_name,ad_flag=ad_flag)
                elif oucount > 1:
                    if addgroupTuple != diffAddTupleList[0]:
                        parent_groupname = []
                        parent_groupname.extend(addgroupList)
                        parent_groupname.pop(0)
                        parent_group_name= parent_groupname
                        parent_group = OmGroup.objects.get(name=parent_group_name)
                        OmGroup.objects.create(name=addgroupList,parent_group=parent_group,functional_flag=functional_flag,display_name=group_name,ad_flag=ad_flag)
                    else:
                        OmGroup.objects.create(name=addgroupList,parent_group=None,functional_flag=functional_flag,display_name=group_name,ad_flag=ad_flag)
        if intersectionTupleList != []:
            for intersectionGroupTuple in intersectionTupleList:
                intersectionGroupList = list(intersectionGroupTuple)
                oucount = sum('OU=' in count for count in intersectionGroupList)
                if oucount == 1:
                    pass
                elif oucount > 1:
                    if OmGroup.objects.filter(name=intersectionGroupList).exists():
                        group_name = OmGroup.objects.get(name=intersectionGroupList)
                        parent_groupname = []
                        parent_groupname.extend(intersectionGroupList)
                        parent_groupname.pop(0)
                        parent_group_name= parent_groupname
                        if OmGroup.objects.filter(name=parent_group_name).exists():
                            parent_group = OmGroup.objects.get(name=parent_group_name)
                            group_name.parent_group = parent_group
                            group_name.save()
                    else:
                        group_name = str(intersectionGroupList[0]).replace("OU=",'')
                        if intersectionGroupTuple != intersectionTupleList[0]:
                            parent_groupname = []
                            parent_groupname.extend(intersectionGroupList)
                            parent_groupname.pop(0)
                            parent_group_name= parent_groupname
                            parent_group = OmGroup.objects.get(name=parent_group_name)
                            OmGroup.objects.create(name=intersectionGroupList,parent_group=parent_group,functional_flag=functional_flag,display_name=group_name,ad_flag=ad_flag)
                        else:
                            OmGroup.objects.create(name=intersectionGroupList,parent_group=None,functional_flag=functional_flag,display_name=group_name,ad_flag=ad_flag)
    debug("diffAddTupleList: %s" % diffAddTupleList)
    debug("diffdeleteTupleList: %s" % diffdeleteTupleList)
    conn.unbind()
    end = time.time()
    execute_time = end-start
    return info("Group create successful,execute time: %.4f second." % (execute_time))

def mapping_group_user(ldap_client_server,ldap_client_server_port,ldap_base_dn,ldap_bind_user,ldap_bind_user_password):
    '''
    use ldap3 mapping group and user
    input: connect LDAP objectClass=user
    return: mapping time
    author: Jia Liu
    ''' 
    start = time.time()
    server = Server(host=ldap_client_server,port=int(ldap_client_server_port), get_info=ALL,connect_timeout=2)
    conn = Connection(server, ldap_bind_user, ldap_bind_user_password, auto_bind=True,receive_timeout=2)
    conn.search(ldap_base_dn, '(&(objectCategory=person)(objectClass=user))', attributes=['distinguishedName','sAMAccountName','cn','userPrincipalName','userAccountControl'])
    result = conn.entries
    dict_OU_Group = {}
    dict_Omuser_Group = {}
    #Get AD List ,exclude group CN=Users and None.
    AD_List = list(filter(lambda x: not "CN=Users"  in str(x['distinguishedName']).split(','), result))
    #Get OmGroupList from LDAP created.
    OmGroupstr_List = list(OmGroup.objects.filter(ad_flag=True).values_list('name',flat=True))
    #Exclude same username in ad_flag = False in user list.
    OmUserNonADList = list(OmUser.objects.filter(ad_flag=False).values_list('username',flat=True))
    AD_Exclude_Duplicate_User_List = list(filter(lambda x: not x['sAMAccountName'][0] in OmUserNonADList, AD_List))
    #Count LDAP groups_id from Omuser_group.
    Omuser_Groups_count  = OmUser.objects.filter(ad_flag=True).values('id').aggregate(count = Count('groups'))
    OmGroup_List = []
    #string type list to list type.
    for GroupList in OmGroupstr_List:
        OmGroup_List.append(ast.literal_eval(GroupList))

    for groupnameList in OmGroup_List:
        #dictionaries value set list type.
        dict_OU_Group[str(groupnameList)] = []
        dict_Omuser_Group[str(groupnameList)] = []
        #Get LDAP group id and append to dictionaries from Omuser_Groups.
        OmuserGroups_id_List = list(OmUser.objects.filter(ad_flag=True,groups__name=groupnameList).values_list('id',flat = True))
        dict_Omuser_Group[str(groupnameList)].extend(OmuserGroups_id_List)
        dict_Omuser_Group[str(groupnameList)].sort()
        #Get group name from sublist in AD_List.
        AD_Group_User_List = list(filter(lambda x: ','.join(groupnameList)  in x['distinguishedName'][0], AD_Exclude_Duplicate_User_List))
        #Get LDAP group id and append to dictionaries from AD_Group_User_List.
        for AD_user in AD_Group_User_List:
            user = AD_user['sAMAccountName'][0]
            omuserid = OmUser.objects.get(username=user).id
            dict_OU_Group[str(groupnameList)].append(omuserid)
        dict_OU_Group[str(groupnameList)].sort()

    #Compare two dictionaries,get add_group_dict and delete_group_dict.
    addGroupDict    = dict( (key, list(set(dict_OU_Group[key])- set(dict_Omuser_Group[key])))
                        for key in (set(dict_OU_Group) & set(dict_Omuser_Group))
                            if dict_OU_Group[key] != dict_Omuser_Group[key])
  
    deleteGroupDict = dict( (key, list(set(dict_Omuser_Group[key]) -set(dict_OU_Group[key])))
                        for key in (set(dict_Omuser_Group) & set(dict_OU_Group))
                            if dict_Omuser_Group[key] != dict_OU_Group[key])
    if Omuser_Groups_count['count'] == 0:   
        for groupname_OU_List in OmGroup_List:
            omgroup = OmGroup.objects.get(name=groupname_OU_List)
            omgroup.user_set.add(*dict_OU_Group[str(groupname_OU_List)])
    if addGroupDict != {}:
        for key,value in addGroupDict.items():
            omgroup = OmGroup.objects.get(name=str(key))
            omgroup.user_set.add(*value)
    if deleteGroupDict != {}:
        for key,value in deleteGroupDict.items():
            omgroup = OmGroup.objects.get(name=str(key))
            omgroup.user_set.remove(*value)
    debug("dict_OU_Group: %s" % dict_OU_Group)
    debug("addGroupDict: %s" % addGroupDict)
    debug("deleteGroupDict: %s" % deleteGroupDict)
    conn.unbind()
    end = time.time()
    execute_time = end-start
    return info("mapping_group_user is successful,execute time: %.4f second." % (execute_time))

def check_LDAP_auth(username,password):
    '''
    use ldap3 check LDAP authorization
    input:  user account to connect LDAP
    return: True or False
    author: Jia Liu
    ''' 
    
    ldap_server = GlobalObject.__ldapObj__['ldap_client_server']
    ldap_port = GlobalObject.__ldapObj__['ldap_client_server_port']
    domain = GlobalObject.__ldapObj__['ldap_client_domain']
    ldap_username = "{}@{}".format(username,domain)
    ldap_password = password
    if len(password) > 0:
        try:
            server = Server(host=ldap_server, port=int(ldap_port), use_ssl=False, get_info='ALL',connect_timeout=2)
            conn =Connection(server, user=ldap_username, password=ldap_password, auto_bind='NONE', version=3,
                                    authentication='SIMPLE', client_strategy='SYNC', auto_referrals=False,
                                    check_names=True, read_only=True, lazy=False, raise_exceptions=False,receive_timeout=2)
            if conn.bind():
                return True
            else:
                return False
            conn.unbind()
        except:
            return False
    else:
        return False
                
def syncLDAP():
    '''
    Get parameters to sync LDAP
    input:  execute LDAP functions
    return: result message
    author: Kolin Hsu,Pei Lin
    ''' 
    result = {}
    try:
        ldpadatastr = SystemSetting.objects.get(name='ldap_config').value
        ldpadata_json = json.loads(ldpadatastr)
        ldap_client_server = ldpadata_json['ldap_client_server']
        ldap_client_server_port = ldpadata_json['ldap_client_server_port']
        ldap_base_dn = ldpadata_json['ldap_base_dn']
        ldap_bind_user = ldpadata_json['ldap_bind_user']
        ldap_bind_user_password = ldpadata_json['ldap_bind_user_password']
        if ldap_client_server != "" and ldap_client_server_port != "" and ldap_base_dn != "" and ldap_bind_user != "" and ldap_bind_user_password != "":
            info('LDAP integration start.')
            create_LDAP_user(ldap_client_server,ldap_client_server_port,ldap_base_dn,ldap_bind_user,ldap_bind_user_password)
            create_LDAP_group(ldap_client_server,ldap_client_server_port,ldap_base_dn,ldap_bind_user,ldap_bind_user_password)
            mapping_group_user(ldap_client_server,ldap_client_server_port,ldap_base_dn,ldap_bind_user,ldap_bind_user_password)
            info('LDAP integration finish.')
            result['status']  = 'success'
            result['message'] = _('LDAP 同步完成')
        else:
            result['status']  = 'fail'
            result['message'] = _('LDAP 設定值為空')
    except Exception as e:
        error("LDAP integration error:"+e.__str__())
        result['status']  = 'fail'
        result['message'] = _('LDAP 同步失敗 ,')+e.__str__()
    finally:
        GlobalObject.__statusObj__["ldapRunning"] = False
        return result