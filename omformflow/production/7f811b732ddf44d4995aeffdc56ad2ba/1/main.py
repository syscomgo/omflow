import os, uuid, json
from omflow.syscom.omengine import OmEngine
from omflow.global_obj import GlobalObject
from omflow.settings import BASE_DIR
flow_uuid = '7f811b732ddf44d4995aeffdc56ad2ba'
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
        data['chart_id_to'] = 'FITEM_2'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_2':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_3'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_3':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_4'] == 'dispatch':
                data['chart_id_to'] = 'FITEM_2'
            if chart_input['FORMITM_4'] == 'dispatch_done':
                data['chart_id_to'] = 'FITEM_5'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
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
    elif chart_id == 'FITEM_5':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_7'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_6':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_8'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_7':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if 'work_done' == chart_input['FORMITM_4']:
                data['chart_id_to'] = 'FITEM_6'
            if 'work' == chart_input['FORMITM_4']:
                data['chart_id_to'] = 'FITEM_5'
            if 'work_fail' == chart_input['FORMITM_4']:
                data['chart_id_to'] = 'FITEM_2'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_8':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_4'] == 'check_done':
                data['chart_id_to'] = 'FITEM_4'
            if chart_input['FORMITM_4'] == 'check_fail':
                data['chart_id_to'] = 'FITEM_5'
            if chart_input['FORMITM_4'] == 'check':
                data['chart_id_to'] = 'FITEM_6'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
