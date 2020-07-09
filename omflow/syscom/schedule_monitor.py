import ast,time,json
from omflow.syscom.q_monitor import SchedulerMonitor
from omflow.models import Scheduler
from importlib import import_module
from omflow.syscom.schedule_base import OmSchedule
import datetime
from omflow.syscom.common import try_except
def cancelScheduleJob(ids):
    '''
    Use schedule tags cancel job
    input: id list
    return: None
    author: Jia Liu
    ''' 
    for i in ids:
        try:
            cancel_schedule_object = Scheduler.objects.get(id=int(i))
            schedule_id = cancel_schedule_object.id
            schedule_cycle = cancel_schedule_object.cycle
            schedule_cycle_date_list_str = cancel_schedule_object.cycle_date
            if schedule_cycle == "Monthly":
                sched_cycle_date_list = ast.literal_eval(schedule_cycle_date_list_str)
                for cycle_date in sched_cycle_date_list:
                    tag_id = str(schedule_id) + "_" + str(cycle_date)
                    OmSchedule.clearJob(tag_id)
            elif schedule_cycle == "Weekly":
                sched_cycle_date_list = ast.literal_eval(schedule_cycle_date_list_str)
                for cycle_date in sched_cycle_date_list:
                    tag_id = str(schedule_id) + "_" + str(cycle_date)
                    OmSchedule.clearJob(tag_id)
            else:
                OmSchedule.clearJob(str(i))
        except:
            pass
    
    
@try_except
def specific_Method(omobjects):
    '''
    specific method to execute job
    input: model object
    return: None
    author: Jia Liu
    ''' 
    if isinstance(omobjects.exec_fun, str):
        exec_dict = json.loads(omobjects.exec_fun)
    elif isinstance(omobjects.exec_fun, dict):
        exec_dict = omobjects.exec_fun
    module_name = exec_dict['module_name']
    method_name = exec_dict['method_name']
    module = import_module(module_name)
    getattr(module, method_name)(omobjects)
    
@try_except    
def put_flow_job(omobjects):
    '''
    if else put flow formdata to queue.
    input: model object
    return: None
    author: Jia Liu
    ''' 
    if isinstance(omobjects.input_param, str):
        exec_formdata = json.loads(omobjects.input_param) 
    elif isinstance(omobjects.input_param, dict):
        exec_formdata = omobjects.input_param
    exec_function = exec_formdata.pop('module_name')
    exec_method = exec_formdata.pop('method_name')
    if omobjects.cycle == "Once":
        SchedulerMonitor.putQueue(exec_function,exec_method,exec_formdata)
        last_run_time_dict = {}
        last_run_time_dict[str(omobjects.id)] = str(OmSchedule.last_run(str(omobjects.id)))
        omobjects.last_exec_time = json.dumps(last_run_time_dict)
        omobjects.is_active = False
        omobjects.save()
        OmSchedule.clearJob(str(omobjects.id))
    elif omobjects.cycle == "Weekly":
        if omobjects.last_exec_time != None and omobjects.next_exec_time != None:
            last_run_time_str = omobjects.last_exec_time
            next_run_time_str = omobjects.next_exec_time
            last_run_time_dict = json.loads(last_run_time_str)
            next_run_time_dict = json.loads(next_run_time_str)
        else:
            last_run_time_dict = {}
            next_run_time_dict = {}
        current_weekday = (datetime.datetime.today().strftime('%A'))
        get_tag_id = str(omobjects.id) + "_" + str(current_weekday)
        last_run_time_dict[get_tag_id] = str(OmSchedule.last_run(str(get_tag_id)))
        next_run_time_dict[get_tag_id] = str(OmSchedule.next_run(str(get_tag_id)))
        omobjects.last_exec_time = json.dumps(last_run_time_dict)
        omobjects.next_exec_time = json.dumps(next_run_time_dict)
        SchedulerMonitor.putQueue(exec_function,exec_method,exec_formdata)
        omobjects.save()
    elif omobjects.cycle == "Monthly" :
        if omobjects.last_exec_time != None and omobjects.next_exec_time != None:
            last_run_time_str = omobjects.last_exec_time
            next_run_time_str = omobjects.next_exec_time
            last_run_time_dict = json.loads(last_run_time_str)
            next_run_time_dict = json.loads(next_run_time_str)
        else:
            last_run_time_dict = {}
            next_run_time_dict = {}
        current_day = (datetime.datetime.today().strftime('%d'))
        get_tag_id = str(omobjects.id) + "_" + str(current_day)
        last_run_time_dict[get_tag_id] = str(OmSchedule.last_run(str(get_tag_id)))
        next_run_time_dict[get_tag_id] = str(OmSchedule.next_run(str(get_tag_id)))
        omobjects.last_exec_time = json.dumps(last_run_time_dict)
        omobjects.next_exec_time = json.dumps(next_run_time_dict)
        SchedulerMonitor.putQueue(exec_function,exec_method,exec_formdata)
        omobjects.save()
    else:
        last_run_time_dict = {}
        next_run_time_dict = {}
        last_run_time_dict[str(omobjects.id)] = str(OmSchedule.last_run(str(omobjects.id)))
        next_run_time_dict[str(omobjects.id)] = str(OmSchedule.next_run(str(omobjects.id)))
        omobjects.last_exec_time = json.dumps(last_run_time_dict)
        omobjects.next_exec_time = json.dumps(next_run_time_dict)
        SchedulerMonitor.putQueue(exec_function,exec_method,exec_formdata)
        omobjects.save()

