'''
Created on 2019年12月25日
@author: kailin
'''
import json, re, datetime
from omflow.models import QueueData, TempFiles
from omflow.syscom.q_monitor import FormFlowMonitor
from omflow.syscom.common import DataChecker, getModel, FormatToFormdataList
from omflow.global_obj import FlowActiveGlobalObject
from django.utils.translation import gettext as _
from omflow.models import Scheduler
from omflow.syscom.schedule_monitor import schedule_Execute
from omflow.syscom.license import getVersion
from ommission.views import createMission, setMission
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from omflow.syscom.default_logger import debug



class OmEngine():
    '''
    author: Kolin Hsu
    '''
    
    def __init__(self,flow_uuid,data):
        '''
        OME的初始化動作
        '''
        self.flow_uuid = flow_uuid
        self.data = data
        self.next_chart_item = None
        self.last_chart_item = None
        self.version = None
        self.flow_value = data.get('flow_value','')
        self.data_no = data.get('data_no','')
        self.data_id = data.get('data_id','')
        self.error_pass = None
        self.flowobject = None
        self.table_uuid = data.get('table_uuid',None)
        self.flowlog = data.get('flowlog',None)
        self.app_id = None
        self.action = None
    
    def checkActive(self):
        '''
        OME的開頭檢查，檢查該流程是否存在、是否已經停用
        '''
        #function variable
        require_field = ['flow_uuid','data']
        chart_id_to = self.data.get('chart_id_to','')
        chart_id_from = self.data.get('chart_id_from','')
        check_data = {}
        check_data['flow_uuid'] = self.flow_uuid
        check_data['data'] = self.data
        debug('flow_uuid: %s   data_no: %s  chart_id_from: %s   chart_id_to: %s' % (self.flow_uuid, self.data_no, chart_id_from, chart_id_to))
        #server side rule check
        checker = DataChecker(check_data, require_field)
        if checker.get('status') == 'success':
            #取得流程物件
            try:
                flowactive = FlowActiveGlobalObject.UUIDSearch(self.flow_uuid)
                #檢查流程使否啟用
                if flowactive.is_active:
                    self.app_id = flowactive.flow_app_id
                    self.version = flowactive.version
                    self.flowobject = json.loads(flowactive.flowobject)
                    #找出上一個點以及下一個點
                    flowobject_items = self.flowobject['items']
                    for f_item in flowobject_items:
                        if f_item['id'] == chart_id_to:
                            self.next_chart_item = f_item
                        elif f_item['id'] == chart_id_from:
                            self.last_chart_item = f_item
                    #找出快速操作設定
                    if self.next_chart_item:
                        if self.next_chart_item['type'] == 'form':
                            action1_text = ''
                            action2_text = ''
                            if flowactive.action1:
                                action1 = json.loads(flowactive.action1).get(chart_id_to,'')
                                if action1:
                                    action1_text = action1['text']
                            if flowactive.action2:
                                action2 = json.loads(flowactive.action2).get(chart_id_to,'')
                                if action2:
                                    action2_text = action2['text']
                            self.action = action1_text + ',' + action2_text
                    #取得錯誤是否通過
                    if self.last_chart_item:
                        self.error_pass = self.last_chart_item['config'].get('error_pass',False)
                    else:
                        self.error_pass = self.data.get('error_pass',False)
                    return self.differentiateLastType()
                else:
                    ms = _('該流程目前為停用狀態。')
                    self.markError(chart_id_from, '', ms)
                    return ms
            except Exception as e:
                debug('OME CheckActive error:     %s' % e.__str__())
                ms = _('該流程沒有已部署的版本')
                self.markError(chart_id_from, '', ms)
                return ms
        else:
            self.markError(chart_id_from, '', checker.get('message',''))
            return checker.get('message','')
    
    
    def differentiateLastType(self):
        '''
        確認上一個點的類型
        '''
        flag = 'from'
        if self.last_chart_item:
            chart_type = self.last_chart_item.get('type','')
            if chart_type == 'start':
                return self.startPoint(flag)
            elif chart_type == 'end':
                return self.endPoint(flag)
            elif chart_type == 'python':
                return self.pythonPoint(flag)
            elif chart_type == 'async':
                return self.asyncPoint(flag)
            elif chart_type == 'form':
                return self.formPoint(flag)
            elif chart_type == 'collection':
                return self.collectionPoint(flag)
            elif chart_type == 'subflow':
                return self.subflowPoint(flag)
            elif chart_type == 'outflow':
                return self.outflowPoint(flag)
            elif chart_type == 'switch':
                return self.switchPoint(flag)
            elif chart_type == 'sleep':
                return self.sleepPoint(flag)
            elif chart_type == 'setform':
                return self.setformPoint(flag)
            elif chart_type == 'inflow':
                return self.inflowPoint(flag)
        else:
            return self.differentiateNextType()
    
    
    def startPoint(self,flag):
        '''
        開始點
        '''
        log = True
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                #log output
                self.outputLog(log, chart_id, '')
                return self.checkError(chart_id, chart_text)
            elif flag == 'to':
                chart = self.next_chart_item
                config = chart['config']
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                hp_result = self.has_preflow(chart)
                config_input_list = config['input']
                #get start input
                try:
                    start_input = self.data.pop('start_input')
                except:
                    start_input = None
                if start_input:
                    for i in start_input:
                        self.flow_value[i] = start_input[i]
                #取得table資料
                require_list = []
                formdata = self.data.get('formdata','')
                for config_input in config_input_list:
                    name = config_input['name'] #建立變數名稱
                    value = config_input['value'] #值/欄位
                    require = config_input['require']
                    if not start_input:
                        #確認value是要取得table還是本身
                        if value == None:
                            c_input_value = ''
                        elif '#' in value: 
                            if not formdata:
                                omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                                formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                            c_input_value = self.regexInOutputValue(formdata, value)
                        else:
                            c_input_value = value
                        #寫入flow value
                        self.flow_value[name] = c_input_value
                    if require == True or require == 'true' or require == 'True':
                        require_list.append(name)
                require_check = self.inputRequireCheck(require_list, self.flow_value)
                if require_check == None:
                    if hp_result['status'] == 'N':
                        if self.data.get('chart_input',''): #子流程或驗證
                            subflow_input = self.data.get('chart_input','')
                            for key in subflow_input:
                                if subflow_input[key]:
                                    self.flow_value[key] = subflow_input[key]
                            if self.data.get('preflow_content',''):
                                log = False
                        else:
                            formdata = self.data.get('formdata','')
                            if formdata:
                                formdata['data_param'] = json.dumps(self.data)
                                #get omdata model
                                omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                                #create ticket
                                omdatano_model = getModel('omformmodel','Omdata_' + self.table_uuid + '_DataNo')
                                data_no = omdatano_model.objects.create().id
                                formdata['data_no'] = data_no
                                self.data_no = data_no
                                self.data['data_no'] = data_no
                                m = omdata_model.objects.create(**formdata)
                                m.init_data_id = m.id
                                m.save()
                                #create mymission
                                mission_param = {}
                                mission_param['flow_uuid'] = m.flow_uuid
                                mission_param['flow_name'] = omdata_model.table_name
                                mission_param['status'] = m.status
                                mission_param['level'] = m.level
                                mission_param['title'] = m.title
                                mission_param['data_no'] = m.data_no
                                mission_param['data_id'] = m.id
                                mission_param['stop_uuid'] = chart_id
                                mission_param['stop_chart_text'] = chart_text
                                mission_param['history'] = True
                                mission_param['create_user_id'] = m.create_user_id
                                mission_param['ticket_createtime'] = m.init_data.createtime
                                createMission(mission_param)
                                self.data_id = m.id
                                self.data['data_id'] = m.id
                                self.data.pop('formdata')
                                #move file from temp to omdata if mapping_id has value
                                if self.data.get('mapping_id',''):
                                    files = []
                                    mapping_id = self.data.pop('mapping_id')
                                    file_list = list(TempFiles.objects.filter(mapping_id=mapping_id))
                                    for i in file_list:
                                        new_file = ContentFile(i.file.read())
                                        new_file.name = i.file.name
                                        file_obj = UploadedFile(new_file, i.file_name, None, i.size, None)
                                        files.append(file_obj)
                                        i.file.close()
                                    from omformflow.views import uploadOmdataFiles
                                    uploadOmdataFiles(files, m.flow_uuid, m.data_no, m.id, m.create_user_id)
                                    TempFiles.objects.filter(mapping_id=mapping_id).delete()
                        self.inputLog(log, chart_id, self.flow_value, chart_text, chart_type)
                        return self.replaceFromTo()
                    elif hp_result['status'] == 'Y':
                        try:
                            input_obj = {}
                            subflow_input_list = chart['config']['subflow_input']
                            formdata = self.data.get('formdata','')
                            require_list = []
                            #get chart's input
                            for subflow_input in subflow_input_list:
                                value = subflow_input['value'] #值/變數/欄位
                                name = subflow_input['name'] #變數
                                require = subflow_input['require']
                                #確認name是要取得table還是flow value還是本身
                                if value == None or not value:
                                    input_obj[name] = ''
                                elif '$' in value:
                                    input_obj[name] = self.flow_value.get(value[2:-1],'')
                                elif '#' in value:
                                    if not formdata:
                                        omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                                        formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                                    input_obj[name] = self.regexInOutputValue(formdata, value)
                                else:
                                    input_obj[name] = value
                                if require == True or require == 'true' or require == 'True':
                                    require_list.append(name)
                            #確認是否為必填欄位
                            require_check = self.inputRequireCheck(require_list, input_obj)
                            if require_check == None:
                                self.data['chart_input'] = input_obj
                                #set preflow data
                                preflow_uuid = self.has_preflow(chart)['value']
                                data_str = json.dumps(self.data)
                                preflow_content = json.loads(data_str)
                                preflow_content.pop('chart_input')
                                new_data = json.loads(data_str)
                                new_data['flow_uuid'] = preflow_uuid
