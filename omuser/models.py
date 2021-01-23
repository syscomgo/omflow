'''
omuser data model
Created on 2019年8月5日
@author: Pen Lin
'''
import uuid
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import UserFormatManager


class OmUser(AbstractUser):
    '''
    extent django default User Model
    '''
    #複寫email欄位,改為必填
    email = models.EmailField(verbose_name = _('Email'), unique=True) 

    #擴展欄位
    table_name = _('Table Name')
    nick_name = models.CharField(verbose_name = _('Nick Name'), max_length=50)
    birthday = models.DateField(verbose_name= _('Birthday'), null=True, blank=True)
    gender = models.CharField(verbose_name= _('Gender'), max_length=10,choices=(('male',_('男')),('female',_('女'))), default='male')
    phone1 = models.CharField(verbose_name= _('Phone1'), max_length=20,null=True, blank=True)
    phone2 = models.CharField(verbose_name= _('Phone2'), max_length=20,null=True, blank=True)
    department = models.CharField(verbose_name= _('Department'), max_length=200,null=True, blank=True)
    company = models.CharField(verbose_name= _('Company'), max_length=200,null=True, blank=True)
    ad_flag = models.BooleanField(verbose_name = _('AD Flage'), default=False)
    ad_sid = models.CharField(verbose_name = _('AD_SID'), max_length=100, null=True, blank=True)
    frequency = models.IntegerField(verbose_name= _('Frequency'), default=5)
    updatetime = models.DateTimeField(verbose_name = _('user Uuid'), auto_now=True)
    user_uuid = models.UUIDField(verbose_name = _('uuid'), default=uuid.uuid4, editable=False, unique=True)
    delete = models.BooleanField(verbose_name = _('Delete'), default=False)
    default_group = models.TextField(verbose_name = _('Default Group'), null=True, blank = True)
    substitute = models.TextField(verbose_name = _('Dubstitute'), default='[]')
    
    objects = UserFormatManager()
    
    class Meta:
        default_permissions = ()
        permissions = (
            ("OmUser_Add", _(' Add Table Name')),
            ("OmUser_Modify", _('Modify Table Name')),
            ("OmUser_View", _('View Table Name')),
            ("OmUser_Delete", _('Delete Table Name')),
        )
    @property
    def getJSON(self):
        pass
    def __str__(self):
        return self.username


class OmGroup(Group):
    '''
    extent django default Group Model
    author: Kolin Hsu
    '''
    table_name = _('table_name')
    parent_group = models.ForeignKey("self", blank=True, null=True, related_name="children_group", verbose_name = _('Parent Group'), on_delete=models.CASCADE)
    functional_flag = models.BooleanField(verbose_name = _('Functional Flag'), default=False)
    ad_flag = models.BooleanField(verbose_name = _('aAd Flag'), default=False)
    description = models.TextField(verbose_name = _('Description'), blank = True)
    display_name = models.CharField(verbose_name= _('Display Name'), max_length=200,null=True, blank=True)
    updatetime = models.DateTimeField(verbose_name = _('Update Time'), auto_now=True)
    group_uuid = models.UUIDField(verbose_name = _('Group Uuid'), default=uuid.uuid4, editable=False, unique=True)
    class Meta:
        default_permissions = ()
        permissions = (
            ("OmGroup_Add", _('OmGroup/Add')),
            ("OmGroup_Modify", _('OmGroup/Modify')),
            ("OmGroup_View", _('OmGroup/View')),
            ("OmGroup_Delete", _('OmGroup/Delete')),
        )