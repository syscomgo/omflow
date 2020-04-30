'''
This custom schedule is based on dbader Schedule(https://github.com/dbader/schedule).
Omflow base schedule object.
Created on 2020/02/01
@author: Darren Liu
'''
import collections
import datetime
from datetime import datetime as dt
import functools
import random
import json
from omflow.models import Scheduler 

"""
---Daily---
example1: Omschedule.every(int(number)).cycle("Daily").exec_time(sched_exec_time).do(somthing)
---Weekly---
example2: Omschedule.every(int(number)).cycle("Weekly").cycle_date("Monday").exec_time(sched_exec_time).do(somthing)
---Monthly---
example3: Omschedule.every(int(number)).cycle("Monthly").cycle_date("01").exec_time(sched_exec_time).do(somthing)
---Secondly---
example4: Omschedule.every(int(number)).cycle("Secondly").exec_time(sched_exec_time).do(somthing)
---Minutely---
example5: Omschedule.every(int(number)).cycle("Minutely").exec_time(sched_exec_time).do(somthing)
---Hourly---
example6: Omschedule.every(int(number)).cycle("Hourly").exec_time(sched_exec_time).do(somthing)
"""

class ScheduleError(Exception):
    pass

class ScheduleValueError(ScheduleError):
    pass

class Schedule(object):
    def __init__(self):
        self.jobs = []
        
    def clearJob(self, tag=None):     
        if tag is None:
            del self.jobs[:]
        else:
            self.jobs[:] = (job for job in self.jobs if tag not in job.tags)

    def every(self, interval=1):
        job = Job(interval, self)
        return job
    
    def _run_job(self, job):
        job.run()
    
    def run_pending(self):
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            self._run_job(job)
    
    def last_run(self,tag=None): 
        last_run_jobs = self.jobs[:]    
        last_run_jobs[:] = (job for job in last_run_jobs if tag in job.tags)
        targetjob = last_run_jobs[0].next_run
        return targetjob
     
    def next_run(self,tag=None):
        next_run_jobs = self.jobs[:]    
        next_run_jobs[:] = (job for job in next_run_jobs if tag in job.tags)
        if next_run_jobs[0].unit != "Monthly":
            targetjob = next_run_jobs[0].next_run + next_run_jobs[0].period
        else: 
            targetjob = next_run_jobs[0].monthAdd(next_run_jobs[0].next_run,next_run_jobs[0].interval,next_run_jobs[0].at_day)
        return targetjob 
                       