#                                 new_data.pop('formdata')
                                new_data['preflow_content'] = preflow_content
                                self.__init__(preflow_uuid, new_data)
                                return self.checkActive()
                            else:
                                return _('缺少必填變數：' + require_check)
                        except Exception as e:
                            debug('OME StartPoint error:     %s' % e.__str__())
                    elif hp_result['status'] in ['E','F']:
                        #remove file from temp db if mapping_id has value
                        if self.data.get('mapping_id',''):
                            mapping_id = self.data.pop('mapping_id')
                            TempFiles.objects.filter(mapping_id=mapping_id).delete()
                        return hp_result['value']
                else:
                    return _('缺少必填變數：'+ require_check)
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(開始點)，請通知系統管理員。<br>') + e.__str__())
    
    
    def endPoint(self,flag):
        '''
        結束點
        '''
        log = True
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                #function variable
                calculate_temp_dict = {}
                chart = self.last_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                content = self.data.get('content','')
                preflow_content = self.data.get('preflow_content','')
                outflow_content = self.data.get('outflow_content','')
                config = chart['config']
                output_obj = {}
                config_output_list = config.get('output','')
                if config_output_list:
                    #get last chart's output
                    formdata = {}
                    #calculate
                    calculate_list = config.get('calculate','')
                    if calculate_list:
                        calculate_temp_dict = self.calculate(calculate_list, formdata)
                    for config_output in config_output_list:
                        name = config_output['name'][2:-1] #輸出參數名稱
                        value = config_output['value'] #flow_value變數名稱
                        #組裝寫入value history db的變數
                        if value == None:
                            output_obj[name] = ''
                        elif '$' in value:
                            value = value[2:-1]
                            if calculate_temp_dict.get(value,None) == None:
                                output_obj[name] = self.flow_value[value]
                            else:
                                output_obj[name] = calculate_temp_dict[value]
                        
                        elif '#' in value:
                            if not formdata:
                                omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                                formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                            output_obj[name] = self.regexInOutputValue(formdata, value)
                        else:
                            output_obj[name] = value
                #log output
                self.outputLog(log, chart_id, output_obj)
                if self.data.get('error','') and (not self.error_pass):
                    error_message = self.data.get('error_message','')
                    return self.markError(chart_id,chart_text,error_message)
                else:
                    #remove queue form db
                    queue_id = self.flow_uuid + str(self.data_id) + str(chart_id)
                    try:
                        QueueData.objects.get(queue_id=queue_id).delete()
                    except:
                        pass
                    #get ommodel
                    model_name = 'Omdata_' + self.table_uuid
                    model = getModel('omformmodel', model_name)
                    data_dumps = json.dumps(self.data)
                    #資料驗證流程
                    if preflow_content:
                        #更新 flow value
                        if output_obj['result'] == 'success':
                            preflow_content['preflow_done'] = True
                        else:
                            preflow_content['preflow_done'] = False
                        self.__init__(preflow_content['flow_uuid'], preflow_content)
                        #回call check active
                        return self.checkActive()
                    #子流程
                    elif content:
                        #update flow value
                        model.objects.filter(id=self.data_id).update(data_param=data_dumps)
                        content['chart_input'] = output_obj
                        self.__init__(content['flow_uuid'], content)
                        return self.checkActive()
                    elif outflow_content:
                        stoptime = datetime.datetime.now()
                        #set outside flow's ticket closed
                        model.objects.filter(id=self.data_id).update(running=False,closed=True,stop_uuid=chart_id,stop_chart_text=chart_text,stoptime=stoptime,data_param=data_dumps)
                        #set mission closed
                        setMission('closed', self.flow_uuid, self.data_no, None, None)
                        #get outflow content
                        outflow_content['outflow_done'] = True
                        #把外部流程的單號跟流程編號拋給父流程
                        output_obj['outflow_uuid'] = self.flow_uuid
                        output_obj['outflow_data_no'] = self.data_no
                        outflow_content['chart_input'] = output_obj
                        self.__init__(outflow_content['flow_uuid'], outflow_content)
                        #回call check active
                        return self.checkActive()
                    #主流程
                    else:
                        stoptime = datetime.datetime.now()
                        #set ticket closed
                        model.objects.filter(id=self.data_id).update(running=False,closed=True,stop_uuid=chart_id,stop_chart_text=chart_text,stoptime=stoptime,data_param=data_dumps)
                        #set mission closed
                        setMission('closed', self.flow_uuid, self.data_no, None, None)
                        debug('close ticket, %s   no. %s  endpoint-output:      %s' % (self.flow_uuid, self.data_no, output_obj))
            elif flag == 'to':
                #log input
                chart = self.next_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                input_value = ''
                self.inputLog(log, chart_id, input_value, chart_text, chart_type)
                return self.replaceFromTo()
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(結束點)，請通知系統管理員。<br>') + e.__str__())
        
    
    def pythonPoint(self,flag):
        '''
        程式碼功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                in_output = self.data['chart_input']
                chart_id = chart['id']
                chart_text = chart['text']
                config = chart['config']
                if self.data.get('autoinstall',False):
                    self.data.pop('autoinstall')
                #log output
                log = config.get('log','')
                output_obj = {}
                config_output_list = config.get('output','')
                if config_output_list:
                    #get last chart's output
                    for config_output in config_output_list:
                        name = config_output['name'][2:-1] #flow_value變數名稱
                        value = config_output['value'][2:-1] #chart變數名稱
                        #回寫flow_value
                        self.flow_value[name] = in_output[value]
                        #組裝寫入value history db的變數
                        output_obj[name] = in_output[value]
                    self.outputLog(log, chart_id, output_obj)
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                #log input
                chart = self.next_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                config = chart['config']
                log = config.get('log',False)
                autoinstall = config.get('autoinstall',False)
                self.data['autoinstall'] = autoinstall
                return self.inputProcess(log)
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(程式碼點)，請通知系統管理員。<br>') + e.__str__())
    
    
    def formPoint(self,flag):
        '''
        人工處理功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                config = chart['config']
                log = config.get('log',False)
                config_output_list = config['output']
                model = getModel('omformmodel', 'Omdata_' + self.table_uuid)
                table_dict = model.objects.getdictformat(id=self.data_id)
                output_dict = {}
                for config_output in config_output_list:
                    name = config_output['name'][2:-1]  #flow_value變數
                    value = config_output['value']  #欄位
                    c_output_value = self.regexInOutputValue(table_dict, value)
                    #寫入flow value
                    self.flow_value[name] = c_output_value
                    #寫入output dict
                    output_dict[name] = c_output_value
                #log output
                self.outputLog(log, chart_id, output_dict)
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                chart = self.next_chart_item
                config = chart['config']
                log = config.get('log',False)
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                check_preflow = False
                if self.last_chart_item:
                    write_from_dict = {}
                    #calculate
                    formdata= {}
                    calculate_list = config.get('calculate','')
                    calculate_temp_dict = {}
                    if calculate_list:
                        calculate_temp_dict = self.calculate(calculate_list, formdata)
                    #欄位設定
                    require_list = []
                    temp_dict = {}
                    config_input_list = config['input']
                    for config_input in config_input_list:
                        name = config_input['name'] #欄位名稱
                        value = config_input['value'] #變數/值
                        #確認value是要取得flow value還是本身
                        if value == None or not value:
                            c_input_value = ''
                        elif '$' in value:
                            value = value[2:-1]
                            if calculate_temp_dict.get(value,None) == None:
                                c_input_value = self.flow_value[value]
                            else:
                                c_input_value = calculate_temp_dict[value]
                        else:
                            c_input_value = value
                        #放入暫存dict
                        if re.match(r'#[A-Z][0-9]+\(.+\)', name):
                            num = int(re.findall(r'#[A-Z]([0-9]+)\(.+\)', name)[0])
                            name = re.findall(r'#[A-Z][0-9]+\((.+)\)', name)[0]
                            l_index = num - 1
                            l = temp_dict.get(name,[])
                            for i in range(l_index):
                                if len(l)-i:
                                    pass
                                else:
                                    l.append('')
                            l.append(c_input_value)
                            temp_dict[name] = l
                        elif re.match(r'#\(.+\)', name):
                            name = re.findall(r'#\((.+)\)', name)[0]
                            temp_dict[name] = c_input_value
                        else:
                            temp_dict[name] = c_input_value
                        #確認該欄位是否為必填
                        require = config_input['require']
                        if require == True or require == 'true' or require == 'True':
                            require_list.append(name.lower())
                    #組成寫回資料庫的dict
                    formdata_list = []
                    formobject_items = self.flowobject['form_object']['items']
                    for key in temp_dict:
                        name = key
                        value = temp_dict[key]
                        for item in formobject_items:
                            if item['id'] == name:
                                FormatToFormdataList(item, value, formdata_list)
                                break
                    if formdata_list:
                        for item in formdata_list:
                            item_id = item['id'].lower()
                            value = item['value']
                            if isinstance(value, dict):
                                new_value = json.dumps(value)
                            elif isinstance(value, list):
                                new_value = json.dumps(value)
                            elif isinstance(value, str):
                                new_value = value
                            elif value == None:
                                new_value = ''
                            else:
                                new_value = str(value)
                            write_from_dict[item_id] = new_value
                    #檢查必填欄位
                    require_check = self.inputRequireCheck(require_list, write_from_dict)
                    if require_check == None:
                        self.inputLog(log, chart_id, write_from_dict, chart_text, chart_type)
                        #get omdata and change running status
                        stoptime = datetime.datetime.now()
                        stop_uuid = self.getchartpath(chart_id)
                        model_name = 'Omdata_' + self.table_uuid
                        model = getModel('omformmodel', model_name)
                        write_from_dict['running'] = False
                        write_from_dict['stop_uuid'] = stop_uuid
                        write_from_dict['stop_chart_text'] = chart_text
                        write_from_dict['stoptime'] = stoptime
                        write_from_dict['history'] = True
                        write_from_dict['data_param'] = json.dumps(self.data)
                        model.objects.filter(id=self.data_id).update(**write_from_dict)
                        o_m = list(model.objects.filter(id=self.data_id).values())[0]
                        o_m.pop('id')
                        o_m.pop('history')
                        #create new omdata
                        m = model.objects.create(**o_m)
                        if m.group:
                            #create mymission
                            mission_param = {}
                            mission_param['flow_uuid'] = m.flow_uuid
                            mission_param['flow_name'] = model.table_name
                            mission_param['status'] = m.status
                            mission_param['level'] = m.level
                            mission_param['title'] = m.title
                            mission_param['data_no'] = m.data_no
                            mission_param['data_id'] = m.id
                            mission_param['stop_uuid'] = stop_uuid
                            mission_param['stop_chart_text'] = chart_text
                            mission_param['create_user_id'] = m.create_user_id
                            mission_param['ticket_createtime'] = m.init_data.createtime
                            mission_param['action'] = self.action
                            group = json.loads(m.group)
                            mission_param['assignee_id'] = group['user']
                            mission_param['assign_group_id'] = group['group']
                            createMission(mission_param)
                        #remove queue db
                        last_chart_id = self.data.get('chart_id_from','')
                        ex_queue_id = self.flow_uuid + str(self.data_id) + str(last_chart_id)
                        try:
                            QueueData.objects.get(queue_id=ex_queue_id).delete()
                        except:
                            pass
                    else:
                        return self.markError(chart_id,chart_text,_('缺少必填變數：' + require_check))
                else:
                    check_preflow = True
                if check_preflow:
                    hp_result = self.has_preflow(chart)
                    if hp_result['status'] == 'N':
                        #沒有資料驗證或是已經驗證完畢
                        return self.replaceFromTo()
                    elif hp_result['status'] == 'F':
                        #資料驗證的結果為不通過
                        return self.markError(chart_id, chart_text, hp_result['value'], True)
                    elif hp_result['status'] == 'Y':
                        #有資料驗證必須執行
                        input_obj = {}
                        subflow_input_list = chart['config']['subflow_input']
                        table_dict = None
                        #get chart's input
                        for subflow_input in subflow_input_list:
                            value = subflow_input['value'] #變數/欄位/字串
                            name = subflow_input['name'] #變數名稱
                            #確認name是要取得table還是flow value還是本身
                            if value == None or not value:
                                input_obj[name] = ''
                            elif '$' in value:
                                input_obj[name] = self.flow_value.get(value[2:-1],'')
                            elif '#' in value:
                                if table_dict == None:
                                    model = getModel('omformmodel', 'Omdata_' + self.table_uuid)
                                    table_dict = model.objects.getdictformat(id=self.data_id)
                                input_obj[name] = self.regexInOutputValue(table_dict, value)
                            else:
                                input_obj[name] = value
                            #確認是否為必填欄位
                            if not input_obj[name]:
                                require = subflow_input['require']
                                if require == True or require == 'true' or require == 'True':
                                    return _('缺少必填變數：'+name)
                        self.data['chart_input'] = input_obj
                        #set preflow data
                        preflow_uuid = self.has_preflow(chart)['value']
                        data_str = json.dumps(self.data)
                        preflow_content = json.loads(data_str)
                        preflow_content.pop('chart_input')
                        new_data = json.loads(data_str)
                        new_data['chart_id_to'] = 'FITEM_1'
                        new_data['flow_uuid'] = preflow_uuid
                        new_data['preflow_content'] = preflow_content
                        self.__init__(preflow_uuid, new_data)
                        return self.checkActive()
                    elif hp_result['status'] == 'E':
                        #找不到資料驗證的流程
                        return self.markError(chart_id, chart_text, hp_result['value'])
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(人工點)，請通知系統管理員。<br>') + e.__str__())
    
    
    def asyncPoint(self,flag):
        '''
        並行功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                chart_id = chart['id']
                config = chart['config']
                log = config.get('log',False)
                chart_text = chart['text']
                #create omdata
                model_name = 'Omdata_' + self.table_uuid
                omdata_model = getModel('omformmodel', model_name)
                main_ticket = list(omdata_model.objects.filter(id=self.data_id).values())[0]
                main_ticket.pop('id')
                m = omdata_model.objects.create(**main_ticket)
                self.data_id = m.id
                self.data['data_id'] = m.id
                self.outputLog(log, chart_id, '')
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                #close main ticket
                chart = self.next_chart_item
                chart_id = chart['id']
                config = chart['config']
                log = config.get('log',False)
                chart_text = chart['text']
                chart_type = chart['type']
                stoptime = datetime.datetime.now()
                stop_uuid = self.getchartpath(chart_id)
                model_name = 'Omdata_' + self.table_uuid
                model = getModel('omformmodel', model_name)
                model.objects.filter(id=self.data_id).update(running=False,stop_uuid=stop_uuid,stop_chart_text=chart_text,stoptime=stoptime)
                self.inputLog(log, chart_id, self.next_chart_item['id'], chart_text, chart_type)
                return self.replaceFromTo()
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(並行點)，請通知系統管理員。<br>') + e.__str__())
    
    
    def collectionPoint(self,flag):
        '''
        集合功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                #log output
                chart = self.last_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                log = chart['config'].get('log','')
                self.outputLog(log, chart_id, '')
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                #set ticket history
                stoptime = datetime.datetime.now()
                chart = self.next_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                stop_uuid = self.getchartpath(chart_id)
                model_name = 'Omdata_' + self.table_uuid
                omdata_model = getModel('omformmodel', model_name)
                omdata_model.objects.filter(id=self.data_id).update(running=False,history=True,stop_uuid=stop_uuid,stop_chart_text=chart_text,stoptime=stoptime)
                #取得flow design確認非同步作業是否都已經完成
                config = chart['config']
                main_chart_id = config['main']
                count = len(config['rules'])
                #取得回來的參數與數量
                minor_flow_value_list = []
                return_flow_list = list(omdata_model.objects.filterformat(data_no=self.data_no,history=True,stop_uuid=stop_uuid,error=False,running=False))
                flow_list = []
                collection_uuid = self.data.get('collection_uuid','n')
                for flow_dict in return_flow_list:
                    data_param = json.loads(flow_dict['data_param'])
                    if data_param.get('collection_uuid','') == collection_uuid:
                        flow_list.append(flow_dict)
                return_num = len(flow_list)
                if return_num == count:
                    for flow_dict in flow_list:
                        data_param = json.loads(flow_dict['data_param'])
                        if data_param['chart_id_from'] == main_chart_id:
                            self.data = data_param
                            self.flow_value = self.data['flow_value']
                            main_flow_dict = flow_dict
                        else:
                            minor_flow_value_list.append(data_param['flow_value'])
                    #merge all flow value
                    for minor_flow in minor_flow_value_list:
                        for field in minor_flow:
                            if self.flow_value.get(field,''):
                                pass
                            else:
                                self.flow_value[field] = minor_flow[field]
                    self.data.pop('collection_uuid')
                    #組合新的主線流程，並建立資料
                    main_flow_dict.pop('id')
                    main_flow_dict.pop('stop_uuid')
                    main_flow_dict.pop('stop_chart_text')
                    main_flow_dict['running'] = True
                    main_flow_dict['data_param'] = self.data
                    m = omdata_model.objects.create(**main_flow_dict)
                    self.data_id = m.id
                    self.data['data_id'] = m.id
                    #log input
                    log = config.get('log',False)
                    self.inputLog(log, chart_id, self.flow_value, chart_text, chart_type)
                    return self.replaceFromTo()
                else:
                    try:
                        #remove queue db
                        last_chart_id = self.data.get('chart_id_from','')
                        ex_queue_id = self.flow_uuid + str(self.data_id) + last_chart_id
                        QueueData.objects.get(queue_id=ex_queue_id).delete()
                    except:
                        pass
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(集合點)，請通知系統管理員。<br>') + e.__str__())
    
    
    def switchPoint(self,flag):
        '''
        判斷功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                chart_id = chart['id']
                config = chart['config']
                log = config.get('log',False)
                chart_text = chart['text']
                if self.next_chart_item:
                    next_chart_id = self.next_chart_item['id']
                else:
                    next_chart_id = ''
                self.outputLog(log, chart_id, next_chart_id)
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                chart = self.next_chart_item
                chart_id = chart['id']
                config = chart['config']
                log = config.get('log',False)
                chart_text = chart['text']
                chart_type = chart['type']
                input_obj = {}
                rules_list = config['rules']
                calculate_temp_dict = {}
                if len(rules_list):
                    #calculate
                    formdata = {}
                    calculate_list = config.get('calculate','')
                    if calculate_list:
                        calculate_temp_dict = self.calculate(calculate_list, formdata)
                    #get rule
                    for switch_rule in rules_list:
                        value1 = switch_rule['value1']
                        value2 = switch_rule['value2']
                        if '$' in value1:
                            value1 = value1[2:-1]
                            if calculate_temp_dict.get(value1,None) == None:
                                input_obj[value1] = self.flow_value.get(value1,'')
                            else:
                                input_obj[value1] = calculate_temp_dict.get(value1,'')
                        elif '#' in value1:
                            if not formdata:
                                omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                                formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                            c_input_value = self.regexInOutputValue(formdata, value1)
                            if re.match(r'#[A-Z][0-9]+\(.+\)', value1):
                                value1 = re.findall(r'#[A-Z][0-9]+\((.+)\)', value1)[0]
                            elif re.match(r'#\(.+\)', value1):
                                value1 = re.findall(r'#\((.+)\)', value1)[0]
                            input_obj[value1] = c_input_value
                        elif value1 == None:
                            pass
                        else:
                            input_obj[value1] = value1
                        if '$' in value2:
                            value2 = value2[2:-1]
                            if calculate_temp_dict.get(value1,None) == None:
                                input_obj[value2] = self.flow_value.get(value2,'')
                            else:
                                input_obj[value2] = calculate_temp_dict.get(value2,'')
                        elif '#' in value2:
                            if not formdata:
                                omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                                formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                            c_input_value = self.regexInOutputValue(formdata, value2)
                            if re.match(r'#[A-Z][0-9]+\(.+\)', value2):
                                value2 = re.findall(r'#[A-Z][0-9]+\((.+)\)', value2)[0]
                            elif re.match(r'#\(.+\)', value2):
                                value2 = re.findall(r'#\((.+)\)', value2)[0]
                            input_obj[value2] = c_input_value
                self.data['chart_input'] = input_obj
                if self.last_chart_item:
                    last_chart_id = self.last_chart_item['id']
                else:
                    last_chart_id = ''
                self.inputLog(log, chart_id, last_chart_id, chart_text, chart_type)
                return self.replaceFromTo()
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(判斷點)，請通知系統管理員。<br>') + e.__str__())
    
    
    def subflowPoint(self,flag):
        '''
        子流程功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                in_output = self.data['chart_input']
                chart_id = chart['id']
                chart_text = chart['text']
                config = chart['config']
                #log output
                log = config.get('log','')
                output_obj = {}
                subflow_output_list = config.get('subflow_output','')
                if subflow_output_list:
                    #get last chart's output
                    for subflow_output in subflow_output_list:
                        name = subflow_output['name'][2:-1] #flow_value變數名稱
                        value = subflow_output['value'] #chart變數名稱
                        #回寫flow_value
                        self.flow_value[name] = in_output[value]
                        #組裝寫入value history db的變數
                        output_obj[name] = in_output[value]
                    self.outputLog(log, chart_id, output_obj)
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                input_obj = {}
                #log input
                chart = self.next_chart_item
                subflow_input_list = chart['config']['subflow_input']
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                formdata = {}
                require_list = []
                #get chart's input
                for subflow_input in subflow_input_list:
                    value = subflow_input['value']
                    name = subflow_input['name']
                    require = subflow_input['require']
                    #確認name是要取得table還是flow value還是本身
                    if value == None or not value:
                        input_obj[name] = ''
                    elif '$' in value:
                        input_obj[name] = self.flow_value.get(value[2:-1],'')
                    elif '#' in value:
                        if not formdata:
                            omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                            formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                        input_obj[name] = self.regexInOutputValue(formdata, value)
                    else:
                        input_obj[name] = value
                    #確認是否為必填欄位
                    if require == True or require == 'true' or require == 'True':
                        require_list.append(name)
                #檢查必填
                require_check = self.inputRequireCheck(require_list, input_obj)
                if require_check == None:
                    self.data['chart_input'] = input_obj
                    log = chart['config'].get('log',False)
                    self.inputLog(log, chart_id, input_obj, chart_text, chart_type)
                    return self.replaceFromTo()
                else:
                    return self.markError(chart_id,chart_text,_('缺少必填變數：' + require_check))
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(子流程點)，請通知系統管理員。<br>') + e.__str__())
    
    
    def outflowPoint(self,flag):
        '''
        外部流程功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                self.data.pop('outflow_done')
                in_output = self.data['chart_input']
                chart_id = chart['id']
                chart_text = chart['text']
                config = chart['config']
                #log output
                log = config.get('log','')
                output_obj = {}
                subflow_output_list = config.get('subflow_output','')
                if subflow_output_list:
                    #get last chart's output
                    for subflow_output in subflow_output_list:
                        name = subflow_output['name'][2:-1] #flow_value變數名稱
                        value = subflow_output['value'][2:-1] #chart變數名稱
                        #回寫flow_value
                        self.flow_value[name] = in_output[value]
                        #組裝寫入value history db的變數
                        output_obj[name] = in_output[value]
                    #把外部流程的單號跟流程編號拋放入output log
                    output_obj['outflow_uuid'] = in_output['outflow_uuid']
                    output_obj['outflow_data_no'] = in_output['outflow_data_no']
                    self.outputLog(log, chart_id, output_obj)
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                #function variable
                chart = self.next_chart_item
                config = chart['config']
                outside_flow_uuid = config.get('flow_uuid','')
                subflow_input_list = config['subflow_input']
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                outflow_done = self.data.get('outflow_done',False)
                start_input_dict = {}
                form_input_dict = {}
                both_input_dict = {}
                if not outside_flow_uuid:
                    self.inputLog(log, chart_id, '', chart_text, chart_type)
                    return self.replaceFromTo()
                elif outflow_done:
                    return self.replaceFromTo()
                else:
                    formdata = {}
                    require_list = []
                    #get chart's input
                    for subflow_input in subflow_input_list:
                        value = subflow_input['value']
                        name = subflow_input['name'][2:-1]
                        require = subflow_input['require']
                        if '$' in subflow_input['name']:
                            input_obj = start_input_dict
                        else:
                            input_obj = form_input_dict
                        #確認name是要取得table還是flow value還是本身
                        if value == None:
                            input_value = ''
                        elif '$' in value:
                            input_value = self.flow_value.get(value[2:-1],'')
                        elif '#' in value:
                            if not formdata:
                                omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                                formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                            input_value = self.regexInOutputValue(formdata, value)
                        else:
                            input_value = value
                        #確認name格式
                        if re.match(r'#[A-Z][0-9]+\(.+\)', name):
                            num = int(re.findall(r'#[A-Z]([0-9]+)\(.+\)', name)[0])
                            name = re.findall(r'#[A-Z][0-9]+\((.+)\)', name)[0]
                            l_index = num - 1
                            l = input_obj.get(name,[])
                            for i in range(l_index):
                                if len(l)-i:
                                    pass
                                else:
                                    l.append('')
                            l.append(input_value)
                            input_obj[name] = l
                            both_input_dict[name] = l
                        elif re.match(r'#\(.+\)', name):
                            name = re.findall(r'#\((.+)\)', name)[0]
                            input_obj[name] = input_value
                            both_input_dict[name] = input_value
                        else:
                            input_obj[name] = input_value
                            both_input_dict[name] = input_value
                        #確認是否為必填欄位
                        if require == True or require == 'true' or require == 'True':
                            require_list.append(name)
                    #檢查必填
                    require_check = self.inputRequireCheck(require_list, both_input_dict)
                    if require_check == None:
                        log = chart['config'].get('log',False)
                        self.inputLog(log, chart_id, both_input_dict, chart_text, chart_type)
                        data_str = json.dumps(self.data)
                        outflow_content = json.loads(data_str)
                        outflow_content['chart_id_from'] = None
                        #組合外部流程的必要參數並呼叫開單
                        outside_flow_formobject = json.loads(FlowActiveGlobalObject.UUIDSearch(outside_flow_uuid).formobject).get('items',[])
                        from omformflow.views import createOmData
                        start_input = json.dumps(start_input_dict)
                        formdata_list = []
                        if form_input_dict:
                            for item in outside_flow_formobject:
                                if item['id'][:8] == 'FORMITM_':
                                    FormatToFormdataList(item, form_input_dict[item['id']], formdata_list)
                        formdata_list = json.dumps(formdata_list)
                        param = {'flow_uuid':outside_flow_uuid,'formdata':formdata_list,'start_input':start_input,'outflow_content':json.dumps(outflow_content)}
                        createomdata_result = createOmData(param)
                        if not createomdata_result['status']:
                            return self.markError(chart_id, chart_text, createomdata_result['message'])
                    else:
                        return self.markError(chart_id,chart_text,_('缺少必填變數：' + require_check))
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(外部流程點)，請通知系統管理員。<br>') + e.__str__())
        
        
    def inflowPoint(self,flag):
        '''
        呼叫流程功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                self.data.pop('outflow_done')
                in_output = self.data['chart_input']
                chart_id = chart['id']
                chart_text = chart['text']
                config = chart['config']
                #log output
                log = config.get('log','')
                output_obj = {}
                subflow_output_list = config.get('subflow_output','')
                if subflow_output_list:
                    #get last chart's output
                    for subflow_output in subflow_output_list:
                        name = subflow_output['name'][2:-1] #flow_value變數名稱
                        value = subflow_output['value'][2:-1] #chart變數名稱
                        #回寫flow_value
                        self.flow_value[name] = in_output[value]
                        #組裝寫入value history db的變數
                        output_obj[name] = in_output[value]
                    #把外部流程的單號跟流程編號拋放入output log
                    output_obj['outflow_uuid'] = in_output['outflow_uuid']
                    output_obj['outflow_data_no'] = in_output['outflow_data_no']
                    self.outputLog(log, chart_id, output_obj)
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                #function variable
                chart = self.next_chart_item
                config = chart['config']
                subflow_input_list = config['subflow_input']
                outside_flow_name = config.get('flow_name','')
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                outflow_done = self.data.get('outflow_done',False)
                start_input_dict = {}
                form_input_dict = {}
                both_input_dict = {}
                if not outside_flow_name:
                    self.inputLog(log, chart_id, '', chart_text, chart_type)
                    return self.replaceFromTo()
                elif outflow_done:
                    return self.replaceFromTo()
                else:
                    formdata = {}
                    require_list = []
                    #get chart's input
                    for subflow_input in subflow_input_list:
                        value = subflow_input['value']
                        name = subflow_input['name'][2:-1]
                        require = subflow_input['require']
                        if '$' in subflow_input['name']:
                            input_obj = start_input_dict
                        else:
                            input_obj = form_input_dict
                        #確認name是要取得table還是flow value還是本身
                        if value == None or not value:
                            input_value = ''
                        elif '$' in value:
                            input_value = self.flow_value.get(value[2:-1],'')
                        elif '#' in value:
                            if not formdata:
                                omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                                formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                            input_value = self.regexInOutputValue(formdata, value)
                        else:
                            input_value = value
                        #確認name格式
                        if re.match(r'#[A-Z][0-9]+\(.+\)', name):
                            num = int(re.findall(r'#[A-Z]([0-9]+)\(.+\)', name)[0])
                            name = re.findall(r'#[A-Z][0-9]+\((.+)\)', name)[0]
                            l_index = num - 1
                            l = input_obj.get(name,[])
                            for i in range(l_index):
                                if len(l)-i:
                                    pass
                                else:
                                    l.append('')
                            l.append(input_value)
                            input_obj[name] = l
                            both_input_dict[name] = l
                        elif re.match(r'#\(.+\)', name):
                            name = re.findall(r'#\((.+)\)', name)[0]
                            input_obj[name] = input_value
                            both_input_dict[name] = input_value
                        else:
                            input_obj[name] = input_value
                            both_input_dict[name] = input_value
                        #確認是否為必填欄位
                        if require == True or require == 'true' or require == 'True':
                            require_list.append(name)
                    #檢查必填
                    require_check = self.inputRequireCheck(require_list, both_input_dict)
                    if require_check == None:
                        log = chart['config'].get('log',False)
                        self.inputLog(log, chart_id, both_input_dict, chart_text, chart_type)
                        data_str = json.dumps(self.data)
                        outflow_content = json.loads(data_str)
                        outflow_content['chart_id_from'] = None
                        #組合外部流程的必要參數並呼叫開單
                        try:
                            outside_flow_fa = FlowActiveGlobalObject.NameSearch(outside_flow_name, self.app_id, None)
                        except:
                            self.markError(chart_id, chart_text, _('應用內找不到此流程：' + outside_flow_name))
                        outside_flow_uuid = outside_flow_fa.flow_uuid.hex
                        outside_flow_formobject = json.loads(outside_flow_fa.formobject).get('items',[])
                        from omformflow.views import createOmData
                        start_input = json.dumps(start_input_dict)
                        formdata_list = []
                        if form_input_dict:
                            for item in outside_flow_formobject:
                                if item['id'][:8] == 'FORMITM_':
                                    FormatToFormdataList(item, form_input_dict[item['id']], formdata_list)
                        formdata_list = json.dumps(formdata_list)
                        param = {'flow_uuid':outside_flow_uuid,'formdata':formdata_list,'start_input':start_input,'outflow_content':json.dumps(outflow_content)}
                        createomdata_result = createOmData(param)
                        if not createomdata_result['status']:
                            return self.markError(chart_id, chart_text, createomdata_result['message'])
                    else:
                        return self.markError(chart_id,chart_text,_('缺少必填變數：' + require_check))
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(呼叫流程點)，請通知系統管理員。<br>') + e.__str__())
    
    
    def sleepPoint(self,flag):
        '''
        暫停功能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                log = chart['config'].get('log','')
                #log output
                self.outputLog(log, chart_id, '')
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                chart = self.next_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                config = chart['config']
                if self.last_chart_item:
                    sleep_value = config.get('value','')
                    if sleep_value:
                        sleep_time = int(self.flow_value.get(sleep_value[2:-1]))
                    else:
                        sleep_time = int(config['msec'])
                    input_param = {}
                    module_name = 'omformflow.views'
                    method_name = 'pushSleepPoint'
                    data_str = json.dumps(self.data)
                    param = json.loads(data_str)
                    exec_time = datetime.datetime.now() + datetime.timedelta(milliseconds=sleep_time)
                    every = '1'
                    cycle = 'Once'
                    cycle_date = '[]'
                    exec_fun = {'module_name':'omflow.syscom.schedule_monitor','method_name':'put_flow_job'}
                    input_param['module_name'] = module_name
                    input_param['method_name'] = method_name
                    input_param['flow_uuid'] = self.table_uuid
                    input_param['formdata'] = param
                    exec_fun_dict = json.dumps(exec_fun)
                    input_param_dict = json.dumps(input_param)
                    scheduler = Scheduler.objects.create(exec_time=exec_time,every=every,cycle=cycle,cycle_date=cycle_date,exec_fun=exec_fun_dict,input_param=input_param_dict,flowactive_id=None)
                    schedule_Execute(scheduler)
                    #remove last queue db
                    try:
                        last_chart_id = self.data.get('chart_id_from','')
                        ex_queue_id = self.flow_uuid + str(self.data_id) + str(last_chart_id)
                        QueueData.objects.get(queue_id=ex_queue_id).delete()
                    except:
                        pass
                else:
                    #log input
                    log = config.get('log',False)
                    self.inputLog(log, chart_id, '', chart_text, chart_type)
                    return self.replaceFromTo()
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(暫停點)，請通知系統管理員。<br>') + e.__str__())
        
    
    def setformPoint(self,flag):
        '''
        自動輸入空能點
        '''
        chart_id = ''
        chart_text = ''
        try:
            if flag == 'from':
                chart = self.last_chart_item
                chart_id = chart['id']
                chart_text = chart['text']
                config = chart['config']
                log = config.get('log',False)
                config_output_list = config['output']
                model = getModel('omformmodel', 'Omdata_' + self.table_uuid)
                table_dict = model.objects.getdictformat(id=self.data_id)
                output_dict = {}
                for config_output in config_output_list:
                    name = config_output['name'][2:-1]  #flow_value變數
                    value = config_output['value']  #欄位
                    c_output_value = self.regexInOutputValue(table_dict, value)
                    #寫入flow value
                    self.flow_value[name] = c_output_value
                    #寫入output dict
                    output_dict[name] = c_output_value
                #log output
                self.outputLog(log, chart_id, output_dict)
                return self.checkError(chart_id,chart_text)
            elif flag == 'to':
                chart = self.next_chart_item
                config = chart['config']
                log = chart.get('log',False)
                chart_id = chart['id']
                chart_text = chart['text']
                chart_type = chart['type']
                write_from_dict = {}
                #calculate
                formdata = {}
                calculate_list = config.get('calculate','')
                calculate_temp_dict = {}
                if calculate_list:
                    calculate_temp_dict = self.calculate(calculate_list, formdata)
                #欄位設定
                require_list = []
                temp_dict = {} 
                config_input_list = config['input']
                for config_input in config_input_list:
                    name = config_input['name'] #欄位名稱
                    value = config_input['value'] #變數/值
                    #確認value是要取得flow value還是本身
                    if value == None or not value:
                        c_input_value = ''
                    elif '$' in value:
                        value = value[2:-1]
                        if calculate_temp_dict.get(value,None) == None:
                            c_input_value = self.flow_value[value]
                        else:
                            c_input_value = calculate_temp_dict[value]
                    else:
                        c_input_value = value
                    #放入暫存dict
                    if re.match(r'#[A-Z][0-9]+\(.+\)', name):
                        num = int(re.findall(r'#[A-Z]([0-9]+)\(.+\)', name)[0])
                        name = re.findall(r'#[A-Z][0-9]+\((.+)\)', name)[0]
                        l_index = num - 1
                        l = temp_dict.get(name,[])
                        for i in range(l_index):
                            if len(l)-i:
                                pass
                            else:
                                l.append('')
                        l.append(c_input_value)
                        temp_dict[name] = l
                    elif re.match(r'#\(.+\)', name):
                        name = re.findall(r'#\((.+)\)', name)[0]
                        temp_dict[name] = c_input_value
                    else:
                        temp_dict[name] = c_input_value
                    #確認該欄位是否為必填
                    require = config_input['require']
                    if require == True or require == 'true' or require == 'True':
                        require_list.append(name.lower())
                #組成寫回資料庫的dict
                formobject_items = self.flowobject['form_object']['items']
                formdata_list = []
                for key in temp_dict:
                    name = key
                    value = temp_dict[key]
                    for item in formobject_items:
                        if item['id'] == name:
                            FormatToFormdataList(item, c_input_value, formdata_list)
                            break
                if formdata_list:
                    for item in formdata_list:
                        item_id = item['id'].lower()
                        value = item['value']
                        if isinstance(value, dict):
                            new_value = json.dumps(value)
                        elif isinstance(value, list):
                            new_value = json.dumps(value)
                        elif isinstance(value, str):
                            new_value = value
                        elif value == None:
                            new_value = ''
                        else:
                            new_value = str(value)
                        write_from_dict[item_id] = new_value
                #檢查必填欄位
                require_check = self.inputRequireCheck(require_list, write_from_dict)
                if require_check == None:
                    model_name = 'Omdata_' + self.table_uuid
                    model = getModel('omformmodel', model_name)
                    model.objects.filter(id=self.data_id).update(**write_from_dict)
                    self.inputLog(log, chart_id, write_from_dict, chart_text, chart_type)
                    return self.replaceFromTo()
                else:
                    return self.markError(chart_id,chart_text,_('缺少必填變數：' + require_check))
        except Exception as e:
            self.markError(chart_id, chart_text, _('OME系統錯誤(自動輸入點)，請通知系統管理員。<br>') + e.__str__())
        
            
    
    def has_preflow(self,chart):
        '''
        檢查是否有資料驗證
        '''
        try:
            status = 'N'
            value = ''
            #check this flow has pre flow or not
            preflow_uid = chart['config'].get('subflow_id','')
            if preflow_uid and preflow_uid != 0 and preflow_uid != '0':
                preflow_done = self.data.get('preflow_done',None)
                #尚未執行資料驗證
                if preflow_done == None:
                    status = 'Y'
                    value = FlowActiveGlobalObject.UIDSearch(preflow_uid, self.flow_uuid).flow_uuid.hex
                #已執行資料驗證且驗證成功
                elif preflow_done == True:
                    pass
                #已執行資料驗證但驗證失敗
                elif preflow_done == False:
                    self.data.pop('preflow_done')
                    status = 'F'
                    value = _('預處理失敗。')
        except:
            status = 'E'
            value = _('找不到預處理流程。')
        finally:
            result = {}
            result['status'] = status
            result['value'] = value
            return result
    
    
    def outputLog(self,log,chart_id,output_value):
        '''
        紀錄上一個點的輸出
        '''
        if self.flowlog and self.table_uuid and log and self.data_id:
            try:
                #get model
                valuehistory_model = getModel('omformmodel', 'Omdata_' + self.table_uuid + '_ValueHistory')
                #log output
                if isinstance(output_value, dict) or isinstance(output_value, list):
                    output_data = json.dumps(output_value)
                else:
                    output_data = output_value
                stop_uuid = self.getchartpath(chart_id)
                valuehistory = valuehistory_model.objects.get(flow_uuid=self.flow_uuid,data_no=self.data_no,data_id=self.data_id,chart_id=stop_uuid)
                valuehistory.error=self.data.get('error',False)
                valuehistory.output_data = output_data
                valuehistory.save()
            except Exception as e:
                debug('OME Output Log error:     %s' % e.__str__())
    
    
    def differentiateNextType(self):
        '''
        確認下一個點的類型
        '''
        flag = 'to'
        if self.next_chart_item:
            chart_type = self.next_chart_item.get('type','')
            if chart_type == 'start':
                return self.startPoint(flag)
            elif chart_type == 'end':
                return self.endPoint(flag)
            elif chart_type == 'python':
                return self.pythonPoint(flag)
            elif chart_type == 'async':
                return self.asyncPoint(flag)
            elif chart_type == 'form':
                return self.formPoint(flag)
            elif chart_type == 'collection':
                return self.collectionPoint(flag)
            elif chart_type == 'subflow':
                return self.subflowPoint(flag)
            elif chart_type == 'outflow':
                return self.outflowPoint(flag)
            elif chart_type == 'switch':
                return self.switchPoint(flag)
            elif chart_type == 'sleep':
                return self.sleepPoint(flag)
            elif chart_type == 'setform':
                return self.setformPoint(flag)
            elif chart_type == 'inflow':
                return self.inflowPoint(flag)
        else:
            return self.closeTicket()
    
    
    def inputLog(self,log,chart_id,input_value,chart_text,chart_type):
        '''
        紀錄下一個點的輸入
        '''
        if self.flowlog and self.table_uuid and log and self.data_id:
            try:
                #get model
                valuehistory_model = getModel('omformmodel', 'Omdata_' + self.table_uuid + '_ValueHistory')
                #log input
                if isinstance(input_value, dict) or isinstance(input_value, list):
                    input_data = json.dumps(input_value)
                else:
                    input_data = input_value
                stop_uuid = self.getchartpath(chart_id)
                valuehistory_model.objects.create(flow_uuid=self.flow_uuid,data_no=self.data_no,data_id=self.data_id,chart_id=stop_uuid,stop_chart_text=chart_text,stop_chart_type=chart_type,input_data=input_data)
            except Exception as e:
                debug('OME Input Log error:     %s' % e.__str__())
        
    
    def calculate(self, calculate_list, formdata):
        '''
        篩選功能
        '''
        def getVariable(flow_value, temp_dict_for_calculate, c_row, formdata):
            #function variable
            var_dict = {}
            for f in c_row:
                if f in ['from','para1','para2']:
                    if c_row[f] == None:
                        var_dict[f] = ''
                    elif '$' in c_row[f]:
                        if temp_dict_for_calculate.get(c_row[f][2:-1],''):
                            var_dict[f] = temp_dict_for_calculate.get(c_row[f][2:-1],'')
                        else:
                            var_dict[f] = flow_value.get(c_row[f][2:-1],'')
                    elif '#' in c_row[f]:
                        var_dict[f] = self.regexInOutputValue(formdata, c_row[f])
                    else:
                        var_dict[f] = c_row[f]
                elif f == 'to':
                    var_dict[f] = c_row[f][2:-1]
            return var_dict
        
        #function variable
        result = {}
        try:
            if len(calculate_list):
                if not formdata:
                    omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                    formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                for c_row in calculate_list:
                    c_type = c_row['type']
                    var_dict = getVariable(self.flow_value, result, c_row, formdata)
#                     if c_type == 'number':
#                         try:
#                             result[var_dict['to']] = int(var_dict['from'])
#                         except:
#                             result[var_dict['to']] = ''
                    if c_type == 'string':
                        try:
                            result[var_dict['to']] = str(var_dict['from'])
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'upper':
                        try:
                            result[var_dict['to']] = var_dict['from'].upper()
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'lower':
                        try:
                            result[var_dict['to']] = var_dict['from'].lower()
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'replace':
                        try:
                            para1 = r'%s' % var_dict['para1']
                            regex = re.sub(para1, var_dict['para2'], var_dict['from'])
                            result[var_dict['to']] = regex
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'len':
                        try:
                            result[var_dict['to']] = str(len(var_dict['from']))
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'strip':
                        try:
                            result[var_dict['to']] = var_dict['from'].strip()
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'startwith':
                        try:
                            para1 = int(var_dict['para1'])
                            result[var_dict['to']] = var_dict['from'][:para1]
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'endof':
                        try:
                            para1 = -int(var_dict['para1'])
                            result[var_dict['to']] = var_dict['from'][para1:]
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'substring':
                        try:
                            para1 = int(var_dict['para1']) - 1
                            para2 = para1 + int(var_dict['para2'])
                            result[var_dict['to']] = var_dict['from'][para1:para2]
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'add':
                        try:
                            result[var_dict['to']] = var_dict['from'] +  var_dict['para1']
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'num+':
                        try:
                            result[var_dict['to']] = str(float(var_dict['from']) + float(var_dict['para1']))
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'num-':
                        try:
                            result[var_dict['to']] = str(float(var_dict['from']) - float(var_dict['para1']))
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'num*':
                        try:
                            result[var_dict['to']] = str(float(var_dict['from']) * float(var_dict['para1']))
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'num/':
                        try:
                            result[var_dict['to']] = str(float(var_dict['from']) / float(var_dict['para1']))
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'num_mod':
                        try:
                            result[var_dict['to']] = str(float(var_dict['from']) % float(var_dict['para1']))
                        except:
                            result[var_dict['to']] = ''
                    elif c_type == 'write':
                        try:
                            self.flow_value[var_dict['to']] = str(var_dict['from'])
                        except:
                            result[var_dict['to']] = ''
        except:
            result = {}
        finally:
            return result
    
    
    def updateFlowValue(self, chart_id, chart_text):
        '''
        更新資料庫的data_param
        '''
        try:
            if self.data_id:
                #get omdata and update omdata
                model_name = 'Omdata_' + self.table_uuid
                model = getModel('omformmodel', model_name)
                data_dumps = json.dumps(self.data)
                model.objects.filter(id=self.data_id).update(data_param=data_dumps)
            return self.differentiateNextType()
        except:
            self.markError(chart_id, chart_text, _('更新流程變數失敗。'))
            return False
    
    
    def checkError(self,chart_id,chart_text):
        '''
        檢查上一個點是否錯誤
        '''
        if self.data.get('error',False) and (not self.error_pass):
            error_message = self.data.get('error_message','')
            return self.markError(chart_id,chart_text,error_message)
        else:
            return self.updateFlowValue(chart_id,chart_text)
    
    
    def markError(self,chart_id,stop_chart_text,error_message,create_mission=False):
        '''
        當錯誤發生時，將該筆資料標記為錯誤
        '''
        try:
            #remove queue db
            ex_queue_id = self.flow_uuid + str(self.data_id) + chart_id
            QueueData.objects.get(queue_id=ex_queue_id).delete()
        except:
            pass
        try:
            if self.data_id:
                stop_uuid = self.getchartpath(chart_id)
                stoptime = datetime.datetime.now()
                model_name = 'Omdata_' + self.table_uuid
                model = getModel('omformmodel', model_name)
                omdata = model.objects.get(id=self.data_id)
                omdata.stop_uuid = stop_uuid
                omdata.stop_chart_text = stop_chart_text
                omdata.stoptime = stoptime
                omdata.running = False
                omdata.error = True
                omdata.history = True
                omdata.error_message = error_message
                omdata.save()
                omdata_dict = omdata.__dict__
                omdata_dict.pop('_state')
                omdata_dict.pop('id')
                omdata_dict.pop('history')
                m = model.objects.create(**omdata_dict)
                if create_mission:
                    pass
                    #create mymission
                    mission_param = {}
                    mission_param['flow_uuid'] = m.flow_uuid
                    mission_param['flow_name'] = model.table_name
                    mission_param['status'] = m.status
                    mission_param['level'] = m.level
                    mission_param['title'] = m.title
                    mission_param['data_no'] = m.data_no
                    mission_param['data_id'] = m.id
                    mission_param['stop_uuid'] = stop_uuid
                    mission_param['stop_chart_text'] = stop_chart_text
                    mission_param['create_user_id'] = m.create_user_id
                    mission_param['ticket_createtime'] = m.init_data.createtime
                    mission_param['action'] = self.action
                    group = json.loads(m.group)
                    mission_param['assignee_id'] = group['user']
                    mission_param['assign_group_id'] = group['group']
                    createMission(mission_param)
        except Exception as e:
            debug('OME MarkError error:     %s' % e.__str__())
    
    
    def getchartpath(self,chart_id):
        '''
        取得階層式流程架構的路徑
        '''
        def getparentpath(data):
            chart_id_from = content.get('chart_id_from','')
            g_content = data.get('content','')
            g_preflow_content = data.get('preflow_content','')
            if g_content:
                g_parent = g_content
            elif g_preflow_content:
                g_parent = g_preflow_content
            else:
                g_parent = False
            if g_parent:
                return getparentpath(g_parent) + '-' + chart_id_from
            else:
                return chart_id_from
        content = self.data.get('content','')
        preflow_content = self.data.get('preflow_content','')
        if content:
            parent = content
        elif preflow_content:
            parent = preflow_content
        else:
            parent = False
        if parent:
            chart_path = getparentpath(parent) + '-' + chart_id
        else:
            chart_path = chart_id
        return chart_path
    
    
    def inputProcess(self,log):
        '''
        組合下一個點的輸入、檢查輸入是否必填，並進行log
        '''
        #function variable
        chart = self.next_chart_item
        chart_id = chart['id']
        chart_text = chart['text']
        chart_type = chart['type']
        config = chart['config']
        input_obj = {}
        config_input_list = config['input']
        calculate_temp_dict = {}
        require_list = []
        formdata = self.data.get('formdata','')
        #get next chart's input
        if len(config_input_list):
            #calculate
            calculate_list = config.get('calculate','')
            if calculate_list:
                calculate_temp_dict = self.calculate(calculate_list, formdata)
            for config_input in config_input_list:
                name = config_input['name'] #變數名稱
                value = config_input['value'] #變數/欄位/值
                #確認name是要取得table還是flow value還是本身
                if value == None or not value:
                    c_input_value = ''
                elif '$' in value:
                    value = value[2:-1]
                    if calculate_temp_dict.get(value,None) == None:
                        c_input_value = self.flow_value[value]
                    else:
                        c_input_value = calculate_temp_dict[value]
                elif '#' in value:
                    if not formdata:
                        omdata_model = getModel('omformmodel','Omdata_' + self.table_uuid)
                        formdata = list(omdata_model.objects.filterformat(id=self.data_id))[0]
                    c_input_value = self.regexInOutputValue(formdata, value)
                else:
                    c_input_value = value
                #確認該欄位是否為必填
                require = config_input['require']
                if require == True or require == 'true' or require == 'True':
                    require_list.append(name)
                #組裝寫入value history db的變數
                input_obj[name] = c_input_value
        #檢查必填欄位
        require_check = self.inputRequireCheck(require_list, input_obj)
        if require_check == None:
            self.inputLog(log, chart_id, input_obj, chart_text, chart_type)
            #put input_obj into data
            self.data['chart_input'] = input_obj
            #put queue
            return self.replaceFromTo()
        else:
            return self.markError(chart_id,chart_text,_('缺少必填變數：'+ require_check))
        
    
    def inputRequireCheck(self, require_list, input_obj):
        '''
        檢查必填欄位使否為空
        '''
        require_check = None
        if len(require_list):
            for name in require_list:
                if input_obj[name]:
                    pass
                else:
                    require_check = name
                    break
        return require_check
    
    
    def replaceFromTo(self):
        '''
        修改id_from以及id_to
        '''
        last_chart_id = self.data.get('chart_id_from','')
        chart_id = self.data.get('chart_id_to','')
        self.data['chart_id_from'] = chart_id
        self.data['chart_id_to'] = ''
        return self.do(chart_id,last_chart_id)
    
    
    def do(self,chart_id,last_chart_id):
        '''
        put data in queue.
        '''
        chart = self.next_chart_item
        config = chart['config']
        chart_type = chart['type']
        content = self.data.get('content','')
        preflow_content = self.data.get('preflow_content','')
        outflow_content = self.data.get('outflow_content','')
        load_balance = config.get('load_balance',False)
        if load_balance:
            self.doLoadBalance()
        else:
            module_name = 'omformflow.production.' + self.flow_uuid +'.' + str(self.version) + '.main'
            method_name = 'main'
            name = 'FormFlow'
            input_param = json.dumps(self.data)
            queue_id = self.flow_uuid + str(self.data_id) + str(chart_id)
            if content and chart_type == 'start':
                parent_flow_uuid = content.get('flow_uuid','')
                parent_data_id = content.get('data_id','')
                parent_chart_id = content.get('chart_id_from','')
                ex_queue_id = parent_flow_uuid + str(parent_data_id) + str(parent_chart_id)
            elif preflow_content and chart_type == 'start':
                parent_flow_uuid = preflow_content.get('flow_uuid','')
                parent_data_id = preflow_content.get('data_id','')
                parent_chart_id = preflow_content.get('chart_id_to','')
                ex_queue_id = parent_flow_uuid + str(parent_data_id) + str(parent_chart_id)
            elif outflow_content and chart_type == 'start':
                parent_flow_uuid = outflow_content.get('flow_uuid','')
                parent_data_id = outflow_content.get('data_id','')
                parent_chart_id = outflow_content.get('chart_id_to','')
                ex_queue_id = parent_flow_uuid + str(parent_data_id) + str(parent_chart_id)
            else:
                ex_queue_id = self.flow_uuid + str(self.data_id) + str(last_chart_id)
            #remove last and write new queue db
            try:
                QueueData.objects.get(queue_id=ex_queue_id).delete()
            except:
                pass
            QueueData.objects.create(queue_id=queue_id,name=name,input_param=input_param,module_name=module_name,method_name=method_name)
            #put queue
            FormFlowMonitor.putQueue(module_name, method_name, self.data)
        
    
    def doLoadBalance(self):
        '''
        分散式運算預留
        '''
        version = getVersion('')
        if version == 0:
            pass
        else:
            pass

    
    def closeTicket(self):
        '''
        無路可走後關單
        '''
        chart_id = self.last_chart_item.get('id','')
        stop_chart_text = self.last_chart_item.get('text','')
        stoptime = datetime.datetime.now()
        stop_uuid = self.getchartpath(chart_id)
        #set ticket closed
        model_name = 'Omdata_' + self.table_uuid
        model = getModel('omformmodel', model_name)
        model.objects.filter(id=self.data_id).update(running=False,closed=True,stop_uuid=stop_uuid,stop_chart_text=stop_chart_text,stoptime=stoptime)


    def regexInOutputValue(self, formdata, value):
        '''
        確認input/output value格式
        '''
        try:
            if re.match(r'#[A-Z][0-9]+\(.+\)', value):
                eng_num = re.findall(r'#([A-Z][0-9]+)\(.+\)', value)[0]
                value = re.findall(r'#[A-Z][0-9]+\((.+)\)', value)[0]
                table_field = value.lower()
                temp_value = json.loads(formdata.get(table_field,'{}'))
                c_input_value = self.getTableFieldValue(eng_num,temp_value)
            elif re.match(r'#\(.+\)', value):
                value = re.findall(r'#\((.+)\)', value)[0]
                table_field = value.lower()
                c_input_value = formdata.get(table_field,'')
        except Exception as e:
            debug(e.__str__())
            c_input_value = ''
        finally:
            return c_input_value

    
    def getTableFieldValue(self, eng_num, temp_value):
        '''
        '''
        try:
            if eng_num == 'G1':
                value = temp_value['group']
            elif eng_num == 'G2':
                value = temp_value['user']
        except Exception as e:
            debug(e.__str__())
            value = ''
        finally:
            return value
    
    
    
    
    
    