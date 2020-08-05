'''
set tags return templates
@author: Jia Liu
'''
from django import template
from omflow.syscom.common import check_app, License
from omformflow.views import checkOmDataPermission
register = template.Library()

@register.simple_tag
def get_ldap_bool():
    boolstr = check_app('omldap')
    return boolstr

@register.simple_tag
def get_org_bool():
    boolstr = check_app('omorganization')
    return boolstr

@register.simple_tag
def omflow_version():
    version = License().getVersion()
    return version

@register.simple_tag
def omflow_version_type():
    version_type = License().getVersionType()
    return version_type

@register.simple_tag
def omform_update_perms(user, flow_uuid, data_no, data_id, per_type):
    result = checkOmDataPermission(user, flow_uuid, data_no, data_id, per_type)
    return result