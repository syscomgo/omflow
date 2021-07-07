'''
Created on 2019年11月14日
@author: Kolin Hsu
'''
#<import start>
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager
#<import end>


#<Omdata_65147887cf6a4237a3ae2b5584623d30 start>
#28
class Omdata_65147887cf6a4237a3ae2b5584623d30(models.Model):
    table_name = _('事故管理')
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
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_65147887cf6a4237a3ae2b5584623d30')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_65147887cf6a4237a3ae2b5584623d30')
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
    formitm_8 = models.TextField(null=True,blank=True)
    formitm_9 = models.TextField(null=True,blank=True)
    formitm_10 = models.TextField(null=True,blank=True)
    formitm_11 = models.TextField(null=True,blank=True)
    formitm_12 = models.TextField(null=True,blank=True)
    formitm_13 = models.TextField(null=True,blank=True)
    formitm_14 = models.TextField(null=True,blank=True)
    formitm_15 = models.TextField(null=True,blank=True)
    formitm_16 = models.TextField(null=True,blank=True)
    formitm_17 = models.TextField(null=True,blank=True)
    formitm_18 = models.TextField(null=True,blank=True)
    formitm_19 = models.TextField(null=True,blank=True)
    formitm_20 = models.TextField(null=True,blank=True)
    formitm_21 = models.TextField(null=True,blank=True)
    formitm_22 = models.TextField(null=True,blank=True)
    formitm_23 = models.TextField(null=True,blank=True)
    formitm_24 = models.TextField(null=True,blank=True)
    formitm_25 = models.TextField(null=True,blank=True)
    formitm_26 = models.TextField(null=True,blank=True)
    formitm_27 = models.TextField(null=True,blank=True)
    formitm_28 = models.TextField(null=True,blank=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_65147887cf6a4237a3ae2b5584623d30_Add', _('新增事故管理')),
            ('Omdata_65147887cf6a4237a3ae2b5584623d30_Modify', _('修改事故管理')),
            ('Omdata_65147887cf6a4237a3ae2b5584623d30_View', _('檢視事故管理')),
            ('Omdata_65147887cf6a4237a3ae2b5584623d30_Delete', _('刪除事故管理')),
        )

class Omdata_65147887cf6a4237a3ae2b5584623d30_ValueHistory(models.Model):
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

class Omdata_65147887cf6a4237a3ae2b5584623d30_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_65147887cf6a4237a3ae2b5584623d30 end>


#<Omdata_738e0f41896f4478bc20987b0852c2d4 start>
#29
class Omdata_738e0f41896f4478bc20987b0852c2d4(models.Model):
    table_name = _('問題管理')
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
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_738e0f41896f4478bc20987b0852c2d4')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_738e0f41896f4478bc20987b0852c2d4')
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
    formitm_8 = models.TextField(null=True,blank=True)
    formitm_9 = models.TextField(null=True,blank=True)
    formitm_10 = models.TextField(null=True,blank=True)
    formitm_11 = models.TextField(null=True,blank=True)
    formitm_12 = models.TextField(null=True,blank=True)
    formitm_13 = models.TextField(null=True,blank=True)
    formitm_14 = models.TextField(null=True,blank=True)
    formitm_15 = models.TextField(null=True,blank=True)
    formitm_16 = models.TextField(null=True,blank=True)
    formitm_17 = models.TextField(null=True,blank=True)
    formitm_18 = models.TextField(null=True,blank=True)
    formitm_19 = models.TextField(null=True,blank=True)
    formitm_20 = models.TextField(null=True,blank=True)
    formitm_21 = models.TextField(null=True,blank=True)
    formitm_22 = models.TextField(null=True,blank=True)
    formitm_23 = models.TextField(null=True,blank=True)
    formitm_24 = models.TextField(null=True,blank=True)
    formitm_25 = models.TextField(null=True,blank=True)
    formitm_26 = models.TextField(null=True,blank=True)
    formitm_27 = models.TextField(null=True,blank=True)
    formitm_28 = models.TextField(null=True,blank=True)
    formitm_29 = models.TextField(null=True,blank=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_738e0f41896f4478bc20987b0852c2d4_Add', _('新增問題管理')),
            ('Omdata_738e0f41896f4478bc20987b0852c2d4_Modify', _('修改問題管理')),
            ('Omdata_738e0f41896f4478bc20987b0852c2d4_View', _('檢視問題管理')),
            ('Omdata_738e0f41896f4478bc20987b0852c2d4_Delete', _('刪除問題管理')),
        )

