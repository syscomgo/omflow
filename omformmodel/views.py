import os
from django.core.management import call_command
from django.apps import apps
from django.conf import settings
from django.db import models
from omflow.syscom.customfield import FormatManager
from django.utils.translation import gettext as _
from omflow.syscom.default_logger import debug


class FormModel():
    
    def __init__(self):
        self.file_path = os.path.join(settings.BASE_DIR, "omformmodel", "models.py")
        self.running = False


    def deployModel(self, flow_uuid, flow_name, form_item_counter):
        '''
        input: flow_uuid, form_item_counter
        return: True, False
        author: Kolin Hsu
        '''
        def createModel(file_path, file_content):
            '''
            create new model
            input: file_content
            return: None
            author: Kolin Hsu
            '''
            #function variable
            file_data = ""
            #write model
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "#<new here>" in line:
                        line = line.replace("#<new here>","")
                    file_data += line
            file_data += "\n" + file_content
            with open(file_path,"w",encoding="utf-8") as f:
                f.write(file_data)
        
        def updateModel(file_path,model_name,file_content,form_item_counter):
            '''
            update model
            input: file_content
            return: None
            author: Kolin Hsu
            '''
            #function variable
            file_data = ""
            model_start = "#<" + model_name + " start>"
            get_model_start_line = False
            next_line_is_json = False
            change = True
            file_content = file_content.replace("#<new here>","")
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    #search flow model start line
                    if get_model_start_line:
                        #the model 2nd line is max form_item_count
                        if next_line_is_json:
                            max_item_count = int(line[1:])
                            next_line_is_json = False
                            #if new version's item counter less than max item counter, do nothing
                            if max_item_count >= form_item_counter:
                                change = False
                                break
                            #or set new max item counter to 2nd line
                            else:
                                file_data += "#<" + model_name + " start>\n"
                                line = "#" + str(form_item_counter) + "\n"
                        else:
                            #find max field
                            field = 'formitm_' + str(max_item_count)
                            if field in line:
                                file_data += line
                                while max_item_count < form_item_counter:
                                    max_item_count += 1
                                    file_data += "    " + "formitm_" + str(max_item_count) + " = models.TextField(null=True,blank=True)\n"
                                line = ""
                                get_model_start_line = False
                        file_data += line
                    else:
                        if model_start in line:
                            line = ""
                            get_model_start_line = True
                            next_line_is_json = True
                        file_data += line
            if change:
                #file_data += file_content
                with open(file_path,"w",encoding="utf-8") as f:
                    f.write(file_data)
            return change
        
        def getDefaultModel(model_name, flow_name, form_item_counter, flow_uuid):
            '''
            create default model class
            input: model_name, form_item_counter
            return: file_content
            author: Kolin Hsu
            '''
            file_content = ""
            file_content += "#<" + model_name + " start>\n"
            file_content += "#" + str(form_item_counter) + "\n"
            file_content += "class " + model_name + "(models.Model):\n"
            code_space = "    "
            file_content += code_space + "table_name = _('"+flow_name+"')\n"
            file_content += code_space + "flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)\n"
            file_content += code_space + "dataid_header = models.CharField(verbose_name= _('資料代碼'), max_length=3)\n"
            file_content += code_space + "data_no = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)\n"
            file_content += code_space + "history = models.BooleanField(verbose_name = _('歷史資料'), default=False)\n"
            file_content += code_space + "status = models.CharField(verbose_name= _('狀態'), max_length=20,null=True, blank=True)\n"
            file_content += code_space + "title = models.CharField(verbose_name= _('標題'), max_length=20,null=True, blank=True)\n"
            file_content += code_space + "level = models.CharField(verbose_name= _('燈號'), max_length=20,null=True, blank=True)\n"
            file_content += code_space + "group = models.CharField(verbose_name= _('受派群組'), max_length=20,null=True, blank=True)\n"
            file_content += code_space + "closed = models.BooleanField(verbose_name = _('關閉標記'), default=False)\n"
            file_content += code_space + "stop_uuid = models.TextField(verbose_name = _('關卡'), blank=True, null=True)\n"
            file_content += code_space + "stop_chart_type = models.TextField(verbose_name = _('關卡類型'), blank=True, null=True)\n"
            file_content += code_space + "stop_chart_text = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)\n"
            file_content += code_space + "running = models.BooleanField(verbose_name = _('執行標記'), default=False)\n"
            file_content += code_space + "error = models.BooleanField(verbose_name = _('是否異常'), default=False)\n"
            file_content += code_space + "createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)\n"
            file_content += code_space + "updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)\n"
            file_content += code_space + "stoptime = models.DateTimeField(verbose_name = _('停止時間'), null=True,blank=True)\n"
            file_content += code_space + "create_user = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_"+flow_uuid+"')\n"
            file_content += code_space + "update_user = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_"+flow_uuid+"')\n"
            file_content += code_space + "data_param = models.TextField(verbose_name = _('流程參數'), null=True,blank=True)\n"
            file_content += code_space + "error_message = models.TextField(verbose_name = _('錯誤訊息'), null=True,blank=True)\n"
            file_content += code_space + "init_data = models.ForeignKey('self', blank=True, null=True, related_name='extra_data', verbose_name = _('初始資料'), on_delete=models.CASCADE)\n"
            for i in range(form_item_counter):
                file_content += code_space + "formitm_" + str(i+1) + " = models.TextField(null=True,blank=True)\n"
            file_content += code_space + "objects = FormatManager()\n"
            file_content += code_space + "class Meta:\n"
            code_space += "    "
            file_content += code_space + "default_permissions = ()\n"
            file_content += code_space + "permissions = (\n"
            file_content += code_space + "    ('"+model_name+"_Add', _('新增"+flow_name+"')),\n"
            file_content += code_space + "    ('"+model_name+"_Modify', _('修改"+flow_name+"')),\n"
            file_content += code_space + "    ('"+model_name+"_View', _('檢視"+flow_name+"')),\n"
            file_content += code_space + "    ('"+model_name+"_Delete', _('刪除"+flow_name+"')),\n"
            file_content += code_space + ")\n"
            code_space = code_space.replace("    ", "", 1)
            code_space = code_space.replace("    ", "", 1)
            file_content += code_space + "\n"
            file_content += "class " + model_name + "_ValueHistory(models.Model):\n"
            code_space = "    "
            file_content += code_space + "flow_uuid = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)\n"
            file_content += code_space + "data_no = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)\n"
            file_content += code_space + "data_id = models.IntegerField(verbose_name = _('多重資料編號'), blank=True, null=True)\n"
            file_content += code_space + "chart_id = models.CharField(verbose_name= _('功能點'), max_length=50,null=True, blank=True)\n"
            file_content += code_space + "stop_chart_type = models.TextField(verbose_name = _('關卡類型'), blank=True, null=True)\n"
            file_content += code_space + "stop_chart_text = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)\n"
            file_content += code_space + "input_data = models.TextField(verbose_name= _('輸入參數'),null=True, blank=True)\n"
            file_content += code_space + "output_data = models.TextField(verbose_name= _('輸出參數'),null=True, blank=True)\n"
            file_content += code_space + "createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)\n"
            file_content += code_space + "updatetime = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)\n"
            file_content += code_space + "error = models.BooleanField(verbose_name = _('異常標記'), default=False)\n"
            file_content += code_space + "objects = FormatManager()\n"
            file_content += code_space + "class Meta:\n"
            code_space += "    "
            file_content += code_space + "default_permissions = ()\n"
            code_space = code_space.replace("    ", "", 1)
            code_space = code_space.replace("    ", "", 1)
            file_content += code_space + "\n"
            file_content += "class " + model_name + "_DataNo(models.Model):\n"
            code_space = "    "
            file_content += code_space + "createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)\n"
            file_content += code_space + "objects = FormatManager()\n"
            file_content += code_space + "class Meta:\n"
            code_space += "    "
            file_content += code_space + "default_permissions = ()\n"
            code_space = code_space.replace("    ", "", 1)
            code_space = code_space.replace("    ", "", 1)
            file_content += "#<" + model_name + " end>\n"
            file_content += "#<new here>\n"
            return file_content
        
        def addModelClass(model_name, flow_name, form_item_counter, flow_uuid):
            class Meta:
                default_permissions = ()
                permissions = (
                    (model_name+"_Add", _('新增')+flow_name),
                    (model_name+"_Modify", _('修改')+flow_name),
                    (model_name+"_View", _('檢視')+flow_name),
                    (model_name+"_Delete", _('刪除')+flow_name),
                )
            class Meta2:
                default_permissions = ()
            #add model to memory
            attrs = {'__module__': 'omformmodel.models','Meta': Meta}
            attrs['table_name'] = flow_name
            attrs['flow_uuid'] = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
            attrs['dataid_header'] = models.CharField(verbose_name= _('資料代碼'), max_length=3)
            attrs['data_no'] = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
            attrs['history'] = models.BooleanField(verbose_name = _('歷史資料'), default=False)
            attrs['status'] = models.CharField(verbose_name= _('狀態'), max_length=20,null=True, blank=True)
            attrs['title'] = models.CharField(verbose_name= _('標題'), max_length=20,null=True, blank=True)
            attrs['level'] = models.CharField(verbose_name= _('燈號'), max_length=20,null=True, blank=True)
            attrs['group'] = models.CharField(verbose_name= _('受派群組'), max_length=20,null=True, blank=True)
            attrs['closed'] = models.BooleanField(verbose_name = _('關閉標記'), default=False)
            attrs['stop_uuid'] = models.TextField(verbose_name = _('關卡'), blank=True, null=True)
            attrs['stop_chart_type'] = models.TextField(verbose_name = _('關卡類型'), blank=True, null=True)
            attrs['stop_chart_text'] = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)
            attrs['running'] = models.BooleanField(verbose_name = _('執行標記'), default=False)
            attrs['error'] = models.BooleanField(verbose_name = _('是否異常'), default=False)
            attrs['createtime'] = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
            attrs['updatetime'] = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
            attrs['stoptime'] = models.DateTimeField(verbose_name = _('停止時間'), null=True,blank=True)
            attrs['create_user'] = models.ForeignKey('omuser.OmUser', verbose_name = _('開單人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='create_'+flow_uuid)
            attrs['update_user'] = models.ForeignKey('omuser.OmUser', verbose_name = _('更新人員'), to_field='username', on_delete=models.SET_NULL, blank=True, null=True, related_name='update_'+flow_uuid)
            attrs['data_param'] = models.TextField(verbose_name = _('流程參數'), null=True,blank=True)
            attrs['error_message'] = models.TextField(verbose_name = _('錯誤訊息'), null=True,blank=True)
            attrs['init_data'] = models.ForeignKey('self', blank=True, null=True, related_name='extra_data', verbose_name = _('初始資料'), on_delete=models.CASCADE)
            for i in range(form_item_counter):
                attrs['formitm_'+str(i+1)] = models.TextField(null=True,blank=True)
            attrs['objects'] = FormatManager()
            type(model_name, (models.Model,), attrs)
            #flow value history
            attrs_vh = {'__module__': 'omformmodel.models','Meta': Meta2}
            attrs_vh['flow_uuid'] = models.UUIDField(verbose_name= _('流程編號'), null=True, blank=True)
            attrs_vh['data_no'] = models.IntegerField(verbose_name = _('資料編號'), null=True, blank=True)
            attrs_vh['data_id'] = models.IntegerField(verbose_name = _('多重資料編號'), blank=True, null=True)
            attrs_vh['chart_id'] = models.CharField(verbose_name= _('功能點'), max_length=50,null=True, blank=True)
            attrs_vh['stop_chart_type'] = models.TextField(verbose_name = _('關卡類型'), blank=True, null=True)
            attrs_vh['stop_chart_text'] = models.TextField(verbose_name = _('關卡名稱'), blank=True, null=True)
            attrs_vh['input_data'] = models.TextField(verbose_name= _('輸入參數'),null=True, blank=True)
            attrs_vh['output_data'] = models.TextField(verbose_name= _('輸出參數'),null=True, blank=True)
            attrs_vh['error'] = models.BooleanField(verbose_name = _('異常標記'), default=False)
            attrs_vh['createtime'] = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
            attrs_vh['updatetime'] = models.DateTimeField(verbose_name = _('更新時間'), auto_now=True)
            attrs_vh['objects'] = FormatManager()
            model_name_vh = model_name + '_ValueHistory'
            type(model_name_vh, (models.Model,), attrs_vh)
            #flow data no
            attrs_no = {'__module__': 'omformmodel.models','Meta': Meta2}
            attrs_no['createtime'] = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
            attrs_no['objects'] = FormatManager()
            model_name_no = model_name + '_DataNo'
            type(model_name_no, (models.Model,), attrs_no)
            call_command('makemigrations','omformmodel')
            call_command('migrate', app_label='omformmodel')
            
        
        while self.running:
            pass
        self.running = True
        result = True
        model_name = 'Omdata_' + flow_uuid
        file_content = getDefaultModel(model_name, flow_name, form_item_counter, flow_uuid)
        try:
            apps.get_registered_model('omformmodel',model_name)
            update_result = updateModel(self.file_path, model_name, file_content, form_item_counter)
            if update_result:
                addModelClass(model_name, flow_name, form_item_counter, flow_uuid)
        except LookupError:
            createModel(self.file_path, file_content)
            addModelClass(model_name, flow_name, form_item_counter, flow_uuid)
        except Exception as e:
            debug('deploy model error: %s' % e.__str__())
            result = False
        finally:
            self.running = False
            return result
    
    
    def deleteModel(self, flow_uuid):
        while self.running:
            pass
        self.running = True
        try:
            #function variable
            file_data = ""
            result = True
            model_name = 'Omdata_' + flow_uuid
            model_start = "#<" + model_name + " start>"
            model_end = "#<" + model_name + " end>"
            get_model_start_line = False
            change_complete = False
            apps.get_registered_model('omformmodel',model_name)
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if change_complete:
                        pass
                    elif get_model_start_line:
                        if model_end in line:
                            get_model_start_line = False
                            change_complete = True
                        line = ""
                    else:
                        if model_start in line:
                            get_model_start_line = True
                            line = ""
                    file_data += line
            with open(self.file_path,"w",encoding="utf-8") as f:
                f.write(file_data)
        except Exception as e:
            debug('delete model error: %s' % e.__str__())
            result = False
        finally:
            self.running = False
            return result
    


OMFormModel = FormModel()