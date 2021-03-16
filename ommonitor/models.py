'''
Created on 2020年05月07日
@author: Kolin Hsu
'''
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager



class MonitorApplication(models.Model):
    '''
    author: Kolin Hsu
    '''
    app_name = models.CharField(max_length=200)
    user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    active_app_name = models.CharField(verbose_name= _('對應名稱'), max_length=200, null=True, blank=True)
    app_attr = models.CharField(verbose_name= _('屬性'), max_length=100)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
        permissions = (
            ("OmMonitor_Manage", _('資料收集管理')),
        )


class MonitorFlow(models.Model):
    '''
    author: Kolin Hsu
    '''
    table_id = models.TextField(verbose_name= _('資料表編號'), null=True, blank=True)
    flow_name = models.CharField(verbose_name= _('名稱'), max_length=200)
    description = models.TextField(verbose_name= _('說明'), null=True, blank=True)
    create_user = models.ForeignKey('omuser.OmUser', on_delete=models.SET_NULL, blank=True, null=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    formobject = models.TextField(verbose_name= _('流程表單設計'), null=True, blank=True)
    flowobject = models.TextField(verbose_name= _('流程設計'),null=True, blank=True)
    config = models.TextField(verbose_name= _('流程設定'),null=True, blank=True)
    subflow = models.TextField(verbose_name= _('子流程'),null=True, blank=True)
    attr = models.TextField(verbose_name= _('屬性'),null=True, blank=True)
    type = models.TextField(verbose_name= _('分類'),null=True, blank=True)
    os_type = models.TextField(verbose_name= _('作業系統'),null=True, blank=True)
    version = models.IntegerField(verbose_name= _('版本'),default=1)
    schedule = models.TextField(verbose_name= _('排程'),null=True, blank=True)
    event_rule = models.TextField(verbose_name= _('事件規則'),null=True, blank=True)
    flow_app = models.ForeignKey('MonitorApplication', on_delete=models.CASCADE)
    python_package = models.BooleanField(verbose_name = _('套件'), default=False)
    history = models.BooleanField(verbose_name = _('歷史資料'), default=False)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class Collector(models.Model):
    '''
    author: Kolin Hsu
    '''
    nick_name = models.CharField(verbose_name= _('顯示名稱'), max_length=100, null=True, blank=True)
    host_name = models.CharField(verbose_name= _('主機名稱'), max_length=100, null=True, blank=True)
    unique_id = models.TextField(verbose_name= _('主機識別碼'), max_length=100)
    os_type = models.CharField(verbose_name= _('作業系統'), max_length=100, null=True, blank=True)
    os_release = models.CharField(verbose_name= _('作業系統版本1'), max_length=100, null=True, blank=True)
    os_version = models.CharField(verbose_name= _('作業系統版本2'), max_length=100, null=True, blank=True)
    ip_address = models.CharField(verbose_name= _('IP位置'), max_length=100, null=True, blank=True)
    access_port = models.CharField(verbose_name= _('連接阜'), max_length=30, null=True, blank=True)
    omflow_version = models.CharField(verbose_name= _('omflow版本'), max_length=100, null=True, blank=True)
    nodegroup = models.ForeignKey('CollectorGroup', on_delete=models.SET_NULL, blank=True, null=True)
    loadbalance = models.BooleanField(verbose_name = _('負載平衡'), default=False)
    level = models.IntegerField(verbose_name= _('燈號'), default=1)
    software = models.TextField(verbose_name= _('軟體清單'), null=True, blank=True)
    hardware = models.TextField(verbose_name= _('硬體資訊'), null=True, blank=True)
    security = models.TextField(verbose_name= _('api碼'), null=True, blank=True)
    policys = models.ManyToManyField(MonitorFlow, through='PolicyCollector')
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now_add=True)
    active = models.BooleanField(verbose_name = _('啟用'), default=True)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class PolicyCollector(models.Model):
    '''
    author: Kolin Hsu
    '''
    node = models.ForeignKey(Collector, on_delete=models.CASCADE)
    policy = models.ForeignKey(MonitorFlow, on_delete=models.CASCADE)
    table_id = models.TextField(verbose_name= _('資料表編號'), null=True, blank=True)
    policy_version = models.IntegerField(verbose_name= _('版本'),null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()


class CollectorGroup(models.Model):
    '''
    author: Kolin Hsu
    '''
    name = models.TextField(verbose_name= _('群組名稱'), null=True, blank=True)
    type = models.TextField(verbose_name= _('類型'),null=True, blank=True)
    description = models.TextField(verbose_name = _('說明'), null=True, blank=True)
     
    class Meta:
        default_permissions = ()


#node紀錄分散處理queue資料
class LoadBalanceQueueData(models.Model):
    '''
    load balance Queue Data
    author: Kolin Hsu
    '''
    queue_id = models.TextField(verbose_name= _('佇列編號'), null=True, blank=True)
    module_name = models.TextField(verbose_name= _('模組名稱'), null=True, blank=True)
    method_name = models.TextField(verbose_name= _('方法名稱'), null=True, blank=True)
    input_param = models.TextField(verbose_name= _('輸入參數'), null=True, blank=True)
    
    class Meta:
        default_permissions = ()
        

#事件管理
class EventManagement(models.Model):
    '''
    author: Kolin Hsu
    '''
    application = models.TextField(verbose_name= _('應用程式'), null=True, blank=True)
    type = models.TextField(verbose_name= _('分類'), null=True, blank=True)
    title = models.TextField(verbose_name= _('標題'), null=True, blank=True)
    content = models.TextField(verbose_name= _('內文'), null=True, blank=True)
    critical = models.IntegerField(verbose_name= _('嚴重等級'), default=1)
    collector = models.ForeignKey('Collector', on_delete=models.SET_NULL, blank=True, null=True)
    source = models.TextField(verbose_name= _('來源'), null=True, blank=True)
    source2 = models.TextField(verbose_name= _('來源2'), null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('開單時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    closed = models.BooleanField(verbose_name = _('關單標記'), default=False)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
        
        
class IncidentRule(models.Model):
    '''
    author: Kolin Hsu
    '''
    rule = models.TextField(verbose_name= _('條件'), null=True, blank=True)
    
    class Meta:
        default_permissions = ()