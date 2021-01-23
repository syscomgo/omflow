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
    table_name = _('Table Name')
    flow_uuid = models.UUIDField(verbose_name= _('Flow uuid'), null=True, blank=True)
    dataid_header = models.CharField(verbose_name= _('Dataid Header'), max_length=3)
    data_no = models.IntegerField(verbose_name = _('Data Number'), null=True, blank=True)
    history = models.BooleanField(verbose_name = _('History'), default=False)
    status = models.CharField(verbose_name= _('Status'), max_length=200,null=True, blank=True)
    title = models.CharField(verbose_name= _('Title'), max_length=200,null=True, blank=True)
    level = models.CharField(verbose_name= _('Level'), max_length=200,null=True, blank=True)
    group = models.CharField(verbose_name= _('Group'), max_length=500,null=True, blank=True)
    closed = models.BooleanField(verbose_name = _('Closed'), default=False)
    stop_uuid = models.TextField(verbose_name = _('Stop uuid'), blank=True, null=True)
    stop_chart_type = models.TextField(verbose_name = _('Stop Chart Type'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('Stop Chart Text'), blank=True, null=True)
    running = models.BooleanField(verbose_name = _('Running'), default=False)
    error = models.BooleanField(verbose_name = _('Error'), default=False)
    createtime = models.DateTimeField(verbose_name = _('Createtime'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('Updatetime'), auto_now=True)
    stoptime = models.DateTimeField(verbose_name = _('Stoptime'), null=True,blank=True)
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('Create User'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_dc33fb340034418c8fbb3baf15525e86')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('Update User'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_dc33fb340034418c8fbb3baf15525e86')
    data_param = models.TextField(verbose_name = _('Data Param'), null=True,blank=True)
    error_message = models.TextField(verbose_name = _('Error Message'), null=True,blank=True)
    init_data = models.ForeignKey('self', blank=True, null=True, related_name='extra_data', verbose_name = _('Inititial Data'), on_delete=models.CASCADE)
    is_child = models.BooleanField(verbose_name = _('is Child'), default=False)
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
            ('Omdata_dc33fb340034418c8fbb3baf15525e86_Add', _('Add')),
            ('Omdata_dc33fb340034418c8fbb3baf15525e86_Modify', _('Modefy')),
            ('Omdata_dc33fb340034418c8fbb3baf15525e86_View', _('View')),
            ('Omdata_dc33fb340034418c8fbb3baf15525e86_Delete', _('Delete')),
        )

class Omdata_dc33fb340034418c8fbb3baf15525e86_ValueHistory(models.Model):
    flow_uuid = models.UUIDField(verbose_name= _('Flow Uuid'), null=True, blank=True)
    data_no = models.IntegerField(verbose_name = _('Data No'), null=True, blank=True)
    data_id = models.IntegerField(verbose_name = _('Data Id'), blank=True, null=True)
    chart_id = models.CharField(verbose_name= _('Chart Id'), max_length=500,null=True, blank=True)
    stop_chart_type = models.TextField(verbose_name = _('Stop Chart Type'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('Stop Chart Text'), blank=True, null=True)
    input_data = models.TextField(verbose_name= _('Input Data'),null=True, blank=True)
    output_data = models.TextField(verbose_name= _('Output Data'),null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('Createtime'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('Updatetime'), auto_now=True)
    error = models.BooleanField(verbose_name = _('Error'), default=False)
    objects = FormatManager()
    class Meta:
        default_permissions = ()

class Omdata_dc33fb340034418c8fbb3baf15525e86_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('Create Time'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_dc33fb340034418c8fbb3baf15525e86 end>


#<Omdata_5eb104183f3945ecab83f94e53190bbb start>
#3
class Omdata_5eb104183f3945ecab83f94e53190bbb(models.Model):
    table_name = _('data entry')
    flow_uuid = models.UUIDField(verbose_name= _('Flow Uuid'), null=True, blank=True)
    dataid_header = models.CharField(verbose_name= _('dataid_header'), max_length=3)
    data_no = models.IntegerField(verbose_name = _('data_no'), null=True, blank=True)
    history = models.BooleanField(verbose_name = _('history'), default=False)
    status = models.CharField(verbose_name= _('status'), max_length=200,null=True, blank=True)
    title = models.CharField(verbose_name= _('title'), max_length=200,null=True, blank=True)
    level = models.CharField(verbose_name= _('level'), max_length=200,null=True, blank=True)
    group = models.CharField(verbose_name= _('group'), max_length=500,null=True, blank=True)
    closed = models.BooleanField(verbose_name = _('closed'), default=False)
    stop_uuid = models.TextField(verbose_name = _('stop_uuid'), blank=True, null=True)
    stop_chart_type = models.TextField(verbose_name = _('stop_chart_type'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('stop_chart_text'), blank=True, null=True)
    running = models.BooleanField(verbose_name = _('running'), default=False)
    error = models.BooleanField(verbose_name = _('error'), default=False)
    createtime = models.DateTimeField(verbose_name = _('createtime'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('updatetime'), auto_now=True)
    stoptime = models.DateTimeField(verbose_name = _('stoptime'), null=True,blank=True)
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('create_user'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_5eb104183f3945ecab83f94e53190bbb')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('update_user'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_5eb104183f3945ecab83f94e53190bbb')
    data_param = models.TextField(verbose_name = _('data_param'), null=True,blank=True)
    error_message = models.TextField(verbose_name = _('error_message'), null=True,blank=True)
    init_data = models.ForeignKey('self', blank=True, null=True, related_name='extra_data', verbose_name = _('init_data'), on_delete=models.CASCADE)
    is_child = models.BooleanField(verbose_name = _('is_child'), default=False)
    formitm_1 = models.TextField(null=True,blank=True)
    formitm_2 = models.TextField(null=True,blank=True)
    formitm_3 = models.TextField(null=True,blank=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
        permissions = (
            ('Omdata_5eb104183f3945ecab83f94e53190bbb_Add', _('Add data entry')),
            ('Omdata_5eb104183f3945ecab83f94e53190bbb_Modify', _('Modefy data entry')),
            ('Omdata_5eb104183f3945ecab83f94e53190bbb_View', _('view data entry')),
            ('Omdata_5eb104183f3945ecab83f94e53190bbb_Delete', _('Delete data entry')),
        )

class Omdata_5eb104183f3945ecab83f94e53190bbb_ValueHistory(models.Model):
    flow_uuid = models.UUIDField(verbose_name= _('Flow Uuid'), null=True, blank=True)
    data_no = models.IntegerField(verbose_name = _('Data No'), null=True, blank=True)
    data_id = models.IntegerField(verbose_name = _('Data Id'), blank=True, null=True)
    chart_id = models.CharField(verbose_name= _('Chart Id'), max_length=500,null=True, blank=True)
    stop_chart_type = models.TextField(verbose_name = _('Stop Chart Type'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('Stop Chart Text'), blank=True, null=True)
    input_data = models.TextField(verbose_name= _('Input Data'),null=True, blank=True)
    output_data = models.TextField(verbose_name= _('Output Data'),null=True, blank=True)
    createtime = models.DateTimeField(verbose_name = _('Create Time'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('Update Time'), auto_now=True)
    error = models.BooleanField(verbose_name = _('Error'), default=False)
    objects = FormatManager()
    class Meta:
        default_permissions = ()

class Omdata_5eb104183f3945ecab83f94e53190bbb_DataNo(models.Model):
    createtime = models.DateTimeField(verbose_name = _('Create Time'), auto_now_add=True)
    objects = FormatManager()
    class Meta:
        default_permissions = ()
#<Omdata_5eb104183f3945ecab83f94e53190bbb end>
#<new here>
