'''
Created on 2019年11月14日
@author: Kolin Hsu
'''
#<import start>
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager
#<import end>


#<Omdata_dc33fb340034418c8fbb3baf15525e86 start>
#7
class Omdata_dc33fb340034418c8fbb3baf15525e86(models.Model):
    table_name = _('任務單')
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    dataid_header = models.CharField(verbose_name= _('資料代碼'), max_length=3)
    data_no = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
    history = models.BooleanField(verbose_name = _('歷史資料'), default=False)
    status = models.CharField(verbose_name= _('狀態'), max_length=200,null=True, blank=True)
    title = models.CharField(verbose_name= _('標題'), max_length=200,null=True, blank=True)
    level = models.CharField(verbose_name= _('燈號'), max_length=200,null=True, blank=True)
    group = models.CharField(verbose_name= _('受派群組'), max_length=500,null=True, blank=True)
    closed = models.BooleanField(verbose_name = _('關閉標記'), default=False)
    stop_uuid = models.TextField(verbose_name = _('關卡'), blank=True, null=True)
    stop_chart_type = models.TextField(verbose_name = _('關卡類型'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)
    running = models.BooleanField(verbose_name = _('執行標記'), default=False)
    error = models.BooleanField(verbose_name = _('是否異常'), default=False)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    stoptime = models.DateTimeField(verbose_name = _('停止時間'), null=True,blank=True)
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_dc33fb340034418c8fbb3baf15525e86')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_dc33fb340034418c8fbb3baf15525e86')
    data_param = models.TextField(verbose_name = _('流程參數'), null=True,blank=True)
    error_message = models.TextField(verbose_name = _('錯誤訊息'), null=True,blank=True)
    init_data = models.ForeignKey('self', blank=True, null=True, related_name='extra_data', verbose_name = _('初始資料'), on_delete=models.CASCADE)
    is_child = models.BooleanField(verbose_name = _('子單'), default=False)
    formitm_1 = models.TextField(null=True,blank=True)
    formitm_2 = models.TextField(null=True,blank=True)
    formitm_3 = models.TextField(null=True,blank=True)
    formitm_4 = models.TextField(null=True,blank=True)
    formitm_5 = models.TextField(null=True,blank=True)
    formitm_6 = models.TextField(null=True,blank=True)
    formitm_7 = models.TextField(null=True,blank=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_dc33fb340034418c8fbb3baf15525e86_Add', _('新增任務單')),
            ('Omdata_dc33fb340034418c8fbb3baf15525e86_Modify', _('修改任務單')),
            ('Omdata_dc33fb340034418c8fbb3baf15525e86_View', _('檢視任務單')),
            ('Omdata_dc33fb340034418c8fbb3baf15525e86_Delete', _('刪除任務單')),
        )

class Omdata_dc33fb340034418c8fbb3baf15525e86_ValueHistory(models.Model):
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    data_no = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
    data_id = models.IntegerField(verbose_name = _('多重資料編號'), blank=True, null=True)
    chart_id = models.CharField(verbose_name= _('功能點'), max_length=500,null=True, blank=True)
    stop_chart_type = models.TextField(verbose_name = _('關卡類型'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)
    input_data = models.TextField(verbose_name= _('輸入參數'),null=True, blank=True)
    output_data = models.TextField(verbose_name= _('輸出參數'),null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    error = models.BooleanField(verbose_name = _('異常標記'), default=False)
    objects = FormatManager()
    class Meta:
        default_permissions = ()

class Omdata_dc33fb340034418c8fbb3baf15525e86_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_dc33fb340034418c8fbb3baf15525e86 end>


#<Omdata_5eb104183f3945ecab83f94e53190bbb start>
#3
class Omdata_5eb104183f3945ecab83f94e53190bbb(models.Model):
    table_name = _('data entry')
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    dataid_header = models.CharField(verbose_name= _('資料代碼'), max_length=3)
    data_no = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
    history = models.BooleanField(verbose_name = _('歷史資料'), default=False)
    status = models.CharField(verbose_name= _('狀態'), max_length=200,null=True, blank=True)
    title = models.CharField(verbose_name= _('標題'), max_length=200,null=True, blank=True)
    level = models.CharField(verbose_name= _('燈號'), max_length=200,null=True, blank=True)
    group = models.CharField(verbose_name= _('受派群組'), max_length=500,null=True, blank=True)
    closed = models.BooleanField(verbose_name = _('關閉標記'), default=False)
    stop_uuid = models.TextField(verbose_name = _('關卡'), blank=True, null=True)
    stop_chart_type = models.TextField(verbose_name = _('關卡類型'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)
    running = models.BooleanField(verbose_name = _('執行標記'), default=False)
    error = models.BooleanField(verbose_name = _('是否異常'), default=False)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    stoptime = models.DateTimeField(verbose_name = _('停止時間'), null=True,blank=True)
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_5eb104183f3945ecab83f94e53190bbb')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_5eb104183f3945ecab83f94e53190bbb')
    data_param = models.TextField(verbose_name = _('流程參數'), null=True,blank=True)
    error_message = models.TextField(verbose_name = _('錯誤訊息'), null=True,blank=True)
    init_data = models.ForeignKey('self', blank=True, null=True, related_name='extra_data', verbose_name = _('初始資料'), on_delete=models.CASCADE)
    is_child = models.BooleanField(verbose_name = _('子單'), default=False)
    formitm_1 = models.TextField(null=True,blank=True)
    formitm_2 = models.TextField(null=True,blank=True)
    formitm_3 = models.TextField(null=True,blank=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_5eb104183f3945ecab83f94e53190bbb_Add', _('新增data entry')),
            ('Omdata_5eb104183f3945ecab83f94e53190bbb_Modify', _('修改data entry')),
            ('Omdata_5eb104183f3945ecab83f94e53190bbb_View', _('檢視data entry')),
            ('Omdata_5eb104183f3945ecab83f94e53190bbb_Delete', _('刪除data entry')),
        )

class Omdata_5eb104183f3945ecab83f94e53190bbb_ValueHistory(models.Model):
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    data_no = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
    data_id = models.IntegerField(verbose_name = _('多重資料編號'), blank=True, null=True)
    chart_id = models.CharField(verbose_name= _('功能點'), max_length=500,null=True, blank=True)
    stop_chart_type = models.TextField(verbose_name = _('關卡類型'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)
    input_data = models.TextField(verbose_name= _('輸入參數'),null=True, blank=True)
    output_data = models.TextField(verbose_name= _('輸出參數'),null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    error = models.BooleanField(verbose_name = _('異常標記'), default=False)
    objects = FormatManager()
    class Meta:
        default_permissions = ()

class Omdata_5eb104183f3945ecab83f94e53190bbb_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_5eb104183f3945ecab83f94e53190bbb end>
#<new here>
