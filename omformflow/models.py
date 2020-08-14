'''
omformflow data model
Created on 2019年11月14日
@author: Kolin Hsu
'''
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager
# from datetime import datetime
# import time



class WorkspaceApplication(models.Model):
    '''
    author: Kolin Hsu
    '''
    app_name = models.CharField(max_length=200)
    user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), blank=True, null=True)
    active_app_name = models.CharField(verbose_name= _('對應名稱'), max_length=200, null=True, blank=True)
    app_attr = models.CharField(verbose_name= _('屬性'), max_length=100)
    language_package = models.TextField(verbose_name= _('語言包'), default='{}')
    
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
    flow_name = models.CharField(verbose_name= _('名稱'), max_length=200)
    description = models.TextField(verbose_name= _('說明'), null=True, blank=True)
    create_user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
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
    app_name = models.CharField(max_length=200)
    user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), blank=True, null=True)
    version = models.IntegerField(verbose_name= _('流程版本'), null=True, blank=True)
    app_attr = models.CharField(verbose_name= _('屬性'), max_length=100)
    undeploy_flag = models.BooleanField(verbose_name = _('下線'), default=False)
    language_package = models.TextField(verbose_name= _('語言包'), default='{}')
    
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
    attr = models.TextField(verbose_name= _('屬性'),null=True, blank=True)
    is_active = models.BooleanField(verbose_name = _('啟用/停用'), default=True)
    create_user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    flow_name = models.CharField(verbose_name= _('名稱'), max_length=200)
    description = models.TextField(verbose_name= _('說明'), null=True, blank=True)
    deploytime = models.DateTimeField(verbose_name = _('部署時間'), auto_now_add=True)
    undeploy_flag = models.BooleanField(verbose_name = _('下線'), default=False)
    undeploy_time = models.DateTimeField(verbose_name = _('下線時間'), null=True, blank=True)
    formobject = models.TextField(verbose_name= _('流程表單設計'), null=True, blank=True)
    merge_formobject = models.TextField(verbose_name= _('整合表單設計'), null=True, blank=True)
    flowobject = models.TextField(verbose_name= _('流程設計'),null=True, blank=True)
    formcounter = models.CharField(verbose_name= _('表單計數'), max_length=200,null=True, blank=True)
    flowcounter = models.CharField(verbose_name= _('流程計數'), max_length=200,null=True, blank=True)
    title_field = models.CharField(verbose_name= _('標題欄位'), max_length=500,null=True, blank=True)
    status_field = models.CharField(verbose_name= _('狀態欄位'), max_length=500,null=True, blank=True)
    common = models.BooleanField(verbose_name = _('共用'), default=False)
    flowlog = models.BooleanField(verbose_name = _('執行過程紀錄'), default=False)
    api = models.BooleanField(verbose_name = _('應用程式介面'), default=False)
    fp_show = models.BooleanField(verbose_name = _('查看目前流程及進度'), default=False)
    attachment = models.BooleanField(verbose_name = _('附加檔案功能'), default=False)
    relation = models.BooleanField(verbose_name = _('顯示關聯資料'), default=False)
    worklog = models.BooleanField(verbose_name = _('填寫及顯示工作日誌'), default=False)
    history = models.BooleanField(verbose_name = _('操作歷程'), default=False)
    mission = models.BooleanField(verbose_name = _('建立任務'), default=True)
    display_field = models.TextField(verbose_name= _('要顯示的欄位'),null=True, blank=True)
    search_field = models.TextField(verbose_name= _('要查詢的欄位'),null=True, blank=True)
    flow_app = models.ForeignKey('ActiveApplication', on_delete=models.CASCADE)
    action1 = models.TextField(verbose_name= _('快速操作1'),null=True, blank=True)
    action2 = models.TextField(verbose_name= _('快速操作2'),null=True, blank=True)
    type = models.TextField(verbose_name= _('分類'),null=True, blank=True)
    permission = models.TextField(verbose_name= _('權限'),null=True, blank=True)
    api_path = models.CharField(verbose_name= _('api路徑'), max_length=500,null=True, blank=True)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
        

def get_file_path(instance,filename):
#     unixtime = int(time.mktime(datetime.now().timetuple()))
    return '{0}/{1}/{2}/{3}/{4}'.format(instance.__module__.replace(".models",""), instance.flow_uuid, instance.data_no, instance.data_id, filename)


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
        
