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
    email = models.EmailField(verbose_name = _('電子郵件'), unique=True) 

    #擴展欄位
    table_name = _('使用者')
    nick_name = models.CharField(verbose_name = _('暱稱'), max_length=50)
    birthday = models.DateField(verbose_name= _('生日'), null=True, blank=True)
    gender = models.CharField(verbose_name= _('性別'), max_length=10,choices=(('male',_('男')),('female',_('女'))), default='male')
    phone1 = models.CharField(verbose_name= _('電話'), max_length=20,null=True, blank=True)
    phone2 = models.CharField(verbose_name= _('手機'), max_length=20,null=True, blank=True)
    department = models.CharField(verbose_name= _('部門名稱'), max_length=20,null=True, blank=True)
    company = models.CharField(verbose_name= _('公司名稱'), max_length=20,null=True, blank=True)
    ad_flag = models.BooleanField(verbose_name = _('AD標記'), default=False)
    ad_sid = models.CharField(verbose_name = _('AD_SID'), max_length=50, null=True, blank=True)
    frequency = models.IntegerField(verbose_name= _('更新頻率'), default=5)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    user_uuid = models.UUIDField(verbose_name = _('uuid'), default=uuid.uuid4, editable=False, unique=True)
    delete = models.BooleanField(verbose_name = _('刪除'), default=False)
    
    objects = UserFormatManager()
    
    class Meta:
        default_permissions = ()
        permissions = (
            ("OmUser_Add", _('新增使用者')),
            ("OmUser_Modify", _('修改使用者')),
            ("OmUser_View", _('檢視使用者')),
            ("OmUser_Delete", _('刪除使用者')),
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
    table_name = _('組織與角色')
    parent_group = models.ForeignKey("self", blank=True, null=True, related_name="children_group", verbose_name = _('上層群組'), on_delete=models.CASCADE)
    functional_flag = models.BooleanField(verbose_name = _('功能群組標記'), default=False)
    ad_flag = models.BooleanField(verbose_name = _('AD標記'), default=False)
    description = models.TextField(verbose_name = _('說明'), blank = True)
    display_name = models.CharField(verbose_name= _('顯示名稱'), max_length=20,null=True, blank=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    group_uuid = models.UUIDField(verbose_name = _('uuid'), default=uuid.uuid4, editable=False, unique=True)
    class Meta:
        default_permissions = ()
        permissions = (
            ("OmGroup_Add", _('新增組織/角色')),
            ("OmGroup_Modify", _('修改組織/角色')),
            ("OmGroup_View", _('檢視組織/角色')),
            ("OmGroup_Delete", _('刪除組織/角色')),
        )