class Job(object):
    def __init__(self, interval,schedule=None):
        self.interval = interval  
        self.exec_datetime = None
        self.unit = None
        self.latest = None
        self.job_func = None
        self.at_day = None
        self.at_time = None  
        self.last_run = None  
        self.next_run = None  
        self.period = None  
        self.start_day = None  
        self.tags = set()  
        self.schedule = schedule  
    
    def __lt__(self, other):
        return self.next_run < other.next_run

    def __repr__(self):
        def format_time(t):
            return t.strftime('%Y-%m-%d %H:%M:%S') if t else '[never]'

        timestats = '(last run: %s, next run: %s)' % (
                    format_time(self.last_run), format_time(self.next_run))

        if hasattr(self.job_func, '__name__'):
            job_func_name = self.job_func.__name__
        else:
            job_func_name = repr(self.job_func)
        args = [repr(x) for x in self.job_func.args]
        kwargs = ['%s=%s' % (k, repr(v))
                  for k, v in self.job_func.keywords.items()]
        call_repr = job_func_name + '(' + ', '.join(args + kwargs) + ')'

        if self.at_time is not None:
            return 'Every %s %s at %s do %s %s' % (
                   self.interval,
                   self.unit[:-1] if self.interval == 1 else self.unit,
                   self.at_time, call_repr, timestats)
        else:
            fmt = (
                'Every %(interval)s ' +
                ('to %(latest)s ' if self.latest is not None else '') +
                '%(unit)s do %(call_repr)s %(timestats)s'
            )

            return fmt % dict(
                interval=self.interval,
                latest=self.latest,
                unit=(self.unit[:-1] if self.interval == 1 else self.unit),
                call_repr=call_repr,
                timestats=timestats
            )
            
    def cycle(self,param):
        self.unit = param
        if param =="Secondly":
            self.unit = "seconds"
        elif param =="Minutely":
            self.unit = "minutes"
        elif param =="Hourly":
            self.unit = "hours"
        elif param =="Daily":
            self.unit = "days"
        elif param =="Weekly":
            self.unit = "weeks"
        return self

    def cycle_date(self,cycledate):
        if self.unit == "weeks" or self.unit == "Monthly":
            self.start_day = cycledate
            return self
            
    def exec_time(self,param):
        if isinstance(param, str):
            self.exec_datetime = dt.strptime(param,'%Y-%m-%d %H:%M:%S')
        else:
            self.exec_datetime = param
        time_format =self.exec_datetime
        time_value_str = "{:%H:%M:%S}".format(time_format)
        time_value_list = time_value_str.split(':')
        hour, minute, second = time_value_list
        if self.unit == 'Monthly':
            day = int(self.start_day)
            self.at_day = day
            hour = int(hour)
        elif self.unit == 'days' or self.unit == 'weeks':
            hour = int(hour)
        elif self.unit == 'hours':
            hour = 0
        elif self.unit == 'minutes':
            hour = 0
            minute = 0
        minute = int(minute)
        second = int(second)
        if self.unit == "seconds":
            self.at_time = None
        else:
            self.at_time = datetime.time(hour, minute, second)
        return self
    
    @property
    def should_run(self):
        return datetime.datetime.now() >= self.next_run
    
    def tag(self, *tags):

        if not all(isinstance(tag, collections.Hashable) for tag in tags):
            raise TypeError('Tags must be hashable')
        self.tags.update(tags)
        return self
    
    def do(self, job_func, *args, **kwargs):
        self.job_func = functools.partial(job_func, *args, **kwargs)
        try:
            functools.update_wrapper(self.job_func, job_func)
        except AttributeError:
            pass
        self.schedule_next_run()
        self.schedule.jobs.append(self)
        return self
    
    def run(self):
        ret = self.job_func()
        if self.last_run == None and self.exec_datetime > datetime.datetime.now():
            self.last_run = None
        elif self.last_run == None and self.exec_datetime <= datetime.datetime.now():
            if self.unit != "Monthly":
                if self.unit == "weeks":
                    schedule_id = list(self.tags)[0]
                    index_count = schedule_id.index('_')
                    index_id = schedule_id[:index_count]
                    format_str_time = Scheduler.objects.get(id=int(index_id)).last_exec_time
                    dict_format_time = json.loads(format_str_time)
                    self.last_run = dt.strptime(dict_format_time[list(self.tags)[0]],'%Y-%m-%d %H:%M:%S')
                else:
                    schedule_id = list(self.tags)
                    format_str_time = Scheduler.objects.get(id=schedule_id[0]).last_exec_time
                    dict_format_time = json.loads(format_str_time)
                    self.last_run = dt.strptime(dict_format_time[str(schedule_id[0])],'%Y-%m-%d %H:%M:%S')
            else:
                schedule_id = list(self.tags)[0]
                index_count = schedule_id.index('_')
                index_id = schedule_id[:index_count]
                format_str_time = Scheduler.objects.get(id=int(index_id)).last_exec_time
                dict_format_time = json.loads(format_str_time)
                self.last_run = dt.strptime(dict_format_time[list(self.tags)[0]],'%Y-%m-%d %H:%M:%S')
        else:
            if self.unit == "Monthly":
                self.last_run = self.next_run
            else:
                self.last_run = self.last_run + self.period
        self.schedule_next_run()
        return ret
    

    def monthAdd(self, date, interval,at_day):
        if date > datetime.datetime.now():
            targetdate = date
        else:
            addmonth = interval + date.month
            try:
                execute_date = date.replace(year=date.year+int(date.month/12),month=(date.month % 12),day = at_day)
            except ValueError:
                try:
                    execute_date = date.replace(year=date.year+int(addmonth/12),month=(addmonth % 12),day = at_day)
                except ValueError:
                    try:
                        execute_date = date.replace(year=date.year+int((addmonth+1)/12),month=(addmonth+1 % 12),day = at_day)
                    except ValueError:
                        try:
                            execute_date = date.replace(year=date.year+int((addmonth+1)/12),month=((addmonth+interval) % 12),day = at_day)
                        except:
                            if ((addmonth+interval) % 12) == 0:
                                execute_date = date.replace(year=date.year+int((interval+1)/12),month=date.month,day = at_day)
            try:
                if datetime.datetime.now() < execute_date:
                    try:
                        targetdate = date.replace(year=execute_date.year+int(execute_date.month/12),month=(execute_date.month % 12),day = at_day)
                    except:
                        targetdate = date.replace(year=execute_date.year,month=execute_date.month,day = at_day)
                else:
                    targetdate = date.replace(year=execute_date.year+int(addmonth/12),month=(addmonth % 12),day = at_day)
            except ValueError:
                targetdate = date.replace(year=execute_date.year+int((addmonth+1)/12),month=((addmonth+1) % 12))
        return targetdate
    
    def format_nowtime(self,_exec_time,cycletype):
        cycle = cycletype
        exec_datetime = _exec_time
        now_time_dminsecond = dt.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
        now_time = dt.strptime(now_time_dminsecond,'%Y-%m-%d %H:%M:%S')
        if cycle == "seconds":
            addminute = now_time.minute -1
            if addminute == -1:
                addminute_zero = 0
                now_time_replace = now_time.replace(minute=addminute_zero,second=int("{:%S}".format(exec_datetime)))
            else:    
                now_time_replace = now_time.replace(minute=addminute,second=int("{:%S}".format(exec_datetime)))
            while now_time_replace < now_time:
                now_time_replace += self.period
        elif cycle == "minutes":
            addhour = now_time.hour -1
            if addhour == -1:
                addhour_zero = 0
                now_time_replace = now_time.replace(hour=addhour_zero,minute=int("{:%M}".format(exec_datetime)),second=int("{:%S}".format(exec_datetime)))
            else:
                now_time_replace = now_time.replace(hour=addhour,minute=int("{:%M}".format(exec_datetime)),second=int("{:%S}".format(exec_datetime)))    
            while now_time_replace < now_time:
                now_time_replace += self.period
        elif cycle == "hours":
            now_time_replace =  now_time.replace(
                                                 hour=int("{:%H}".format(exec_datetime)),\
                                                 minute=int("{:%M}".format(exec_datetime)),\
                                                 second=int("{:%S}".format(exec_datetime)))
            while now_time_replace < now_time:
                now_time_replace += self.period
        elif cycle == "days":
            args = [x for x in self.job_func.args]
            omschedule_next_run_str = args[0].next_exec_time
            if omschedule_next_run_str != None:
                omschedule_next_run_dict = json.loads(omschedule_next_run_str)
                omschedule_next_run = dt.strptime(omschedule_next_run_dict[str(args[0].id)],'%Y-%m-%d %H:%M:%S')
            else:
                omschedule_next_run = None
            om_next_run = omschedule_next_run
            if om_next_run is None:
                now_time_replace = exec_datetime
            elif om_next_run > datetime.datetime.now():
                now_time_replace = omschedule_next_run
            else:
                now_time_replace = omschedule_next_run
        else:
            now_time_replace = now_time
        return now_time_replace
        
    
    def schedule_next_run(self):
        if self.unit not in ('seconds', 'minutes', 'hours', 'days', 'weeks','Monthly'):
            raise ScheduleValueError('Invalid unit')

        if self.latest is not None:
            if not (self.latest >= self.interval):
                raise ScheduleError('`latest` is greater than `interval`')
            interval = random.randint(self.interval, self.latest)
        else:
            interval = self.interval
        if self.unit == 'Monthly':
            if self.at_time is None or self.at_day is None:
                raise ScheduleError('Monthly jobs expect "at()" to be defined')
            if self.last_run == None:
                args = [x for x in self.job_func.args]
                omschedule_next_run_str = args[0].next_exec_time
                if omschedule_next_run_str is None or omschedule_next_run_str == "":
                    if isinstance(args[0].exec_time, str):
                        omschedule_time = dt.strptime(args[0].exec_time,'%Y-%m-%d %H:%M:%S')
                    elif isinstance(args[0].exec_time, datetime.date):
                        omschedule_time = args[0].exec_time
                    omschedule_next_run = self.monthAdd(omschedule_time,self.interval,self.at_day)
                else:
                    omschedule_next_run_dict = json.loads(omschedule_next_run_str)
                    tag_id = str(args[0].id) + "_" + str(self.start_day)
                    try:
                        omschedule_next_run_time = omschedule_next_run_dict[tag_id]
                    except:
                        if isinstance(args[0].exec_time, str):
                            omschedule_time = dt.strptime(args[0].exec_time,'%Y-%m-%d %H:%M:%S')
                        elif isinstance(args[0].exec_time, datetime.date):
                            omschedule_time = args[0].exec_time
                        omschedule_next_run = self.monthAdd(omschedule_time,self.interval,self.at_day)
                        omschedule_next_run_time = str(omschedule_next_run)
                    omschedule_next_run = dt.strptime(omschedule_next_run_time, '%Y-%m-%d %H:%M:%S')
                self.next_run = omschedule_next_run
            else:
                self.next_run = self.monthAdd(self.last_run,self.interval,self.at_day)
        else:
            self.period = datetime.timedelta(**{self.unit: interval})
            if self.last_run == None:
                if self.exec_datetime >= datetime.datetime.now():
                    self.next_run = self.exec_datetime
                else:
                    datetime_replace = self.format_nowtime(self.exec_datetime,self.unit)
                    self.next_run = datetime_replace
            else:
                self.next_run = self.last_run + self.period
        if self.start_day is not None:
            if self.unit != 'weeks' and self.unit != 'Monthly':
                raise ScheduleValueError('`unit` should be \'weeks or Monthly\'')
            elif self.unit == 'weeks':
                weekdays = (
                    'Monday',
                    'Tuesday',
                    'Wednesday',
                    'Thursday',
                    'Friday',
                    'Saturday',
                    'Sunday'
                )
                if self.start_day not in weekdays:
                    raise ScheduleValueError('Invalid start day')
                weekday = weekdays.index(self.start_day)
                days_ahead = weekday - self.next_run.weekday()
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                self.next_run += datetime.timedelta(days_ahead)

            elif self.unit == "Monthly":
                try:
                    self.next_run = self.next_run.replace(day=self.at_day)
                except ValueError:
                    pass
        if self.at_time is not None:
            if (self.unit not in ('Monthly','days', 'hours', 'minutes')
                    and self.start_day is None):
                raise ScheduleValueError(('Invalid unit without'
                                          ' specifying start day'))
            kwargs = {
                'second': self.at_time.second,
                'microsecond': 0
            }
            if self.unit in ['Monthly', 'days'] or self.start_day is not None:
                kwargs['hour'] = self.at_time.hour
            if self.unit in ['Monthly', 'days', 'hours'] or \
               self.start_day is not None:
                kwargs['minute'] = self.at_time.minute
            self.next_run = self.next_run.replace(**kwargs)
        if self.start_day is not None and self.at_time is not None and self.unit != 'Monthly':
            if (self.next_run - datetime.datetime.now()).days >= 7:
                self.next_run -= self.period
        

OmSchedule = Schedule()

jobs = OmSchedule.jobs
