'''
chat data model
Created on 2019年8月19日
@author: Kolin Hsu
'''

from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager


class Messages(models.Model):
    '''
    classdocs
    '''
    subject = models.CharField(verbose_name = _('主旨'), max_length=100)
    formid = models.CharField(verbose_name = _('表單編號'), blank=True, max_length=100)
    dataid = models.CharField(verbose_name = _('資料編號'), blank=True, max_length=100)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    flag = models.BooleanField(verbose_name = _('標記'), default=False)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
    @property
    def getJSON(self):
        pass
    def __str__(self):
        return self.subject


class HistoryMembers(models.Model):
    '''
    classdocs
    '''
    user = models.ForeignKey('omuser.OmUser', on_delete=models.CASCADE)
    messagehistory = models.ForeignKey('MessageHistory', on_delete=models.CASCADE)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
 
 
class HistoryGroups(models.Model):
    '''
    classdocs
    '''
    group = models.ForeignKey('omuser.OmGroup', on_delete=models.CASCADE)
    messagehistory = models.ForeignKey('MessageHistory', on_delete=models.CASCADE)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class MessageHistory(models.Model):
    '''
    classdocs
    '''
    create_user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    create_user_username = models.CharField(verbose_name = _('發送者名稱'), max_length=100, blank=True)
    create_group = models.ForeignKey('omuser.OmGroup', on_delete=models.SET_NULL, blank=True, null=True)
    create_group_name = models.CharField(verbose_name = _('發送群組名稱'), max_length=100, blank=True)
    delete_users_username = models.TextField(verbose_name = _('已刪除的接收者名稱'), blank=True)
    receive_groups_name = models.TextField(verbose_name = _('接收群組名稱'), blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    content = models.TextField(verbose_name = _('內文'), blank=True)
    messages = models.ForeignKey('Messages', on_delete=models.CASCADE)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class MessageBox(models.Model):
    '''
    classdocs
    '''
    read = models.BooleanField(verbose_name = _('是否讀取'), default=False)
    messages = models.ForeignKey('Messages', on_delete=models.CASCADE)
    messagehistory = models.ForeignKey('MessageHistory', on_delete=models.CASCADE)
    delete = models.BooleanField(verbose_name = _('是否刪除'), default=False)
    omuser = models.ForeignKey('omuser.OmUser', on_delete=models.CASCADE)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
        

def get_file_path(instance,filename):
    return '{0}/{1}/{2}'.format(instance.__module__.replace(".models",""),instance.main.id, filename)

        
class MessageHistoryFiles(models.Model):
    '''
    classdocs
    '''
    file = models.FileField(upload_to=get_file_path)
    size = models.IntegerField(verbose_name = _('大小'), blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    delete = models.BooleanField(verbose_name = _('是否刪除'), default=False)
    main = models.ForeignKey('MessageHistory', on_delete=models.CASCADE)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


