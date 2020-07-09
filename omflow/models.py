'''
Created on 2019年12月4日

@author: kailin
'''
import uuid, os
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager
from django.dispatch import receiver


class SystemSetting(models.Model):
    '''
    left sidebar management
    author: Kolin Hsu
    '''
    name = models.CharField(verbose_name= _('名稱'), max_length=50)
    value = models.TextField(verbose_name = _('值'))
    description = models.TextField(verbose_name= _('說明'), null=True, blank=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class Scheduler(models.Model):
    '''
    Scheduler
    author: Kolin Hsu
    '''
    Recurrence = (   
                ("ONCE", _("執行一次")),
                ("SECONDLY", _("每秒鐘")),
                ("MINUTELY", _("每分鐘")),
                ("HOURLY", _("每小時")),
                ("DAILY", _("每天")),
                ("WEEKLY", _("每週")),
                ("MONTHLY", _("每月")),
            )
    create_time = models.DateTimeField(verbose_name= _('建立時間'),auto_now_add=True)
    exec_time = models.DateTimeField(verbose_name= _('執行時間'),null=True, blank=True)
    every = models.CharField(verbose_name= _('每次'),max_length=50,null=True, blank=True)
    cycle = models.CharField(verbose_name= _('週期'), max_length=50,choices=Recurrence,null=True, blank=True)
    cycle_date = models.CharField(verbose_name= _('週期執行日期'), max_length=50,null=True, blank=True)
    exec_fun = models.CharField(verbose_name= _('執行功能'), max_length=500)
    input_param = models.TextField(verbose_name = _('輸入參數'))
    is_active = models.BooleanField(verbose_name = _('啟用/停用'), default=True)
    last_exec_time = models.TextField(verbose_name = _('上次執行時間'), null=True, blank=True)
    next_exec_time = models.TextField(verbose_name = _('下次執行時間'), null=True, blank=True)
    flowactive = models.ForeignKey('omformflow.FlowActive', related_name="specific_flowactive",on_delete=models.SET_NULL, blank=True, null=True)
    type = models.TextField(verbose_name = _('分類'), null=True, blank=True)
    
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
        

class QueueData(models.Model):
    '''
    Queue Data
    author: Kolin Hsu
    '''
    queue_id = models.TextField(verbose_name= _('佇列編號'), null=True, blank=True)
    name = models.CharField(verbose_name= _('名稱'), max_length=50)
    module_name = models.TextField(verbose_name= _('模組名稱'), null=True, blank=True)
    method_name = models.TextField(verbose_name= _('方法名稱'), null=True, blank=True)
    input_param = models.TextField(verbose_name= _('輸入參數'), null=True, blank=True)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


def get_file_path(instance,filename):
    return '{0}/{1}/{2}'.format('temp', instance.mapping_id, filename)


class TempFiles(models.Model):
    '''
    classdocs
    '''
    file = models.FileField(upload_to=get_file_path)
    size = models.IntegerField(verbose_name = _('大小'), blank=True)
    file_name = models.TextField(verbose_name= _('檔案名稱'),null=True, blank=True)
    mapping_id = models.TextField(verbose_name= _('對照編號'),null=True, blank=True)
    class Meta:
        default_permissions = ()
        

@receiver(models.signals.post_delete, sender=TempFiles)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class Translation(models.Model):
    '''
    classdocs
    '''
    language = models.TextField(verbose_name= _('語言'),null=True, blank=True)
    trans = models.TextField(verbose_name= _('翻譯表'),null=True, blank=True)
    class Meta:
        default_permissions = ()