'''
Created on 2019年12月4日

@author: kailin
'''
from django.db import models
from django.utils.translation import gettext as _


class Position(models.Model):
    '''
    classdocs
    '''
    display_name = models.TextField(verbose_name= _('名稱'),null=True, blank=True)
    description = models.TextField(verbose_name= _('說明'),null=True, blank=True)
    class Meta:
        default_permissions = ()


class Organization(models.Model):
    '''
    classdocs
    '''
    name = models.TextField(verbose_name= _('名稱'),null=True, blank=True)
    value = models.TextField(verbose_name= _('值'),null=True, blank=True)
    class Meta:
        default_permissions = ()