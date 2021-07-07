import os
from django.core.management import call_command
from django.conf import settings
from django.db import models
from omflow.syscom.customfield import FormatManager
from django.utils.translation import gettext as _
from omflow.syscom.default_logger import debug
from omflow.syscom.common import getModel


class PolicyModel():
    
    def __init__(self):
        self.file_path = os.path.join(settings.BASE_DIR, "ompolicymodel", "models.py")
        self.running = False


    def deployModel(self, policy_id, policy_name, variable_list):
        '''
        input: policy_id, policy_name, variable_item_counter
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
        
        def updateModel(file_path, model_name, variable_list):
            '''
            update model
            input: file_content
            return: None
            author: Kolin Hsu
            '''
            #function variable
            file_data = ""
            add_location = "#" + model_name + " add field here"
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if add_location in line:
                        for variable_name in variable_list:
                            file_data += "    " + variable_name + " = models.TextField(null=True,blank=True)\n"
                    file_data += line
            with open(file_path,"w",encoding="utf-8") as f:
                f.write(file_data)
        
        def getDefaultModel(model_name, policy_name, variable_list):
            '''
            create default model class
            input: model_name, form_item_counter
            return: file_content
            author: Kolin Hsu
            '''
            file_content = ""
            file_content += "class " + model_name + "(models.Model):\n"
            code_space = "    "
            file_content += code_space + "table_name = _('"+policy_name+"')\n"
            file_content += code_space + "collector = models.ForeignKey('ommonitor.Collector', on_delete=models.CASCADE)\n"
            file_content += code_space + "error = models.BooleanField(verbose_name = _('是否異常'), default=False)\n"
            file_content += code_space + "createtime = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)\n"
            file_content += code_space + "error_message = models.TextField(verbose_name = _('錯誤訊息'), null=True,blank=True)\n"
            for variable_name in variable_list:
                file_content += code_space + variable_name + " = models.TextField(null=True,blank=True)\n"
            file_content += code_space + "#" + model_name + " add field here\n"
            file_content += code_space + "objects = FormatManager()\n"
            file_content += code_space + "class Meta:\n"
            code_space += "    "
            file_content += code_space + "default_permissions = ()\n"
            code_space = code_space.replace("    ", "", 1)
            code_space = code_space.replace("    ", "", 1)
            file_content += "#<new here>\n"
            return file_content
        
        def addModelClass(model_name, policy_name, variable_list):
            class Meta:
                default_permissions = ()
            #add model to memory
            attrs = {'__module__': 'ompolicymodel.models','Meta': Meta}
            attrs['table_name'] = policy_name
            attrs['collector'] = models.ForeignKey('ommonitor.Collector', on_delete=models.CASCADE)
            attrs['error'] = models.BooleanField(verbose_name = _('是否異常'), default=False)
            attrs['createtime'] = models.DateTimeField(verbose_name = _('建立時間'), auto_now_add=True)
            attrs['error_message'] = models.TextField(verbose_name = _('錯誤訊息'), null=True,blank=True)
            for variable_name in variable_list:
                attrs[variable_name] = models.TextField(null=True,blank=True)
            attrs['objects'] = FormatManager()
            type(model_name, (models.Model,), attrs)
            call_command('makemigrations','ompolicymodel')
            call_command('migrate', app_label='ompolicymodel')
            
        
        while self.running:
            pass
        self.running = True
        result = True
        model_name = 'OmPolicy_' + str(policy_id)
        try:
            model = getModel('ompolicymodel',model_name)
            if model:
                filed_list = list(f.name for f in model._meta.fields)
                update_variable_list = list(set(variable_list) - set(filed_list))
                if update_variable_list:
                    updateModel(self.file_path, model_name, variable_list)
                    all_variable_list = filed_list + update_variable_list
                    addModelClass(model_name, policy_name, all_variable_list)
            else:
                file_content = getDefaultModel(model_name, policy_name, variable_list)
                createModel(self.file_path, file_content)
                addModelClass(model_name, policy_name, variable_list)
        except Exception as e:
            debug('deploy model error: %s' % e.__str__())
            result = False
        finally:
            self.running = False
            return result
    
    
    def deleteModel(self, policy_id):
        while self.running:
            pass
        self.running = True
        try:
            #function variable
            file_data = ""
            result = True
            model_name = 'OmPolicy_' + str(policy_id)
            model_start = "#<" + model_name + " start>"
            model_end = "#<" + model_name + " end>"
            get_model_start_line = False
            change_complete = False
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
    


OMPolicyModel = PolicyModel()