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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('omuser.OmUser', on_delete=models.CASCADE)
    content = models.TextField(verbose_name = _('儀錶板設計'), blank=True)
    class Meta:
        default_permissions = ()
