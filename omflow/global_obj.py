'''
Created on 2019年9月4日

@author: Kolin Hsu
'''

class GlobalObject():
    __userObj__ = {}
    __securityObj__ = {}
    __sidebarDesignObj__ = {}
    __chartCompileObj__ = {}
    __ldapObj__ = {}
    __statusObj__ = {"ldapRunning": False}




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
    
    
    #上架流程時建立flowactive
    def setFlowActive(self, fa):
        if fa:
            flow_uuid = fa.flow_uuid.hex
            flow_name = fa.flow_name
            app_id = fa.flow_app_id
            flow_id = fa.id
            self.flowactive[flow_uuid] = fa
            self.setIDDict(flow_id, flow_uuid)
            self.setNameDict(app_id, flow_name, flow_uuid)
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
            self.appname_dict[app_name] = app_id
            return True
        else:
            return False
    
    
    #刪除應用時刪除appname_dict
    def deleteAppNameDict(self, app_name):
        if app_name:
            result = self.appname_dict.pop(app_name)
            return result
        else:
            return False
    
    
    def ServerStart(self):
        from omformflow.models import FlowActive, ActiveApplication
        fa_list = list(FlowActive.objects.filter(undeploy_flag=False))
        aa_list = list(ActiveApplication.objects.filter(undeploy_flag=False).values('id','app_name'))
        for fa in fa_list:
            self.setFlowActive(fa)
        for aa in aa_list:
            app_id = str(aa['id'])
            app_name = aa['app_name']
            self.setAppNameDict(app_name, app_id)



FlowActiveGlobalObject = FlowActive()