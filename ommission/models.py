'''
Created on 2020年04月06日
@author: Kolin Hsu
'''
from django.db import models
from django.utils.translation import gettext as _
from omflow.syscom.customfield import FormatManager



class Missions(models.Model):
    table_name = _('Table Name')
    flow_uuid = models.UUIDField(verbose_name= _('Flow Uuid'), null=True, blank=True)
    flow_name = models.TextField(verbose_name = _('Flow Name'), blank=True, null=True)
    status = models.TextField(verbose_name = _('Status'), blank=True, null=True)
    level = models.TextField(verbose_name = _('Level'), blank=True, null=True)
    title = models.TextField(verbose_name = _('Title'), blank=True, null=True)
    data_no = models.IntegerField(verbose_name = _('Data No'), null=True, blank=True)
    data_id = models.IntegerField(verbose_name = _('Data Id'), null=True, blank=True)
    history = models.BooleanField(verbose_name = _('History'), default=False)
    stop_uuid = models.TextField(verbose_name = _('Stop Uuid'), blank=True, null=True)
    stop_chart_text = models.TextField(verbose_name = _('Stop Chart Text'), blank=True, null=True)
    create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('Create User'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_ticket')
    update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('Update User'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_ticket')
    ticket_createtime = models.DateTimeField(verbose_name = _('Ticket Createtime'), blank=True, null=True)
    createtime = models.DateTimeField(verbose_name = _('Create Time'), auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name = _('Update Time'), auto_now=True)
    assignee = models.ForeignKey('omuser.OmUser', verbose_name = _('Assignee'), on_delete=models.SET_NULL, blank=True, null=True, related_name='my_mission')
    assign_group = models.ForeignKey('omuser.OmGroup', verbose_name = _('Assign Group'), on_delete=models.SET_NULL, blank=True, null=True, related_name='group_mission')
    action = models.TextField(verbose_name= _('Action'),null=True, blank=True)
    attachment = models.BooleanField(verbose_name = _('Attachment'), default=False)
    closed = models.BooleanField(verbose_name = _('Closed'), default=False)
    is_active = models.BooleanField(verbose_name = _('Is Active'), default=True)
    deploy_flag = models.BooleanField(verbose_name = _('Deploy Flag'), default=True)
    
    objects = FormatManager()
    
    class Meta:
        default_permissions = ()
