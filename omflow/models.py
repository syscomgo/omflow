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
    name = models.CharField(verbose_name= _('name'), max_length=50)
    value = models.TextField(verbose_name = _('value'))
    description = models.TextField(verbose_name= _('description'), null=True, blank=True)
    updatetime = models.DateTimeField(verbose_name = _('updatetime'), auto_now=True)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class Scheduler(models.Model):
    '''
    Scheduler
    author: Kolin Hsu
    '''
    Recurrence = (   
                ("ONCE", _("ONCE")),
                ("SECONDLY", _("SECONDLY")),
                ("MINUTELY", _("MINUTELY")),
                ("HOURLY", _("HOURLY")),
                ("DAILY", _("DAILY")),
                ("WEEKLY", _("WEEKLY")),
                ("MONTHLY", _("MONTHLY")),
            )
    create_time = models.DateTimeField(verbose_name= _('Create Time'),auto_now_add=True)
    exec_time = models.DateTimeField(verbose_name= _('Exec Time'),null=True, blank=True)
    every = models.CharField(verbose_name= _('Every'),max_length=50,null=True, blank=True)
    cycle = models.CharField(verbose_name= _('Cycle'), max_length=50,choices=Recurrence,null=True, blank=True)
    cycle_date = models.CharField(verbose_name= _('Cycle Date'), max_length=50,null=True, blank=True)
    exec_fun = models.CharField(verbose_name= _('Exec Fun'), max_length=500)
    input_param = models.TextField(verbose_name = _('Input Param'))
    is_active = models.BooleanField(verbose_name = _('Is Active'), default=True)
    last_exec_time = models.TextField(verbose_name = _('Last executing Time'), null=True, blank=True)
    next_exec_time = models.TextField(verbose_name = _('Next Executing Time'), null=True, blank=True)
    flowactive = models.ForeignKey('omformflow.FlowActive', related_name="specific_flowactive",on_delete=models.SET_NULL, blank=True, null=True)
    type = models.TextField(verbose_name = _('type'), null=True, blank=True)
    
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
        

class QueueData(models.Model):
    '''
    Queue Data
    author: Kolin Hsu
    '''
    queue_id = models.TextField(verbose_name= _('Queue Id'), null=True, blank=True)
    name = models.CharField(verbose_name= _('Name'), max_length=50)
    module_name = models.TextField(verbose_name= _('Module Name'), null=True, blank=True)
    method_name = models.TextField(verbose_name= _('Method Name'), null=True, blank=True)
    input_param = models.TextField(verbose_name= _('Input Parameter'), null=True, blank=True)
    
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
    size = models.IntegerField(verbose_name = _('Size'), blank=True)
    file_name = models.TextField(verbose_name= _('File Name'),null=True, blank=True)
    mapping_id = models.TextField(verbose_name= _('Mapping Id'),null=True, blank=True)
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
    language = models.TextField(verbose_name= _('Language'),null=True, blank=True)
    trans = models.TextField(verbose_name= _('Translating'),null=True, blank=True)
    class Meta:
        default_permissions = ()