from django.shortcuts import render
from django.utils.translation import gettext as _
from omflow.syscom.message import ResponseAjax, statusEnum
from omflow.global_obj import GlobalObject
from omflow.syscom.common import try_except
from omflow.syscom.default_logger import  info, error
from omldap.ldap_config import syncLDAP
from django.contrib.auth.decorators import login_required

@login_required
@try_except
def ldapCheckConnect(param):
    '''
    use ldap3 check connection
    input: use bind_user to connect LDAP 
    return: connection status
    author: Jia Liu
    ''' 
    return_result = {}
    try:
        from ldap3 import Server,Connection,ALL
        postdata = param.POST
        ldap_client_server = postdata.get('ldap_client_server','')
        ldap_client_server_port = postdata.get('ldap_client_server_port','')
        ldap_bind_user = postdata.get('ldap_bind_user','')
        ldap_bind_user_password = postdata.get('ldap_bind_user_password','')
        ldap_server = Server(host=ldap_client_server, port=int(ldap_client_server_port), use_ssl=False, get_info=ALL,connect_timeout=2)
        ldap_connection = Connection(ldap_server, user=ldap_bind_user, password=ldap_bind_user_password, auto_bind='NONE', version=3,
                                 authentication='SIMPLE', client_strategy='SYNC', auto_referrals=True, check_names=True,
                                 read_only=False, lazy=False,
                                 raise_exceptions=False,receive_timeout=2)
        ldap_connection.bind()
        result = ldap_connection.result
        if result['description'] == 'success':
            return_result["status"] = "success"
            return_result["message"] = _('LDAP連線成功')
            info('LDAP server connection is successful.')
        elif result['description'] == 'invalidCredentials':
            return_result["status"] = "invalidCredentials"
            return_result["message"] = _('LDAP帳號密碼錯誤')
            info('"%s" Wrong username or password.' % ldap_bind_user)
        ldap_connection.unbind()
        return return_result
    except Exception as e:
        error(e,param)
        return_result["status"] = "error"
        return_result["message"] = _('AD伺服器無法使用')
        return return_result        
@login_required
@try_except    
def ldapManualSync(param):
    '''
    LDAP manual Sync
    input: execute LDAP functions
    return: messages
    author: Pei Lin
    ''' 
    if GlobalObject.__statusObj__["ldapRunning"] == False:
        GlobalObject.__statusObj__["ldapRunning"] = True
        result = syncLDAP()
        return result
    else:
        result= {}
        result['status'] = 'in progress'
        result['message'] = _('LDAP更新正在執行')
        return result
#         return ResponseAjax(statusEnum.no_permission , _('LDAP更新正在執行')).returnJSON()
    