class Omdata_738e0f41896f4478bc20987b0852c2d4_ValueHistory(models.Model):
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

class Omdata_738e0f41896f4478bc20987b0852c2d4_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_738e0f41896f4478bc20987b0852c2d4 end>


#<Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7 start>
#43
class Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7(models.Model):
    table_name = _('變更管理')
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
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_1e1f6c4c66b84d46bccbcd9f51f96bb7')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_1e1f6c4c66b84d46bccbcd9f51f96bb7')
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
    formitm_8 = models.TextField(null=True,blank=True)
    formitm_9 = models.TextField(null=True,blank=True)
    formitm_10 = models.TextField(null=True,blank=True)
    formitm_11 = models.TextField(null=True,blank=True)
    formitm_12 = models.TextField(null=True,blank=True)
    formitm_13 = models.TextField(null=True,blank=True)
    formitm_14 = models.TextField(null=True,blank=True)
    formitm_15 = models.TextField(null=True,blank=True)
    formitm_16 = models.TextField(null=True,blank=True)
    formitm_17 = models.TextField(null=True,blank=True)
    formitm_18 = models.TextField(null=True,blank=True)
    formitm_19 = models.TextField(null=True,blank=True)
    formitm_20 = models.TextField(null=True,blank=True)
    formitm_21 = models.TextField(null=True,blank=True)
    formitm_22 = models.TextField(null=True,blank=True)
    formitm_23 = models.TextField(null=True,blank=True)
    formitm_24 = models.TextField(null=True,blank=True)
    formitm_25 = models.TextField(null=True,blank=True)
    formitm_26 = models.TextField(null=True,blank=True)
    formitm_27 = models.TextField(null=True,blank=True)
    formitm_28 = models.TextField(null=True,blank=True)
    formitm_29 = models.TextField(null=True,blank=True)
    formitm_30 = models.TextField(null=True,blank=True)
    formitm_31 = models.TextField(null=True,blank=True)
    formitm_32 = models.TextField(null=True,blank=True)
    formitm_33 = models.TextField(null=True,blank=True)
    formitm_34 = models.TextField(null=True,blank=True)
    formitm_35 = models.TextField(null=True,blank=True)
    formitm_36 = models.TextField(null=True,blank=True)
    formitm_37 = models.TextField(null=True,blank=True)
    formitm_38 = models.TextField(null=True,blank=True)
    formitm_39 = models.TextField(null=True,blank=True)
    formitm_40 = models.TextField(null=True,blank=True)
    formitm_41 = models.TextField(null=True,blank=True)
    formitm_42 = models.TextField(null=True,blank=True)
    formitm_43 = models.TextField(null=True,blank=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7_Add', _('新增變更管理')),
            ('Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7_Modify', _('修改變更管理')),
            ('Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7_View', _('檢視變更管理')),
            ('Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7_Delete', _('刪除變更管理')),
        )

class Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7_ValueHistory(models.Model):
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

class Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_1e1f6c4c66b84d46bccbcd9f51f96bb7 end>


