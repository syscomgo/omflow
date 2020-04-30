'''
set tags return templates
@author: Jia Liu
'''
from django import template
from omflow.syscom.common import check_ldap_app
from omflow.syscom.license import getVersion,getVersionType
register = template.Library()

@register.simple_tag
def get_ldap_bool():
    boolstr = check_ldap_app()
    return boolstr

@register.simple_tag
def onflow_version():
    version = getVersion()
    return version

@register.simple_tag
def omflow_version_type():
    version_type = getVersionType()
    return version_type