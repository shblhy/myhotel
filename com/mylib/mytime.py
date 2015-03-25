# -*- coding: utf-8 
from datetime import timedelta,datetime
import time
import unittest


class TimeTest(unittest.TestCase):
    def runTest(self):
        time_str='round_before_10_days'
        end_time=datetime.now()-timedelta(hours=2)
        start_time=end_time-timedelta(days=2)
        startTime,endTime=get_relative_time(time_str,start_time,end_time)
        print startTime.strftime('%Y-%m-%d %H:%M:%S')
        print endTime.strftime('%Y-%m-%d %H:%M:%S')


def get_relative_time(time_str,start_time,end_time,rnd=False):
    """
    last_1_days 前一天(昨天此时到现在)
    round_last_1_days 昨天（昨天0:00至24:00）
    last_3_days 前三天（三天前此时到现在）
    last_7_days 前七天（上周此时到本周此时）
    round_last_1_weeks 上周(上上周一0:00到上周一0:00)
    ast_2_days  最近两天
    after_2_days 在start_time后的两天
    before_2_day2 在end_time前的两天
    """
    unit = time_str.split('_')
    unit = unit[len(unit)-1]
    if time_str.startswith('before'):        
        if rnd:endTime=rndtime(end_time,unit)
        else:endTime=end_time
        startTime = get_timedelta(time_str,endTime)
    elif time_str.startswith('after'):
        if rnd:startTime=rndtime(start_time,unit)
        else:startTime=start_time
        endTime = get_timedelta(time_str,startTime)            
    elif time_str.startswith('last'):
        if rnd:endTime=rndtime(datetime.now(),unit)
        else:endTime=datetime.now()
        startTime = get_timedelta(time_str,endTime)
    elif time_str.startswith('round'):
        time_str=time_str.replace('round_','')
        return get_relative_time(time_str,start_time,end_time,True)
    return startTime,endTime


def get_timedelta(time_str,time_=datetime.now()):
    '''
    处理after_1_weeks等
    '''
    t=time_str.split('_')
    duration = int(t[1])
    unit = t[2]
    if unit=='months':
        td=timedelta(days=duration*30)
    elif unit=='weeks':
        td=timedelta(days=duration*7)
    elif unit=='minutes':
        td=timedelta(minutes=duration)
    elif unit=='hours':
        td=timedelta(hours=duration)
    elif unit=='days':
        td=timedelta(days=duration)
    else:
        raise Exception('time unit error')
    if t[0] in ['before','last']:
        return time_-td
    elif t[0]=='after':
        return time_+td


def rndtime(time_,unit,next_=False):#默认取本点或之前点，next_=True时取本点或之后点
    if unit in ['months','30_days']:
        rndTime=datetime(year=time_.year,month=time_.month)
    elif unit in ['weeks','7_days']:
        rndTime=datetime(year=time_.year,month=time_.month,day=time_.day)
        rndTime=rndTime- timedelta(days=rndTime.weekday())
    elif unit in ['days','1_days']:
        rndTime=datetime(year=time_.year,month=time_.month,day=time_.day)
    elif unit in ['hours','1_hours']:
        rndTime=datetime(year=time_.year,month=time_.month,day=time_.day,hour=time_.hour)
    elif unit=='minutes':
        rndTime=timedelta(year=time_.year,month=time_.month,day=time_.day,hour=time_.hour,minutes=time_.minute)
    elif unit == '5_minutes':
        rndTime = time_.replace(minute=time_.minute/5*5,second=0,microsecond=0)
    elif unit == '6_hours':
        rndTime = time_.replace(hour=time_.hour/6*6,minute=0,second=0,microsecond=0)
    if next_ and rndTime<time_:
        rndTime+=get_duration_by_str(unit)
    return rndTime


def get_next_month_begin_day(pre_time):
    if pre_time.month != 12:
        newTime = pre_time.replace(month=pre_time.month+1,day=1,hour=0,minute=0,second=0,microsecond=0)
    else:
        newTime = pre_time.replace(year=pre_time.year+1,month=1,day=1,hour=0,minute=0,second=0,microsecond=0)
    return newTime


def get_last_month_begin_day(pre_time):
    if pre_time.month != 1:
        newTime = pre_time.replace(month=pre_time.month-1,day=1,hour=0,minute=0,second=0,microsecond=0)
    else:
        newTime = pre_time.replace(year=pre_time.year-1,month=12,day=1,hour=0,minute=0,second=0,microsecond=0)
    return newTime


