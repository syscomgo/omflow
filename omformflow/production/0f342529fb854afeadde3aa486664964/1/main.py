import os, uuid, json
from omflow.syscom.omengine import OmEngine
from omflow.global_obj import GlobalObject
from omflow.settings import BASE_DIR
flow_uuid = '0f342529fb854afeadde3aa486664964'
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
        data['chart_id_to'] = 'FITEM_3'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_2':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_4'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_3':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_6'] == '0':
                data['chart_id_to'] = 'FITEM_2'
            if chart_input['FORMITM_6'] == '1':
                data['chart_id_to'] = 'FITEM_5'
            if chart_input['FORMITM_6'] == '2':
                data['chart_id_to'] = 'FITEM_7'
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
        data['chart_id_to'] = 'FITEM_4'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_7':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_4'
        OmEngine(flow_uuid,data).checkActive()
