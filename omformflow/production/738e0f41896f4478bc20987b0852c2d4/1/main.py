import os, uuid, json
from omflow.syscom.omengine import OmEngine
from omflow.global_obj import GlobalObject
from omflow.settings import BASE_DIR
flow_uuid = '738e0f41896f4478bc20987b0852c2d4'
version = 1
def main(data):
    chart_id = data.get('chart_id_from','')
    file_path = os.path.join(BASE_DIR, 'omformflow', 'production', flow_uuid, str(version))
    if chart_id == 'FITEM_1':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_14'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_4':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = ''
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_6':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = ''
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_7':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_32'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_9':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = ''
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_10':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_31'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_12':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_4'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_14':
        try:
            data['error'] = False
            data['collection_uuid'] = uuid.uuid4().hex
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data_str = json.dumps(data)
        data_FITEM_26 = json.loads(data_str)
        data_FITEM_26['chart_id_to'] = 'FITEM_26'
        OmEngine(flow_uuid,data_FITEM_26).checkActive()
        data_FITEM_7 = json.loads(data_str)
        data_FITEM_7['chart_id_to'] = 'FITEM_7'
        OmEngine(flow_uuid,data_FITEM_7).checkActive()
    elif chart_id == 'FITEM_15':
        try:
            data['error'] = False
            data['collection_uuid'] = uuid.uuid4().hex
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data_str = json.dumps(data)
        data_FITEM_9 = json.loads(data_str)
        data_FITEM_9['chart_id_to'] = 'FITEM_9'
        OmEngine(flow_uuid,data_FITEM_9).checkActive()
        data_FITEM_35 = json.loads(data_str)
        data_FITEM_35['chart_id_to'] = 'FITEM_35'
        OmEngine(flow_uuid,data_FITEM_35).checkActive()
    elif chart_id == 'FITEM_24':
        try:
            autoinstall = data.get('autoinstall',False)
            load_balance = data.get('load_balance',False)
            chart_input = data['chart_input']
            chart_input_str = json.dumps(chart_input)
            chart_input_c = json.loads(chart_input_str)
            import_error = False
            package = ''
            key = flow_uuid + '_' + chart_id
            compileObj = GlobalObject.__chartCompileObj__.get(key,'')
            chart_file_path = os.path.join(file_path, chart_id + '.py')
            if load_balance:
                with open(chart_file_path,'r',encoding='UTF-8') as f:
                    chart_file = f.read()
                    f.close()
            else:
                if not compileObj:
                    with open(chart_file_path,'r',encoding='UTF-8') as f:
                        chart_file = f.read()
                        f.close()
                    import_str = ''
                    chart_file_to_list = chart_file.split('\n')
                    for line in chart_file_to_list:
                        line_lstrip = line.lstrip()
                        if (line_lstrip[:7] == 'import ') or (line_lstrip[:5] == 'from '):
                            import_str += line_lstrip + '\n'
                    compile_import_str = compile(import_str,'','exec')
                    loop = True
                    last_package = ''
                    while loop:
                        try:
                            exec(compile_import_str)
                            compileObj = compile(chart_file,'','exec')
                            loop = False
                            package = ''
                        except Exception as e:
                            if 'No module named ' in e.__str__():
                                import subprocess
                                import sys
                                package = e.__str__()[17:-1]
                                if package == last_package or (not autoinstall):
                                    import_error = True
                                    loop = False
                                    data['error'] = True
                                    data['error_message'] = e.__str__()
                                else:
                                    last_package = package
                                    try:
                                        subprocess.check_call(['C:/Program Files/OMFLOW Server/Python/python.exe', '-m', 'pip', 'install', package])
                                    except Exception as e:
                                        import_error = True
                                        loop = False
                                        data['error'] = True
                                        data['error_message'] = e.__str__()
                            else:
                                import_error = True
                                loop = False
                                data['error'] = True
                                data['error_message'] = e.__str__()
                    if not import_error:
                        GlobalObject.__chartCompileObj__[key] = compileObj
                if not import_error:
                    exec(compileObj,chart_input_c)
                    for key in list(chart_input.keys()):
                        output_value = chart_input_c[key]
                        if isinstance(output_value, list) or isinstance(output_value, dict):
                            output_value_str = json.dumps(output_value)
                        else:
                            output_value_str = str(output_value)
                        chart_input[key] = output_value_str
                    data['error'] = False
        except Exception as e:
            if package:
                data['error_message'] = '找不到符合的條件。' + package
            else:
                data['error_message'] = e.__str__()
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_27'
        if load_balance:
            try:
                from ommonitor.views import sendPython
                sendPython(flow_uuid, data, chart_file)
            except:
                OmEngine(flow_uuid,data).checkActive()
        else:
            OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_26':
        try:
            autoinstall = data.get('autoinstall',False)
            load_balance = data.get('load_balance',False)
            chart_input = data['chart_input']
            chart_input_str = json.dumps(chart_input)
            chart_input_c = json.loads(chart_input_str)
            import_error = False
            package = ''
            key = flow_uuid + '_' + chart_id
            compileObj = GlobalObject.__chartCompileObj__.get(key,'')
            chart_file_path = os.path.join(file_path, chart_id + '.py')
            if load_balance:
                with open(chart_file_path,'r',encoding='UTF-8') as f:
                    chart_file = f.read()
                    f.close()
            else:
                if not compileObj:
                    with open(chart_file_path,'r',encoding='UTF-8') as f:
                        chart_file = f.read()
                        f.close()
                    import_str = ''
                    chart_file_to_list = chart_file.split('\n')
                    for line in chart_file_to_list:
                        line_lstrip = line.lstrip()
                        if (line_lstrip[:7] == 'import ') or (line_lstrip[:5] == 'from '):
                            import_str += line_lstrip + '\n'
                    compile_import_str = compile(import_str,'','exec')
                    loop = True
                    last_package = ''
                    while loop:
                        try:
                            exec(compile_import_str)
                            compileObj = compile(chart_file,'','exec')
                            loop = False
                            package = ''
                        except Exception as e:
                            if 'No module named ' in e.__str__():
                                import subprocess
                                import sys
                                package = e.__str__()[17:-1]
                                if package == last_package or (not autoinstall):
                                    import_error = True
                                    loop = False
                                    data['error'] = True
                                    data['error_message'] = e.__str__()
                                else:
                                    last_package = package
                                    try:
                                        subprocess.check_call(['C:/Program Files/OMFLOW Server/Python/python.exe', '-m', 'pip', 'install', package])
                                    except Exception as e:
                                        import_error = True
                                        loop = False
                                        data['error'] = True
                                        data['error_message'] = e.__str__()
                            else:
                                import_error = True
                                loop = False
                                data['error'] = True
                                data['error_message'] = e.__str__()
                    if not import_error:
                        GlobalObject.__chartCompileObj__[key] = compileObj
                if not import_error:
                    exec(compileObj,chart_input_c)
                    for key in list(chart_input.keys()):
                        output_value = chart_input_c[key]
                        if isinstance(output_value, list) or isinstance(output_value, dict):
                            output_value_str = json.dumps(output_value)
                        else:
                            output_value_str = str(output_value)
                        chart_input[key] = output_value_str
                    data['error'] = False
        except Exception as e:
            if package:
                data['error_message'] = '找不到符合的條件。' + package
            else:
                data['error_message'] = e.__str__()
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_6'
        if load_balance:
            try:
                from ommonitor.views import sendPython
                sendPython(flow_uuid, data, chart_file)
            except:
                OmEngine(flow_uuid,data).checkActive()
        else:
            OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_27':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_12'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_31':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_3'] == '4':
                data['chart_id_to'] = 'FITEM_24'
            if chart_input['FORMITM_3'] == '5':
                data['chart_id_to'] = 'FITEM_34'
            if chart_input['FORMITM_3'] == '3':
                data['chart_id_to'] = 'FITEM_35'
            if chart_input['FORMITM_3'] == '1':
                data['chart_id_to'] = 'FITEM_32'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_32':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_3'] == '4':
                data['chart_id_to'] = 'FITEM_33'
            if chart_input['FORMITM_3'] == '5':
                data['chart_id_to'] = 'FITEM_34'
            if chart_input['FORMITM_3'] == '1':
                data['chart_id_to'] = 'FITEM_39'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_33':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_24'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_34':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_4'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_35':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_36'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_36':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_3'] == '5':
                data['chart_id_to'] = 'FITEM_34'
            if chart_input['FORMITM_3'] == '4':
                data['chart_id_to'] = 'FITEM_10'
            if chart_input['FORMITM_3'] == '3':
                data['chart_id_to'] = 'FITEM_38'
            if chart_input['FORMITM_3'] == '2':
                data['chart_id_to'] = 'FITEM_35'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_38':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_31'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_39':
        try:
            autoinstall = data.get('autoinstall',False)
            load_balance = data.get('load_balance',False)
            chart_input = data['chart_input']
            chart_input_str = json.dumps(chart_input)
            chart_input_c = json.loads(chart_input_str)
            import_error = False
            package = ''
            key = flow_uuid + '_' + chart_id
            compileObj = GlobalObject.__chartCompileObj__.get(key,'')
            chart_file_path = os.path.join(file_path, chart_id + '.py')
            if load_balance:
                with open(chart_file_path,'r',encoding='UTF-8') as f:
                    chart_file = f.read()
                    f.close()
            else:
                if not compileObj:
                    with open(chart_file_path,'r',encoding='UTF-8') as f:
                        chart_file = f.read()
                        f.close()
                    import_str = ''
                    chart_file_to_list = chart_file.split('\n')
                    for line in chart_file_to_list:
                        line_lstrip = line.lstrip()
                        if (line_lstrip[:7] == 'import ') or (line_lstrip[:5] == 'from '):
                            import_str += line_lstrip + '\n'
                    compile_import_str = compile(import_str,'','exec')
                    loop = True
                    last_package = ''
                    while loop:
                        try:
                            exec(compile_import_str)
                            compileObj = compile(chart_file,'','exec')
                            loop = False
                            package = ''
                        except Exception as e:
                            if 'No module named ' in e.__str__():
                                import subprocess
                                import sys
                                package = e.__str__()[17:-1]
                                if package == last_package or (not autoinstall):
                                    import_error = True
                                    loop = False
                                    data['error'] = True
                                    data['error_message'] = e.__str__()
                                else:
                                    last_package = package
                                    try:
                                        subprocess.check_call(['C:/Program Files/OMFLOW Server/Python/python.exe', '-m', 'pip', 'install', package])
                                    except Exception as e:
                                        import_error = True
                                        loop = False
                                        data['error'] = True
                                        data['error_message'] = e.__str__()
                            else:
                                import_error = True
                                loop = False
                                data['error'] = True
                                data['error_message'] = e.__str__()
                    if not import_error:
                        GlobalObject.__chartCompileObj__[key] = compileObj
                if not import_error:
                    exec(compileObj,chart_input_c)
                    for key in list(chart_input.keys()):
                        output_value = chart_input_c[key]
                        if isinstance(output_value, list) or isinstance(output_value, dict):
                            output_value_str = json.dumps(output_value)
                        else:
                            output_value_str = str(output_value)
                        chart_input[key] = output_value_str
                    data['error'] = False
        except Exception as e:
            if package:
                data['error_message'] = '找不到符合的條件。' + package
            else:
                data['error_message'] = e.__str__()
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_15'
        if load_balance:
            try:
                from ommonitor.views import sendPython
                sendPython(flow_uuid, data, chart_file)
            except:
                OmEngine(flow_uuid,data).checkActive()
        else:
            OmEngine(flow_uuid,data).checkActive()