#<Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec start>
#13
class Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec(models.Model):
    table_name = _('發送流程')
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
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_a9016845ef2b4dc0bbf98c1cbd50e2ec')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_a9016845ef2b4dc0bbf98c1cbd50e2ec')
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
    formitm_8 = models.TextField(null=True,blank=True)
    formitm_9 = models.TextField(null=True,blank=True)
    formitm_10 = models.TextField(null=True,blank=True)
    formitm_11 = models.TextField(null=True,blank=True)
    formitm_12 = models.TextField(null=True,blank=True)
    formitm_13 = models.TextField(null=True,blank=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec_Add', _('新增發送流程')),
            ('Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec_Modify', _('修改發送流程')),
            ('Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec_View', _('檢視發送流程')),
            ('Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec_Delete', _('刪除發送流程')),
        )

class Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec_ValueHistory(models.Model):
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

class Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_a9016845ef2b4dc0bbf98c1cbd50e2ec end>


#<Omdata_2d2fe67815a34cafa606640bdc7a3209 start>
#25
class Omdata_2d2fe67815a34cafa606640bdc7a3209(models.Model):
    table_name = _('核准流程')
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
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_2d2fe67815a34cafa606640bdc7a3209')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_2d2fe67815a34cafa606640bdc7a3209')
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
    formitm_8 = models.TextField(null=True,blank=True)
    formitm_9 = models.TextField(null=True,blank=True)
    formitm_10 = models.TextField(null=True,blank=True)
    formitm_11 = models.TextField(null=True,blank=True)
    formitm_12 = models.TextField(null=True,blank=True)
    formitm_13 = models.TextField(null=True,blank=True)
    formitm_14 = models.TextField(null=True,blank=True)
    formitm_15 = models.TextField(null=True,blank=True)
    formitm_16 = models.TextField(null=True,blank=True)
    formitm_17 = models.TextField(null=True,blank=True)
    formitm_18 = models.TextField(null=True,blank=True)
    formitm_19 = models.TextField(null=True,blank=True)
    formitm_20 = models.TextField(null=True,blank=True)
    formitm_21 = models.TextField(null=True,blank=True)
    formitm_22 = models.TextField(null=True,blank=True)
    formitm_23 = models.TextField(null=True,blank=True)
    formitm_24 = models.TextField(null=True,blank=True)
    formitm_25 = models.TextField(null=True,blank=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_2d2fe67815a34cafa606640bdc7a3209_Add', _('新增核准流程')),
            ('Omdata_2d2fe67815a34cafa606640bdc7a3209_Modify', _('修改核准流程')),
            ('Omdata_2d2fe67815a34cafa606640bdc7a3209_View', _('檢視核准流程')),
            ('Omdata_2d2fe67815a34cafa606640bdc7a3209_Delete', _('刪除核准流程')),
        )

class Omdata_2d2fe67815a34cafa606640bdc7a3209_ValueHistory(models.Model):
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

class Omdata_2d2fe67815a34cafa606640bdc7a3209_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_2d2fe67815a34cafa606640bdc7a3209 end>


#<Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8 start>
#0
class Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8(models.Model):
    table_name = _('收件流程')
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
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_cf119f3e9198464f8fe1aff7a4e3e3b8')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_cf119f3e9198464f8fe1aff7a4e3e3b8')
    data_param = models.TextField(verbose_name = _('流程參數'), null=True,blank=True)
    error_message = models.TextField(verbose_name = _('錯誤訊息'), null=True,blank=True)
    init_data = models.ForeignKey('self', blank=True, null=True, related_name='extra_data', verbose_name = _('初始資料'), on_delete=models.CASCADE)
    is_child = models.BooleanField(verbose_name = _('子單'), default=False)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8_Add', _('新增收件流程')),
            ('Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8_Modify', _('修改收件流程')),
            ('Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8_View', _('檢視收件流程')),
            ('Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8_Delete', _('刪除收件流程')),
        )

class Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8_ValueHistory(models.Model):
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

class Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_cf119f3e9198464f8fe1aff7a4e3e3b8 end>
#<new here>
