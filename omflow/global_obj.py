'''
Created on 2019年9月4日

@author: Kolin Hsu
'''
import json

class GlobalObject():
    __userObj__ = {}                #api token物件
    __securityObj__ = {}            #api token物件
    __sidebarDesignObj__ = {}       #左側選單
    __chartCompileObj__ = {}        #python點編譯物件
    __ldapObj__ = {}                #ldap使用
    __statusObj__ = {"ldapRunning": False,'server_start_time':None, 'first_migrate':False}     #server端狀態
    __OmParameter__ = {}            #參數表
    __OrganizationObj__ = {}        #組織圖拆解物件
    __loadbalanceObj__ = {}         #分散運算uuid暫存區
    __loadbalanceMissionObj__ = {}  #分散運算collector分配的任務


class FlowActive():
    
    def __init__(self):
        '''
        init class
        author: Kolin Hsu
        '''
        self.flowactive = {}        #{flow_uuid : object}
        self.app_flowname_dict = {} #{app_id : {flow_name : flow_uuid}}
        self.id_dict = {}           #{flow_id : flow_uuid}
        self.uid_dict = {}          #{parent_uuid : {flow_uid : flow_uuid}}
        self.appname_dict = {}      #{app_name : app_id}
        self.api_path_dict = {}     #{api_path : flow_uuid}
        '''
        app_lan_dict是存放各app翻譯包的物件。
        {
            "active" : {app_id : lan_package}
            "workspace" : {app_id : lan_package}
        }
        '''
        self.app_lan_dict = {'active':{}, 'workspace':{}}
        '''
        sys_lan_dict系統相關翻譯包的物件。
        {
            service:{'en':{}, 'ja':{}, 'zh-hant':{}, 'zh-hans':{}} 
        }
        '''
        self.sys_lan_dict = {}
    
    
    #利用flow_uuid搜尋flowactive
    def UUIDSearch(self, flow_uuid):
        if flow_uuid:
            return self.flowactive.get(flow_uuid,None)
        else:
            return None
    
    
    #利用app_name或app_id及flow_name搜尋flowactive
    def NameSearch(self, flow_name, app_id=None, app_name=None):
        if app_id and flow_name:
            flow_uuid = self.NamegetUUID(flow_name, app_id)
            if flow_uuid:
                return self.UUIDSearch(flow_uuid)
            else:
                return None
        elif app_name and flow_name:
            app_id = self.getAppID(app_name)
            if app_id:
                flow_uuid = self.NamegetUUID(flow_name, app_id)
                if flow_uuid:
                    return self.UUIDSearch(flow_uuid)
                else:
                    return None
            else:
                return None
        else:
            return None
    
    def NamegetUUID(self, flow_name, app_id):
        if app_id and flow_name:
            app_id = str(app_id)
            return self.app_flowname_dict.get(app_id,{}).get(flow_name,'')
    
    
    def getAppID(self, app_name):
        if app_name:
            return self.appname_dict.get(app_name,'')
        else:
            return None
    
    
    #利用flow_id搜尋flowactive
    def IDSearch(self, flow_id):
        if flow_id:
            flow_uuid = self.IDgetUUID(flow_id)
            if flow_uuid:
                return self.UUIDSearch(flow_uuid)
            else:
                return None
        else:
            return None
    
    
    def IDgetUUID(self, flow_id):
        if flow_id:
            flow_id = str(flow_id)
            return self.id_dict.get(flow_id,'')
    
    
    #利用flow_uid搜尋flowactive
    def UIDSearch(self, flow_uid, parent_uuid):
        if flow_uid and parent_uuid:
            flow_uuid = self.UIDgetUUID(flow_uid, parent_uuid)
            if flow_uuid:
                return self.UUIDSearch(flow_uuid)
            else:
                return None
        else:
            return None
    
    
    def UIDgetUUID(self, flow_uid, parent_uuid):
        if flow_uid and parent_uuid:
            flow_uid = str(flow_uid)
            return self.uid_dict.get(parent_uuid,{}).get(flow_uid,'')
    
    
    #利用api_path搜尋flowactive
    def APISearch(self, api_path):
        if api_path:
            flow_uuid = self.APIgetUUID(api_path)
            if flow_uuid:
                return self.UUIDSearch(flow_uuid)
            else:
                return None
        else:
            return None
    
    
    def APIgetUUID(self, api_path):
        if api_path:
            return self.api_path_dict.get(api_path,'')

    def UUIDgetAPI(self, flow_uuid):
        if flow_uuid:
            for api_path in self.api_path_dict:
                if flow_uuid == self.api_path_dict[api_path]:
                    return api_path
        return None    
    
    #上架流程時建立flowactive
    def setFlowActive(self, fa):
        if fa:
            flow_uuid = fa.flow_uuid.hex
            flow_name = fa.flow_name
            app_id = fa.flow_app_id
            flow_id = fa.id
            api_path = fa.api_path
            self.flowactive[flow_uuid] = fa
            self.setIDDict(flow_id, flow_uuid)
            self.setNameDict(app_id, flow_name, flow_uuid)
            self.setAPIDict(flow_uuid, api_path)
            if fa.parent_uuid:
                parent_flow_uuid = fa.parent_uuid.hex
                flow_uid = fa.flow_uid
                self.setUIDDict(flow_uid, flow_uuid, parent_flow_uuid)
            return True
        else:
            return None
        
    
    def setNameDict(self, app_id, flow_name, flow_uuid):
        if app_id and flow_name and flow_uuid:
            app_id = str(app_id)
            flowname_dict = self.app_flowname_dict.get(app_id,{})
            if flowname_dict:
                self.app_flowname_dict[app_id][flow_name] = flow_uuid
            else:
                flowname_dict = {flow_name : flow_uuid}
                self.app_flowname_dict[app_id] = flowname_dict
            return True
        else:
            return None
        
    
    def setIDDict(self, flow_id, flow_uuid):
        if flow_id and flow_uuid:
            flow_id = str(flow_id)
            self.id_dict[flow_id] = flow_uuid
            return True
        else:
            return None
        
    
    def setUIDDict(self, flow_uid, flow_uuid, parent_flow_uuid):
        if flow_uid and flow_uuid and parent_flow_uuid:
            flow_uid = str(flow_uid)
            sub_dict = self.uid_dict.get(parent_flow_uuid,{})
            if sub_dict:
                self.uid_dict[parent_flow_uuid][flow_uid] = flow_uuid
            else:
                sub_dict = {flow_uid : flow_uuid}
                self.uid_dict[parent_flow_uuid] = sub_dict
            return True
        else:
            return None
    
    
    def setAPIDict(self, flow_uuid, api_path):
        if flow_uuid and api_path:
            self.api_path_dict[api_path] = flow_uuid
            return True
        else:
            return None
    
    
    #下架流程時刪除flowactive
    def deleteFlowActive(self, flow_uuid=None, flow_id=None):
        if flow_uuid or flow_id:
            try:
                if flow_id:
                    flow_id = str(flow_id)
                    flow_uuid = self.id_dict.get(flow_id,'')
                result = self.flowactive.pop(flow_uuid)
                flow_id = result.id
                self.deleteIDDict(flow_id)
                app_id = result.flow_app_id
                flow_name = result.flow_name
                self.deleteNameDict(app_id, flow_name)
                if result.parent_uuid:
                    parent_flow_uuid = result.parent_uuid.hex
                    flow_uid = result.flow_uid
                    self.deleteUIDDict(flow_uid, parent_flow_uuid)
                return result
            except:
                return None
        else:
            return None
        
    
    def deleteNameDict(self, app_id, flow_name):
        try:
            if app_id and flow_name:
                app_id = str(app_id)
                result = self.app_flowname_dict[app_id].pop(flow_name)
                return result
            elif app_id and not flow_name:
                app_id = str(app_id)
                result = self.app_flowname_dict.pop(app_id)
                return result
            else:
                return None
        except:
            return None
        
    
    def deleteIDDict(self, flow_id):
        if flow_id:
            try:
                flow_id = str(flow_id)
                result = self.id_dict.pop(flow_id)
                return result
            except:
                return None
        else:
            return None
        
    
    def deleteUIDDict(self, flow_uid, parent_flow_uuid):
        try:
            if flow_uid and parent_flow_uuid:
                flow_uid = str(flow_uid)
                result = self.uid_dict[parent_flow_uuid].pop(flow_uid)
                return result
            elif parent_flow_uuid and not flow_uid:
                flow_uid = str(flow_uid)
                result = self.uid_dict.pop(parent_flow_uuid)
                return result
            else:
                return None
        except:
            return None
    
    
    #上架應用時建立appname_dict
    def setAppNameDict(self, app_name, app_id):
        if app_name and app_id:
            app_id = str(app_id)
            self.appname_dict[app_name] = app_id
            return True
        else:
            return False
    
    
    #下架應用時刪除appname_dict
    def deleteAppNameDict(self, app_name):
        if app_name:
            result = self.appname_dict.pop(app_name)
            return result
        else:
            return False
    
    
    #建立/編輯應用或流程、上架應用時建立app_lan_dict
    def setAppLanDict(self, app_flow_type, app_id, app_name, lan_package):
        if app_id:
            app_id = str(app_id)
        if app_flow_type and (app_id or app_name) and lan_package:
            if isinstance(lan_package, str):
                lan_package = json.loads(lan_package)
            if app_name and app_flow_type == 'active':
                app_id = self.getAppID(app_name)
            if app_id:
                self.app_lan_dict[app_flow_type][app_id] = lan_package
                return True
            else:
                return False
        else:
            return False
    
    def setSysLanDict(self, name, lang, package):
        try:
            if lang:
                self.sys_lan_dict[name][lang] = package
            else:
                self.sys_lan_dict[name] = package
        except:
            pass
        
    def getSysLanDict(self, name):
        return self.sys_lan_dict.get(name,{})
        
    #刪除或下架應用時刪除app_lan_dict
    def deleteAppLanDict(self, app_flow_type, app_id=None, app_name=None):
        if app_id:
            app_id = str(app_id)
        if app_flow_type and (app_id or app_name):
            if app_name and app_flow_type == 'active':
                app_id = self.getAppID(app_name)
            if app_id:
                self.app_lan_dict[app_flow_type].pop(app_id)
                return True
            else:
                return False
        else:
            return False
        
        
    #取得app_lan_dict
    def getAppLanDict(self, app_flow_type, app_id=None, app_name=None):
        if app_id:
            app_id = str(app_id)
        if app_flow_type and (app_id or app_name):
            if app_name and app_flow_type == 'active':
                app_id = self.getAppID(app_name)
            if app_id:
                lan_package = self.app_lan_dict.get(app_flow_type,{}).get(app_id,{})
                return lan_package
            else:
                return {}
        else:
            return {}
    
    
    #啟動server時進行初始化
    def ServerStart(self):
        from omformflow.models import FlowActive, ActiveApplication, WorkspaceApplication
        fa_list = list(FlowActive.objects.filter(undeploy_flag=False))
        aa_list = list(ActiveApplication.objects.filter(undeploy_flag=False).values('id','app_name','language_package'))
        wa_list = list(WorkspaceApplication.objects.all().values('id','language_package'))
        
        for fa in fa_list:
            self.setFlowActive(fa)
        for aa in aa_list:
            app_id = str(aa['id'])
            app_name = aa['app_name']
            language_package = aa['language_package']
            self.setAppNameDict(app_name, app_id)
            self.setAppLanDict('active', app_id, None, language_package)
        for wa in wa_list:
            wapp_id = str(wa['id'])
            wa_language_package = wa['language_package']
            self.setAppLanDict('workspace', wapp_id, None, wa_language_package)
        
        #建立「服務請求」Global語言包
        from omservice.models import OmServiceDesign
        service_list = list(OmServiceDesign.objects.all().order_by("-id"))
        if len(service_list):
            if service_list[0].language_package:
                lan_package = json.loads(service_list[0].language_package)
            else:
                lan_package = {}
            self.sys_lan_dict['service'] = lan_package
            
FlowActiveGlobalObject = FlowActive()