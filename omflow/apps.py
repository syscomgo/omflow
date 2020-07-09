from django.apps import AppConfig
from datetime import datetime
from omflow.syscom.constant import personal_information_agree, software_use_agree
import json, os
from django.conf import settings


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
            from omflow.syscom.q_monitor import FormFlowMonitor, LoadBalanceMonitor
            from omflow.models import SystemSetting, QueueData
            from omflow.syscom.schedule_monitor import scheduleThread
            import threading
            
            starttime = str(datetime.now())
            GlobalObject.__statusObj__['server_start_time'] = datetime.now()
            #開發環境runserver的主線程功能只會監控子線程運作，以子線程為主要運行，子線程環境變數為True。
            if (os.environ.get('RUN_MAIN') == 'true') or "mod_wsgi" in sys.argv or "--noreload" in sys.argv:
                t1 = threading.Thread(target=FormFlowMonitor.setRunning)
                t1.start()
                t2 = threading.Thread(target=scheduleThread)
                t2.start()
            
            #確認是否為第一次啟動server
            systemsetting = SystemSetting.objects.all()
            if systemsetting:
                FlowActiveGlobalObject.ServerStart()
                if (os.environ.get('RUN_MAIN') == 'true') or "mod_wsgi" in sys.argv or "--noreload" in sys.argv:
                    #將未完成的單放入form flow monitor
                    q_l = list(QueueData.objects.all().values('module_name','method_name','input_param'))
                    for q in q_l:
                        FormFlowMonitor.putQueue(q['module_name'], q['method_name'], json.loads(q['input_param']))
                    from omflow.syscom.common import check_app
                    if settings.OMFLOW_TYPE == 'collector' and check_app('ommonitor'):
                        from ommonitor.models import LoadBalanceQueueData
                        #將未完成的python放入load balance monitor
                        q_l = list(LoadBalanceQueueData.objects.all().values('module_name','method_name','input_param'))
                        for q in q_l:
                            LoadBalanceMonitor.putQueue(q['module_name'], q['method_name'], json.loads(q['input_param']))
                sidebar_design_str = SystemSetting.objects.get(name='sidebar_design').value
                sidebar_design = json.loads(sidebar_design_str)
                GlobalObject.__sidebarDesignObj__['sidebar_design'] = sidebar_design
                GlobalObject.__sidebarDesignObj__['design_updatetime'] = starttime
                GlobalObject.__sidebarDesignObj__['permission_updatetime'] = starttime
                #ThreadPoolExecutor max workers
                POOL_MAX_WORKER = int(SystemSetting.objects.get(name='pool_max_worker').value)
                ldap_str = SystemSetting.objects.get(name='ldap_config').value
                ldap_json = json.loads(ldap_str)
            else:
                #create system user when first time run server
                from omuser.models import OmUser
                import uuid
                sysuser = OmUser.objects.create_user(username='system',nick_name='system',password=uuid.uuid4().hex,email='system@system.com',is_superuser=True)
                #create sidebar design when first time run server
                app_list = settings.INSTALLED_APPS
                sidebar_design = []
                #check which app has been installed
                if 'omformflow' in app_list:
                    mymission = {"id":"mymission","name":"我的任務","p_id":"","flow_uuid":"default","icon":"commenting"}
                    service = {"id":"service","name":"服務請求","p_id":"","flow_uuid":"default","icon":"shopping-cart"}
                    customflow = {"id":"custom_1","name":"自訂應用","p_id":"","flow_uuid":"custom","icon":"folder"}
                    servermanage = {"id":"servermanage","name":"資料收集","p_id":"","flow_uuid":"default","icon":"server"}
                    flowmgmt = {"id":"flowmgmt","name":"應用管理","p_id":"","flow_uuid":"default","icon":"cubes"}
                    sidebar_design.append(mymission)
                    sidebar_design.append(service)
                    sidebar_design.append(servermanage)
                    sidebar_design.append(flowmgmt)
                    sidebar_design.append(customflow)
                staffmgmt = {"id":"staffmgmt","name":"人員管理","p_id":"","flow_uuid":"default","icon":"user"}
                syssetting = {"id":"syssetting","name":"系統設定","p_id":"","flow_uuid":"default","icon":"gear"}
                sidebar_design.append(staffmgmt)
                sidebar_design.append(syssetting)
                sidebar_design_str = json.dumps(sidebar_design)
                SystemSetting.objects.create(name='sidebar_design',description='side bar design json',value=sidebar_design_str)
                GlobalObject.__sidebarDesignObj__['sidebar_design'] = sidebar_design
                GlobalObject.__sidebarDesignObj__['design_updatetime'] = starttime
                GlobalObject.__sidebarDesignObj__['permission_updatetime'] = starttime
                #ThreadPoolExecutor max workers
                POOL_MAX_WORKER = 10
                SystemSetting.objects.create(name='pool_max_worker',description='formflow thread pool max worker',value=POOL_MAX_WORKER)
                #ldap config
                ldpadata_json = {'ldap_client_server':'','ldap_client_server_port':'','ldap_base_dn':'','ldap_bind_user':'','ldap_bind_user_password':'','ldap_client_domain':''}
                ldpadata_str = json.dumps(ldpadata_json)
                SystemSetting.objects.create(name='ldap_config',description='ldap connect setting',value=ldpadata_str)
                #使用條款
                SystemSetting.objects.create(name='PI_agree',description='personal_information_agree',value=personal_information_agree)
                SystemSetting.objects.create(name='SU_agree',description='software_use_agree',value=software_use_agree)
                #node default group
                from ommonitor.models import CollectorGroup
                CollectorGroup.objects.create(name='未分類')
                CollectorGroup.objects.create(name='分散處理')
                #首次啟動匯入default流程
                firstrunImport(sysuser)
            #server, node啟動的事前準備
            if (os.environ.get('RUN_MAIN') == 'true') or "mod_wsgi" in sys.argv or "--noreload" in sys.argv:
                doPreProcessing()
            #設定global
            from omformflow.models import OmParameter
            op = list(OmParameter.objects.filter(group_id=None).values('name','value'))
            for i in op:
                GlobalObject.__OmParameter__[i['name']] = i['value']
            ldap_json ={}
            GlobalObject.__ldapObj__['ldap_client_server'] = ldap_json.get('ldap_client_server','')
            GlobalObject.__ldapObj__['ldap_client_server_port'] = ldap_json.get('ldap_client_server_port','')
            GlobalObject.__ldapObj__['ldap_client_domain'] = ldap_json.get('ldap_client_domain','')
            
                
