import os, uuid, json
from omflow.syscom.omengine import OmEngine
from omflow.global_obj import GlobalObject
from omflow.settings import BASE_DIR
flow_uuid = '2d2fe67815a34cafa606640bdc7a3209'
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
        data['chart_id_to'] = 'FITEM_10'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_2':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_11'
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
    elif chart_id == 'FITEM_10':
        try:
            data['error'] = False
        except:
            data['error_message'] = ''
            data['error'] = True
        data['error_pass'] = False
        data['chart_id_to'] = 'FITEM_2'
        OmEngine(flow_uuid,data).checkActive()
    elif chart_id == 'FITEM_11':
        try:
            chart_input = data['chart_input']
            data['error'] = False
            if chart_input['FORMITM_14'] != '22':
                data['chart_id_to'] = 'FITEM_4'
            if chart_input['FORMITM_14'] == '22':
                data['chart_id_to'] = 'FITEM_10'
        except:
            data['error'] = True
        data['error_pass'] = False
        if not data['chart_id_to']:
            data['error_message'] = '找不到符合的條件。'
            data['error'] = True
        OmEngine(flow_uuid,data).checkActive()
