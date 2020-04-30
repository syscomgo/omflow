from django.apps import AppConfig
from datetime import datetime
from omflow.syscom.constant import *
import json, os


class AppOmflowConfig(AppConfig):
    '''
    update omflow setting when start server
    input: main function 
    return: None
    author: Jia Liu
    '''
    name = 'omflow'
 
    def ready(self):
        import sys
        if (not 'makemigrations' in sys.argv) and (not 'migrate' in sys.argv):
            #set sidebar design to global object
            from omflow.global_obj import GlobalObject, FlowActiveGlobalObject
            from omflow.syscom.q_monitor import FormFlowMonitor, SchedulerMonitor
            from omflow.models import SystemSetting, QueueData
            from django.conf import settings
            from omflow.syscom.schedule_monitor import scheduleThread
            import threading
            #開發環境runserver的主線程功能只會監控子線程運作，以子線程為主要運行，子線程環境變數為True。
            if (os.environ.get('RUN_MAIN') == 'true') or "mod_wsgi" in sys.argv or "--noreload" in sys.argv:
                t1 = threading.Thread(target=FormFlowMonitor.setRunning)
                t1.start()
                t2 = threading.Thread(target=scheduleThread)
                t2.start()
                
            starttime = str(datetime.now())
            systemsetting = SystemSetting.objects.all()
            if systemsetting:
#                 if (os.environ.get('RUN_MAIN') == 'true') or "mod_wsgi" in sys.argv or "--noreload" in sys.argv:
#                     #將未完成的單放入form flow monitor
#                     q_l = list(QueueData.objects.all().values('module_name','method_name','input_param'))
#                     for q in q_l:
#                         FormFlowMonitor.putQueue(q['module_name'], q['method_name'], json.loads(q['input_param']))
                sidebar_design_str = SystemSetting.objects.get(name='sidebar_design').value
                sidebar_design = json.loads(sidebar_design_str)
                #ThreadPoolExecutor max workers
                POOL_MAX_WORKER = int(SystemSetting.objects.get(name='pool_max_worker').value)
                ldap_str = SystemSetting.objects.get(name='ldap_config').value
                ldap_json = json.loads(ldap_str)
            else:
                #create system user when first time run server
                from omuser.models import OmUser
                OmUser.objects.create_user(username='system',nick_name='system',password='system',email='system@system.com',is_superuser=True)
                #create sidebar design when first time run server
                app_list = settings.INSTALLED_APPS
                sidebar_design = []
                #check which app has been installed
                if 'omformflow' in app_list:
                    mymission = {"id":"mymission","name":"我的任務","p_id":"","flow_uuid":"default","icon":"commenting"}
                    service = {"id":"service","name":"服務請求","p_id":"","flow_uuid":"default","icon":"shopping-cart"}
                    customflow = {"id":"custom_1","name":"自訂應用","p_id":"","flow_uuid":"custom","icon":"folder"}
                    servicemanage = {"id":"servicemanage","name":"服務管理","p_id":"","flow_uuid":"default","icon":"headphones"}
                    servermanage = {"id":"servermanage","name":"資料收集","p_id":"","flow_uuid":"default","icon":"server"}
#                         report = {"id":"report","name":"報表","p_id":"","flow_uuid":"default","icon":"bar-chart"}
                    flowmgmt = {"id":"flowmgmt","name":"應用管理","p_id":"","flow_uuid":"default","icon":"cubes"}
                    sidebar_design.append(mymission)
                    sidebar_design.append(service)
                    sidebar_design.append(servicemanage)
                    sidebar_design.append(servermanage)
#                         sidebar_design.append(report)
                    sidebar_design.append(flowmgmt)
                    sidebar_design.append(customflow)
                staffmgmt = {"id":"staffmgmt","name":"人員管理","p_id":"","flow_uuid":"default","icon":"user"}
                syssetting = {"id":"syssetting","name":"系統設定","p_id":"","flow_uuid":"default","icon":"gear"}
                sidebar_design.append(staffmgmt)
                sidebar_design.append(syssetting)
                sidebar_design_str = json.dumps(sidebar_design)
                SystemSetting.objects.create(name='sidebar_design',description='side bar design json',value=sidebar_design_str)
                #ThreadPoolExecutor max workers
                POOL_MAX_WORKER = 50
                SystemSetting.objects.create(name='pool_max_worker',description='formflow thread pool max worker',value=POOL_MAX_WORKER)
                ldpadata_json = {'ldap_client_server':'','ldap_client_server_port':'','ldap_base_dn':'','ldap_bind_user':'','ldap_bind_user_password':'','ldap_client_domain':''}
                ldpadata_str = json.dumps(ldpadata_json)
                SystemSetting.objects.create(name='ldap_config',description='ldap connect setting',value=ldpadata_str)
                SystemSetting.objects.create(name='PI_agree',description='personal_information_agree',value=personal_information_agree)
                SystemSetting.objects.create(name='SU_agree',description='software_use_agree',value=software_use_agree)
            #設定global
            GlobalObject.__sidebarDesignObj__['sidebar_design'] = sidebar_design
            GlobalObject.__sidebarDesignObj__['design_updatetime'] = starttime
            GlobalObject.__sidebarDesignObj__['permission_updatetime'] = starttime
#             FormFlowMonitor.shutdownPool()
#             FormFlowMonitor.setPool(POOL_MAX_WORKER)
#             SchedulerMonitor.shutdownPool()
#             SchedulerMonitor.setPool(POOL_MAX_WORKER)
            GlobalObject.__ldapObj__['ldap_client_server'] = ldap_json['ldap_client_server']
            GlobalObject.__ldapObj__['ldap_client_server_port'] = ldap_json['ldap_client_server_port']
            GlobalObject.__ldapObj__['ldap_client_domain'] = ldap_json['ldap_client_domain']
            FlowActiveGlobalObject.ServerStart()
                