@try_except        
def schedule_Execute(omobjects):
    '''
    Execute schedule
    input: model object
    return: run_pending()
    author: Jia Liu
    ''' 
    sched_exec_time = omobjects.exec_time
    sched_every = omobjects.every
    sched_cycle = omobjects.cycle
    sched_cycle_date = omobjects.cycle_date
    sched_id = str(omobjects.id)
    if sched_cycle == "Once":
        OmSchedule.every().cycle('Daily').exec_time(sched_exec_time).do(specific_Method,omobjects).tag(str(sched_id))
    elif sched_cycle == "Secondly":
        OmSchedule.every(int(sched_every)).cycle(sched_cycle).exec_time(sched_exec_time).do(specific_Method,omobjects).tag(str(sched_id))
    elif sched_cycle == "Minutely":
        OmSchedule.every(int(sched_every)).cycle(sched_cycle).exec_time(sched_exec_time).do(specific_Method,omobjects).tag(str(sched_id))
    elif sched_cycle == "Hourly":
        OmSchedule.every(int(sched_every)).cycle(sched_cycle).exec_time(sched_exec_time).do(specific_Method,omobjects).tag(str(sched_id))
    elif sched_cycle == "Monthly":
        for cycle_date in sched_cycle_date:
            tag_id = sched_id + "_" + cycle_date
            OmSchedule.every(int(sched_every)).cycle(sched_cycle).cycle_date(cycle_date).exec_time(sched_exec_time).do(specific_Method,omobjects).tag(tag_id)
    elif sched_cycle == "Daily":
        OmSchedule.every(int(sched_every)).cycle(sched_cycle).exec_time(sched_exec_time).do(specific_Method,omobjects).tag(str(sched_id))
    elif sched_cycle == "Weekly":
        for cycle_date in sched_cycle_date:
            tag_id = sched_id + "_" + cycle_date
            OmSchedule.every(int(sched_every)).cycle(sched_cycle).cycle_date(cycle_date).exec_time(sched_exec_time).do(specific_Method,omobjects).tag(tag_id)

@try_except
def scheduleDB_Execute():
    '''
    Execute DB schedule
    input: model object
    return: run_pending()
    author: Jia Liu
    ''' 
    schedule_pre_executeList = Scheduler.objects.filter(is_active='True') #'id','every','cycle','cycle_date','cycle_runtime','exec_fun','input_param'
    for schedule_pre in schedule_pre_executeList:
        sched_exec_time = schedule_pre.exec_time
        sched_every = schedule_pre.every
        sched_cycle = schedule_pre.cycle
        sched_cycle_date = schedule_pre.cycle_date
        sched_id = str(schedule_pre.id)
        if sched_cycle == "Once":
            OmSchedule.every().cycle('Daily').exec_time(sched_exec_time).do(specific_Method,schedule_pre).tag(sched_id)
        elif sched_cycle == "Secondly":
            OmSchedule.every(int(sched_every)).cycle(sched_cycle).exec_time(sched_exec_time).do(specific_Method,schedule_pre).tag(sched_id)
        elif sched_cycle == "Minutely":
            OmSchedule.every(int(sched_every)).cycle(sched_cycle).exec_time(sched_exec_time).do(specific_Method,schedule_pre).tag(sched_id)
        elif sched_cycle == "Hourly":
            OmSchedule.every(int(sched_every)).cycle(sched_cycle).exec_time(sched_exec_time).do(specific_Method,schedule_pre).tag(sched_id)
        elif sched_cycle == "Monthly":
            sched_cycle_date_list = ast.literal_eval(sched_cycle_date)
            for cycle_date in sched_cycle_date_list:
                tag_id = sched_id + "_" + cycle_date
                OmSchedule.every(int(sched_every)).cycle(sched_cycle).cycle_date(cycle_date).exec_time(sched_exec_time).do(specific_Method,schedule_pre).tag(tag_id)
        elif sched_cycle == "Daily": 
            OmSchedule.every(int(sched_every)).cycle(sched_cycle).exec_time(sched_exec_time).do(specific_Method,schedule_pre).tag(sched_id)            
        elif sched_cycle == "Weekly":
            sched_cycle_date_list = ast.literal_eval(sched_cycle_date)
            for cycle_date in sched_cycle_date_list:
                tag_id = sched_id + "_" + cycle_date
                OmSchedule.every(int(sched_every)).cycle(sched_cycle).cycle_date(cycle_date).exec_time(sched_exec_time).do(specific_Method,schedule_pre).tag(tag_id)

@try_except    
def scheduleThread():
    '''
    Schedule thread.
    input: scheduleDB_Execute function
    return: run_pending()
    author: Jia Liu
    ''' 
    scheduleDB_Execute()
    while True:
        OmSchedule.run_pending()
#         print(OmSchedule.jobs)
        time.sleep(0.0001)