class OmdataRelation(models.Model):
    '''
    classdocs
    '''
    subject_flow = models.UUIDField(verbose_name= _('主表單流程'), null=True, blank=True)
    subject_no = models.IntegerField(verbose_name = _('主資料編號'), null=True, blank=True)
    relation_type = models.TextField(verbose_name= _('關聯類型'),null=True, blank=True)
    relation_percentage = models.IntegerField(verbose_name = _('被影響百分比'), null=True, blank=True)
    object_flow = models.UUIDField(verbose_name= _('副表單流程'),null=True, blank=True)
    object_no = models.IntegerField(verbose_name = _('副資料編號'), null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('建立人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True)
     
    objects = FormatManager()
     
    class Meta:
        default_permissions = ()


class OmdataWorklog(models.Model):
    '''
    classdocs
    '''
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    data_no = models.IntegerField(verbose_name = _('資料流水號'), null=True, blank=True)
    content = models.TextField(verbose_name= _('內容'),null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('建立人'), on_delete=models.SET_NULL, blank=True, null=True, related_name='create_worklog')
     
    objects = FormatManager()
     
    class Meta:
        default_permissions = ()


class OmParameter(models.Model):
    '''
    classdocs
    '''
    name = models.TextField(verbose_name= _('參數名稱'), null=True, blank=True)
    value = models.TextField(verbose_name = _('參數值'), null=True, blank=True)
    type = models.TextField(verbose_name= _('類型'),null=True, blank=True)
    description = models.TextField(verbose_name= _('說明'),null=True, blank=True)
    shadow = models.BooleanField(verbose_name = _('是否遮蔽'), default=False)
    group_id = models.TextField(verbose_name= _('群組id'),null=True, blank=True)
     
    objects = FormatManager()
     
    class Meta:
        default_permissions = ()
    

class SLARule(models.Model):
    '''
    classdocs
    '''
    sla_name = models.CharField(verbose_name= _('服務水準名稱'), max_length=200)
    description = models.TextField(verbose_name= _('說明'), null=True, blank=True)
    app_name = models.CharField(verbose_name= _('應用名稱'), max_length=200)
    flow_name = models.CharField(verbose_name= _('流程名稱'), max_length=200)
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    type = models.TextField(verbose_name= _('類型'),null=True, blank=True)
    timer_start = models.TextField(verbose_name= _('時間測量開始'),null=True, blank=True)
    timer_end = models.TextField(verbose_name= _('時間測量終止'),null=True, blank=True)
    advanced = models.TextField(verbose_name= _('進階條件'),null=True, blank=True)
    target = models.TextField(verbose_name= _('數值測量欄位'),null=True, blank=True)
    remind = models.TextField(verbose_name= _('提醒'),null=True, blank=True)
    violation = models.TextField(verbose_name= _('違反'),null=True, blank=True)
    title = models.TextField(verbose_name= _('標題'),null=True, blank=True)
    content = models.TextField(verbose_name= _('內容'),null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    notify_createuser = models.BooleanField(verbose_name = _('通知開單人'), default=False)
    notify_group = models.TextField(verbose_name= _('通知角色'),null=True, blank=True)
    notify_user = models.TextField(verbose_name= _('通知人'),null=True, blank=True)
       
    objects = FormatManager()
       
    class Meta:
        default_permissions = ()
 
 
class SLAData(models.Model):
    '''
    classdocs
    '''
    sla = models.ForeignKey('SLARule', on_delete=models.CASCADE)
    type = models.TextField(verbose_name= _('類型'), default='num')
    app_name = models.CharField(verbose_name= _('應用名稱'), max_length=200)
    flow_name = models.CharField(verbose_name= _('流程名稱'), max_length=200)
    data_no = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    remind = models.TextField(verbose_name= _('提醒'), null=True, blank=True)
    violation = models.TextField(verbose_name= _('違反'), null=True, blank=True)
    level = models.CharField(verbose_name = _('燈號'), max_length=50, default='green')
    closed = models.BooleanField(verbose_name = _('關閉標記'), default=False)
      
    objects = FormatManager()
      
    class Meta:
        default_permissions = ()
    