def doPreProcessing():
    '''
    server建立schedule檢查node回報狀態
    node建立schedule向server回報狀態
    '''
    try:
        from omflow.syscom.common import License
        version_type = License().getVersionType()
        if version_type != 'C':
            if settings.OMFLOW_TYPE == 'server':
                method_name = 'checkNodeStatus'
            elif settings.OMFLOW_TYPE == 'collector':
                method_name = 'registerToServer'
            from omflow.models import Scheduler
            input_param = {'module_name':'ommonitor.views','method_name':method_name,'param':None}
            input_param_str = json.dumps(input_param)
            sch = Scheduler.objects.filter(input_param=input_param_str).exists()
            if not sch:
                from omflow.syscom.schedule_monitor import schedule_Execute
                exec_time = datetime.now()
                every = '3'
                cycle = 'Minutely'
                cycle_date = '[]'
                exec_fun = {'module_name':'omflow.syscom.schedule_monitor','method_name':'put_flow_job'}
                exec_fun_str = json.dumps(exec_fun)
                scheduler = Scheduler.objects.create(exec_time=exec_time,every=every,cycle=cycle,cycle_date=cycle_date,exec_fun=exec_fun_str,input_param=input_param_str,flowactive_id=None)
                schedule_Execute(scheduler)
            #SLA
            if settings.OMFLOW_TYPE == 'server':
                method_name = 'checkSLAData'
                input_param = {'module_name':'omformflow.views','method_name':method_name,'param':None}
                input_param_str = json.dumps(input_param)
                sch = Scheduler.objects.filter(input_param=input_param_str).exists()
                if not sch:
                    from omflow.syscom.schedule_monitor import schedule_Execute
                    exec_time = datetime.now()
                    every = '1'
                    cycle = 'Minutely'
                    cycle_date = '[]'
                    exec_fun = {'module_name':'omflow.syscom.schedule_monitor','method_name':'put_flow_job'}
                    exec_fun_str = json.dumps(exec_fun)
                    scheduler = Scheduler.objects.create(exec_time=exec_time,every=every,cycle=cycle,cycle_date=cycle_date,exec_fun=exec_fun_str,input_param=input_param_str,flowactive_id=None)
                    schedule_Execute(scheduler)
    except:
        pass
        

def firstrunImport(sysuser):
    try:
        from omflow.syscom.common import License
        version_type = License().getVersionType()
        if version_type != 'C':
            from ommonitor.views import importMonitorApplication
            from omformflow.views import deployWorkspaceApplication, importWorkspaceApplication
            from omformflow.models import WorkspaceApplication, OmParameter
            #匯入sys、lib流程
            flow_file_path = os.path.join(settings.BASE_DIR, "default_flow.omf")
            with open(flow_file_path,'r',encoding='UTF-8') as f:
                flow_file_content = f.read()
                f.close()
            if flow_file_content:
                ima_res = importWorkspaceApplication(flow_file_content, sysuser)
            #匯入default policy
            policy_file_path = os.path.join(settings.BASE_DIR, "default_policy.omf")
            with open(policy_file_path,'r',encoding='UTF-8') as f:
                policy_file_content = f.read()
                f.close()
            if policy_file_content:
                app_list = json.loads(policy_file_content)
                ima_res = importMonitorApplication(app_list, sysuser)
            #匯入default parameter
            param_file_path = os.path.join(settings.BASE_DIR, "default_param.omf")
            with open(param_file_path,'r',encoding='UTF-8') as f:
                param_file_content = f.read()
                f.close()
            if param_file_content:
                param_list = json.loads(param_file_content)
                OmParameter.objects.bulk_create([OmParameter(**param) for param in param_list])
            #上架匯入流程
            if ima_res['status']:
                wa_list = list(WorkspaceApplication.objects.all().values('id','app_name'))
                for wa in wa_list:
                    postdata = {'lside_pid':'','w_app_id':wa['id'],'app_name':wa['app_name']}
                    deployWorkspaceApplication(postdata, sysuser)
            WorkspaceApplication.objects.all().delete()
    except:
        pass