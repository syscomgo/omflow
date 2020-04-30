'''
flowdesign data model
Created on 2019年11月14日
@author: Kolin Hsu
'''

from django.db import models
from django.utils.translation import gettext as _
import uuid

class OmService(models.Model):
    '''
    service_objects
    author: Arthur
    '''
    service_id = models.IntegerField(verbose_name = _('服務編號'), default=1, blank=True) 
    flow_uuid = models.UUIDField(verbose_name = _('流程編號'), default=uuid.uuid4)
    role = models.TextField(verbose_name = _('允許角色'), blank=True)
    #content = models.TextField(verbose_name = _('服務設計'), blank=True) 
    default_value = models.TextField(verbose_name = _('預設值'), blank=True)
    class Meta:
        default_permissions = ()

class OmServiceDesign(models.Model):
    '''
    service_structure
    author: Arthur
    '''
    content = models.TextField(verbose_name = _('服務設計'), blank=True)
    class Meta:
        default_permissions = ()
        permissions = (
            ("OmServiceDesign_Manage", _('管理服務請求')),
        )