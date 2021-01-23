'''
flowdesign data model
Created on 2019年11月14日
@author: Kolin Hsu
'''

from django.db import models
from django.utils.translation import gettext as _
import uuid

class OmDashboard(models.Model):
    '''
    dashomdashboardign
    author: Arthur
    '''
    user = models.ForeignKey('omuser.OmUser', on_delete=models.CASCADE)
    content = models.TextField(verbose_name = _('Content'), blank=True)
    class Meta:
        default_permissions = ()
