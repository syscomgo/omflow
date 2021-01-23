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
    service_id = models.IntegerField(verbose_name = _('Service Id'), default=1, blank=True) 
    flow_uuid = models.UUIDField(verbose_name = _('Flow Uuid'), default=uuid.uuid4)
    role = models.TextField(verbose_name = _('Role'), blank=True)
    #content = models.TextField(verbose_name = _('服務設計'), blank=True) 
    default_value = models.TextField(verbose_name = _('Dfault Value'), blank=True)
    class Meta:
        default_permissions = ()

class OmServiceDesign(models.Model):
    '''
    service_structure
    author: Arthur
    '''
    content = models.TextField(verbose_name = _('Content'), blank=True)
    language_package = models.TextField(verbose_name= _('Language Package'), default='{}')
    class Meta:
        default_permissions = ()
        permissions = (
            ("OmServiceDesign_Manage", _('服務請求管理')),
        )