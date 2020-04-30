'''
Created on 2020年04月06日
@author: Kolin Hsu
'''
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager



class Missions(models.Model):
    table_name = _('我的任務')
    flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
    flow_name = models.TextField(verbose_name = _('流程名稱'), blank=True, null=True)
    status = models.TextField(verbose_name = _('狀態'), blank=True, null=True)
    level = models.TextField(verbose_name = _('燈號'), blank=True, null=True)
    title = models.TextField(verbose_name = _('標題'), blank=True, null=True)
    data_no = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
    data_id = models.IntegerField(verbose_name = _('資料流水號'), null=True, blank=True)
    history = models.BooleanField(verbose_name = _('歷史資料'), default=False)
    stop_uuid = models.TextField(verbose_name = _('關卡'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_ticket')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_ticket')
    ticket_createtime = models.DateTimeField(verbose_name = _('開單時間'), blank=True, null=True)
    createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
    assignee = models.ForeignKey('omuser.OmUser', verbose_name = _('受派人'), on_delete=models.SET_NULL, blank=True, null=True, related_name='my_mission')
    assign_group = models.ForeignKey('omuser.OmGroup', verbose_name = _('受派群組'), on_delete=models.SET_NULL, blank=True, null=True, related_name='group_mission')
    action = models.TextField(verbose_name= _('快速操作'),null=True, blank=True)
    attachment = models.BooleanField(verbose_name = _('附加檔案'), default=False)
    closed = models.BooleanField(verbose_name = _('關單'), default=False)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