def datetime_to_timestamp(datetime_):
    return str(int(time.mktime(datetime_.timetuple())))


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_duration_by_str(duration_str):
    if not duration_str.__contains__('_'):
        params={duration_str:1}
    else:
        params={duration_str.split('_')[1]:int(duration_str.split('_')[0])}
    return timedelta(**params)


def get_duration(start_time, end_time):
    """ 用于根据开始结束时间获取时间趋势图的时间粒度，单位为秒 """
    d_val = end_time - start_time
    if d_val > timedelta(days=180):  # 时间间隔大于180天，为30天粒度
        duration = timedelta(days=180).total_seconds()  # '30_days'
    elif d_val > timedelta(days=60):  # 时间间隔大于60天，为7天粒度
        duration = timedelta(days=60).total_seconds()  # '7_days'
    elif d_val > timedelta(days=14):  # 时间间隔大于14天，为1天粒度
        duration = timedelta(days=14).total_seconds()  # '1_days'
    elif d_val > timedelta(days=2):  # 时间间隔大于2天, 为6小时粒度
        duration = timedelta(days=2).total_seconds()  # '6_hours'
    else:
        duration = timedelta(hours=1).total_seconds()  # '1_hours'
    return duration


def get_sta_point(start_time, end_time):
    """获取统计时间点, 供SQL语句查询时间趋势统计数据用。

    Args:
        start_time: 开始时间
        end_time: 结束时间

    Example:
        1. Input: start_time=8:10, end_time=8:30
           Return: duration=1_hours, sta_point=[('2013-10-12 9:00'， 201338182)]
        2. Input: start_time=8:10, end_time=9:20
           Return: duration=1_hours, sta_point=[('2013-10-12 9:00', 201338182), ('2013-10-12 10:00', 201333182)]
        3. Input: start_time=10-10 8:10, end_time=10-12 9:20
           Return: duration=6_hours, sta_point=[('2013-10-10 12:00, 201338182'), ('2013-10-10 18:00, 201338182'), ...]
    """

    d_val = end_time - start_time
    result = []
    if d_val > timedelta(days=180):  # 时间间隔大于180天，为30天粒度
        duration = '30_days'
        while start_time <= end_time:
            start_time = get_next_month_begin_day(start_time)
            timestamp = int(time.mktime(start_time.timetuple()))
            result.append((start_time.strftime('%Y-%m'), timestamp))
    elif d_val > timedelta(days=60):  # 时间间隔大于60天，为7天粒度
        duration = '7_days'
        while start_time <= end_time:
            start_time += timedelta(days=7-start_time.weekday())
            ret = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
            timestamp = int(time.mktime(ret.timetuple()))
            result.append((ret.strftime('%Y-%m-%d'), timestamp))
    elif d_val > timedelta(days=14):  # 时间间隔大于14天，为1天粒度
        duration = '1_days'
        while start_time <= end_time:
            start_time += timedelta(days=1)
            ret = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
            timestamp = int(time.mktime(ret.timetuple()))
            result.append((ret.strftime('%Y-%m-%d'), timestamp))
    elif d_val > timedelta(days=2):  # 时间间隔大于2天, 为6小时粒度
        duration = '6_hours'
        while start_time <= end_time:
            start_time += timedelta(hours=6-start_time.hour % 6)
            ret = start_time.replace(minute=0, second=0, microsecond=0)
            timestamp = int(time.mktime(ret.timetuple()))
            result.append((ret.strftime('%Y-%m-%d %H:%M'), timestamp))
    else:
        duration = '1_hours'
        while start_time <= end_time:
            start_time += timedelta(hours=1)
            ret = start_time.replace(minute=0, second=0, microsecond=0)
            timestamp = int(time.mktime(ret.timetuple()))
            result.append((ret.strftime('%Y-%m-%d %H:%M'), timestamp))
    return result


def str_timedelta(td):
    """ 将时间间隔对象timedelta转为中文描述 """
    t_desc = str(td).split(', ')
    if len(t_desc) == 1:
        td_str = t_desc[0].split(':')[0] + u'小时' + t_desc[0].split(':')[1] + u'分钟'
    else:
        td_str = t_desc[0].replace(' days', u'天').replace(' day', u'天')
        td_str += t_desc[1].split(':')[0] + u'小时' + t_desc[1].split(':')[1] + u'分钟'
    return td_str


def str_start_end_time(time_str, end_time=datetime.now()):
    """ 根据相对时间字符串获取开始结束时间，结果是,分隔的字符串

     Args:
        参见get_relative_time函数
     """
    start_time, end_time = get_relative_time(time_str, None, end_time)
    return start_time.strftime('%Y-%m-%d %H:%M:%S') + ',' + end_time.strftime('%Y-%m-%d %H:%M:%S')