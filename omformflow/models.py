'''
omformflow data model
Created on 2019年11月14日
@author: Kolin Hsu
'''
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager
from datetime import datetime
import time



class WorkspaceApplication(models.Model):
    '''
    author: Kolin Hsu
    '''
    app_name = models.CharField(max_length=100)
    user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), blank=True, null=True)
    active_app_name = models.CharField(verbose_name= _('對應名稱'), max_length=12, null=True, blank=True)
    app_attr = models.CharField(verbose_name= _('屬性'), max_length=10)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
        permissions = (
            ("OmFormFlow_Manage", _('自訂流程管理')),
        )


class FlowWorkspace(models.Model):
    '''
    form design
    author: Kolin Hsu
    '''
    flow_name = models.CharField(verbose_name= _('名稱'), max_length=12)
    description = models.TextField(verbose_name= _('說明'), null=True, blank=True)
    create_user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), blank=True, null=True)
    formobject = models.TextField(verbose_name= _('流程表單設計'), null=True, blank=True)
    flowobject = models.TextField(verbose_name= _('流程設計'),null=True, blank=True)
    config = models.TextField(verbose_name= _('流程設定'),null=True, blank=True)
    subflow = models.TextField(verbose_name= _('子流程'),null=True, blank=True)
    flow_app = models.ForeignKey('WorkspaceApplication', on_delete=models.CASCADE)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class ActiveApplication(models.Model):
    '''
    author: Kolin Hsu
    '''
    app_name = models.CharField(max_length=100)
    user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), blank=True, null=True)
    version = models.IntegerField(verbose_name= _('流程版本'), null=True, blank=True)
    app_attr = models.CharField(verbose_name= _('屬性'), max_length=10)
    undeploy_flag = models.BooleanField(verbose_name = _('下線'), default=False)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class FlowActive(models.Model):
    '''
    form design
    author: Kolin Hsu
    '''
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    flow_uid = models.TextField(verbose_name= _('uid'), null=True, blank=True)
    version = models.IntegerField(verbose_name= _('流程版本'), null=True, blank=True)
    parent_uuid = models.UUIDField(verbose_name= _('主流程編號'), null=True, blank=True)
    is_active = models.BooleanField(verbose_name = _('啟用/停用'), default=True)
    create_user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    flow_name = models.CharField(verbose_name= _('名稱'), max_length=12)
    description = models.TextField(verbose_name= _('說明'), null=True, blank=True)
    deploytime = models.DateTimeField(verbose_name = _('部署時間'), auto_now_add=True)
    undeploy_flag = models.BooleanField(verbose_name = _('下線'), default=False)
    undeploy_time = models.DateTimeField(verbose_name = _('下線時間'), null=True, blank=True)
    formobject = models.TextField(verbose_name= _('流程表單設計'), null=True, blank=True)
    flowobject = models.TextField(verbose_name= _('流程設計'),null=True, blank=True)
    formcounter = models.CharField(verbose_name= _('表單計數'), max_length=20,null=True, blank=True)
    flowcounter = models.CharField(verbose_name= _('流程計數'), max_length=20,null=True, blank=True)
    title_field = models.CharField(verbose_name= _('標題欄位'), max_length=20,null=True, blank=True)
    status_field = models.CharField(verbose_name= _('狀態欄位'), max_length=20,null=True, blank=True)
    common = models.BooleanField(verbose_name = _('共用'), default=False)
    flowlog = models.BooleanField(verbose_name = _('執行過程紀錄'), default=False)
    api = models.BooleanField(verbose_name = _('應用程式介面'), default=False)
    fp_show = models.BooleanField(verbose_name = _('查看目前流程及進度'), default=False)
    attachment = models.BooleanField(verbose_name = _('附加檔案功能'), default=False)
    relation = models.BooleanField(verbose_name = _('顯示關聯資料'), default=False)
    worklog = models.BooleanField(verbose_name = _('填寫及顯示工作日誌'), default=False)
    history = models.BooleanField(verbose_name = _('操作歷程'), default=False)
    display_field = models.TextField(verbose_name= _('要顯示的欄位'),null=True, blank=True)
    search_field = models.TextField(verbose_name= _('要查詢的欄位'),null=True, blank=True)
    flow_app = models.ForeignKey('ActiveApplication', on_delete=models.CASCADE)
    action1 = models.TextField(verbose_name= _('快速操作1'),null=True, blank=True)
    action2 = models.TextField(verbose_name= _('快速操作2'),null=True, blank=True)
    type = models.TextField(verbose_name= _('分類'),null=True, blank=True)
    permission = models.TextField(verbose_name= _('權限'),null=True, blank=True)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
        

def get_file_path(instance,filename):
    unixtime = int(time.mktime(datetime.now().timetuple()))
    return '{0}/{1}/{2}/{3}/{4}/{5}'.format(instance.__module__.replace(".models",""), instance.flow_uuid, instance.data_no, instance.data_id, unixtime, filename)


class OmdataFiles(models.Model):
    '''
    classdocs
    '''
    file = models.FileField(upload_to=get_file_path)
    size = models.IntegerField(verbose_name = _('大小'), blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    delete = models.BooleanField(verbose_name = _('是否刪除'), default=False)
    file_name = models.TextField(verbose_name= _('檔案名稱'),null=True, blank=True)
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    data_no = models.IntegerField(verbose_name = _('資料流水號'), null=True, blank=True)
    data_id = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
    upload_user = models.ForeignKey('omuser.OmUser', verbose_name = _('上傳人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_omdatefile')
     
    objects = FormatManager()
     
    class Meta:
        default_permissions = ()