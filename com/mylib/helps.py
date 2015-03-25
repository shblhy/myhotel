#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from sqlalchemy import func, desc
from com.mylib.myalchemy import DBSessionPbnet, T_Result_Dict, T_AlarmTask

from InternetQOEmonitorSystemFront.settings import STATIC_ROOT_PATH
from task.errcode import ErrCodeDict


def rate(numerator, denominator, ndigits=2, default=0):
    """ 计算百分比

    Description: 除数不为零，并保留一定小数位

    Args:
        numerator: 分子
        denominator：分母
        ndigits: 小数位数
        default: 当分母为0时，默认值
    """
    return round(numerator*1.0/denominator*100, ndigits) if denominator else default


def second(value):
    """ ms 转换为 s """
    return round(value*1.0/1000, 3) if value else 0


def kb(value):
    """ byte 转换为 kb """
    return round(value*1.0/1024, 2) if value else 0


def kb_s(value):
    """ byte/s 转换为kb/s """
    return round(value*1.0/1024, 2) if value else 0


def get_fault_desc(tt, obj):
    """ 故障现象

     Args:
        tt: 测试类型id，1、2、4、8、16、32
        obj: 任务测试结果，通过SQLAlchemy查询的T_DnsResult、T_DownloadResult等的实例对象
     """
    desc = ''

    if tt == 1:  # Ping测试
        if obj.score == 0:
            desc = u'ping不通'
        elif obj.short_factor == 'delay':
            desc = u'延迟大'
        elif obj.short_factor == 'loss_rate':
            desc = u'丢包率高'
        elif obj.short_factor == 'jitter':
            desc = u'波动过大'

    elif tt == 2:  # 域名解析测试
        desc = u'DNS解析失败'

    elif tt == 4:  # Telnet测试
        if obj.score == 0:
            desc = u'连不通'
        else:
            desc = u'延迟大'

    elif tt == 8:  # 路由跟踪测试
        desc = u'路由跟踪失败'

    elif tt == 16:  # 下载测试
        if obj.score == 0:
            desc = u'下载失败'
        elif obj.short_factor == 'down_rate':
            desc = u'下载速度慢'
        elif obj.short_factor == 'connect_time':
            desc = u'连接时间大'

    elif tt == 32:  # 页面测试
        if obj.score == 0 :
            desc = u'页面打不开'
        elif obj.short_factor == 'screen_time':
            desc = u'首屏时间长'
        elif obj.short_factor == 'page_load_time':
            desc = u'页面打开慢'
        elif obj.short_factor == 'error_proportion':
            desc = u'页面部分元素错'

    return desc


def get_fault_reason(tt, obj):
    """ 故障原因

    Args:
        tt: 测试类型id，1、2、4、8、16、32
        obj: 任务测试结果，通过SQLAlchemy查询的T_DnsResult、T_DownloadResult等的实例对象
    """
    reason = ''

    if tt == 1:  # Ping测试
        if obj.score == 0:
            reason = ErrCodeDict[obj.errcode].desc
        elif obj.short_factor in ('delay', 'loss_rate'):
            reason = u'链路问题'

    elif tt == 2:  # 域名解析测试
        reason = u'DNS解析失败'

    elif tt == 4:  # Telnet测试
        if obj.score == 0:
            reason = ErrCodeDict[obj.errcode].desc
        elif obj.short_factor == 'delay':
            reason = u'链路问题'

    elif tt == 8:  # 路由跟踪测试
        reason = u'路由跟踪失败'

    elif tt == 16:  # 下载测试
        if obj.short_factor == 'down_rate':
            reason = u'链路或源站可能有问题'
        elif obj.short_factor == 'connect_time':
            reason = u'源站可能有问题'
        elif obj.code and obj.code >= 300:
            reason = u'HTTP错误码' + str(obj.code)
        else:
            reason = ErrCodeDict[obj.errcode].desc

    elif tt == 32:  # 页面测试
        if obj.score == 0:
            if 100200 <= obj.errcode < 100600:
                # reason = str(obj.dest) + u'HTTP错误码' + str(obj.errcode - 100000)
                reason = u'HTTP错误码' + str(obj.errcode - 100000)
            else:
                # reason = str(obj.dest) + ErrCodeDict[obj.errcode].desc
                reason = ErrCodeDict[obj.errcode].desc
        else:
            try:
                res=[]
                # TODO: 下面代码需要修改
                from task.job import PageElement
                page_eles = PageElement.objects.get(tid=obj.tid)
                analyzeDict = page_eles.get_domain_analyze()

                if obj.short_factor  == 'error_proportion':
                    #错误请求占比高，按域名分别分析状态码，错误率高的进行重定向
                    for domain in analyzeDict:
                        #if analyzeDict[domain][1]/analyzeDict[domain][2]>0.5:
                        if analyzeDict[domain][1]>0:
                            res.append(domain)
                    reason = u'这些域名：'+u'、'.join(res)+u'返回了错误状态码'
                else:
                    #网速慢，按域名分布分析下载速度，下载速度低的进行重定向
                    for domain in analyzeDict:
                        if analyzeDict[domain][0]>0:
                            res.append(domain)
                    reason = u'这些域名：'+u'、'.join(res)+u'有元素下载速度过慢'
            except Exception,e0:
                print e0.message
                return ''

    return reason


def alarm_reason(obj):
    """ 告警原因

     Args:
        obj: 通过SQLAlchemy查询的T_Alarm对象
     """
    from task.testbase import TaskType
    session = DBSessionPbnet()
    result_model = T_Result_Dict[TaskType.objects.get(id=obj.tt).test_name]  # 根据测试类型获取测试结果Model
    if obj.flag == 1:  # 告警已结束
        if not obj.reason:
            # 如果已结束的告警没有告警原因，获取产生此告警的测试结果中根据short_factor分组最多的一条,并更新
            sub_q = session.query(
                func.max(result_model.tid).label('tid')
            ).join(
                T_AlarmTask, T_AlarmTask.tid == result_model.tid
            ).filter(
                T_AlarmTask.alarm_id == obj.id
            ).group_by(
                result_model.short_factor
            ).order_by(desc(func.count(result_model.tid))).limit(1).subquery()
            recent_result = session.query(result_model).join(sub_q, sub_q.c.tid == result_model.tid).first()
            reason = get_fault_desc(obj.tt, recent_result)
            obj.reason = reason
            session.commit()
        else:
            reason = obj.reason
    else:  # 告警持续中
        # 获取最近一次的测试结果的故障现象，作为告警原因
        recent_result = session.query(
            result_model
        ).join(
            T_AlarmTask, T_AlarmTask.tid == result_model.tid
        ).filter(
            T_AlarmTask.alarm_id == obj.id
        ).order_by(desc(result_model.tid)).first()
        reason = get_fault_desc(obj.tt, recent_result)
    return reason


def is_draw_map(sid):
    dir = os.path.join(STATIC_ROOT_PATH, 'components/svgMap/maps/')
    return os.path.isfile(dir + sid + '.svg')

