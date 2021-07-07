import os, uuid, json
from omflow.syscom.omengine import OmEngine
from omflow.global_obj import GlobalObject
from omflow.settings import BASE_DIR
flow_uuid = '1e1f6c4c66b84d46bccbcd9f51f96bb7'
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
        data['chart_id_to'] = 'FITEM_15'
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
    elif chart_id == 'FITEM_15':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_27'
            data['flow_uuid'] = '7d0e2cb825e1452a8290c630677d42b4'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_16':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_24'
            data['flow_uuid'] = '9097310f4960430c8f2d7dd7d588386b'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_17':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_29'
            data['flow_uuid'] = '0f342529fb854afeadde3aa486664964'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_18':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_25'
            data['flow_uuid'] = '9097310f4960430c8f2d7dd7d588386b'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_19':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_30'
            data['flow_uuid'] = '731d5316d4c949d7bb21ecd4e878b9a3'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_20':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_31'
            data['flow_uuid'] = 'f22366ebecc244d9ad7b72abfae78c86'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_22':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_23'
            data['flow_uuid'] = '9097310f4960430c8f2d7dd7d588386b'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_23':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_4'
            data['flow_uuid'] = 'a93c6eb3b09941c38b8cb2588b75be70'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_24':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['ap_status'] == '00':
                data['chart_id_to'] = 'FITEM_17'
            if chart_input['ap_status'] == '11':
                data['chart_id_to'] = 'FITEM_15'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_25':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['ap_status'] == '00':
                data['chart_id_to'] = 'FITEM_19'
            if chart_input['ap_status'] == '11':
                data['chart_id_to'] = 'FITEM_17'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_27':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_11'] != '8':
                data['chart_id_to'] = 'FITEM_16'
            if chart_input['FORMITM_11'] == '8':
                data['chart_id_to'] = 'FITEM_28'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_28':
        try:
            data_str = json.dumps(data)
            content = json.loads(data_str)
            content['chart_id_to'] = 'FITEM_34'
            data['flow_uuid'] = 'c8450b76a94b4d7885b6f684c2dfe2d6'
            data['chart_id_from'] = ''
            data['chart_id_to'] = 'FITEM_1'
            data['flow_value'] = {}
            data['content'] = content
            data['error'] = False
        except Exception as e:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        OmEngine(data['flow_uuid'],data).checkActive()
    elif chart_id == 'FITEM_29':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_11'] != '8':
                data['chart_id_to'] = 'FITEM_18'
            if chart_input['FORMITM_11'] == '8':
                data['chart_id_to'] = 'FITEM_28'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_30':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_11'] != '8':
                data['chart_id_to'] = 'FITEM_20'
            if chart_input['FORMITM_11'] == '8':
                data['chart_id_to'] = 'FITEM_28'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_31':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_11'] != '8':
                data['chart_id_to'] = 'FITEM_22'
            if chart_input['FORMITM_11'] == '8':
                data['chart_id_to'] = 'FITEM_28'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_34':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['status'] == '0':
                data['chart_id_to'] = 'FITEM_15'
            if chart_input['status'] == '8':
                data['chart_id_to'] = 'FITEM_4'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
