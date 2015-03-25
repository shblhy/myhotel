# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
SQLAlchemy Expression Language: SQLAlchemy表达式语言
SQLAlchemy表达式在联合查询时非常有效，这是django orm所做不到的。
例如：批量外键操作、多重select操作。。。

Usage: 参看位于此文件最后的main方法
参见 ProberTest.myalchemy_test方法

"""

from sqlalchemy import create_engine, Table
from sqlalchemy.sql import select
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

# sessionmaker: session对象的工厂
DBSessionWeb = sessionmaker(autoflush=True, autocommit=False)
DBSessionPbnet = sessionmaker(autoflush=True, autocommit=False)
DBSessionMem = sessionmaker(autoflush=True, autocommit=False)

# Table和Model的映射，所有的Model都应该继承此类
DeclarativeBaseWeb = declarative_base()
DeclarativeBasePbnet = declarative_base()
DeclarativeBaseMem = declarative_base()

# MetaData: 所有Table对象和它们相关Schema的集合，通过bind一个Engine或Connection来执行SQL
metadata_web = DeclarativeBaseWeb.metadata
metadata_pbnet = DeclarativeBasePbnet.metadata
metadata_mem = DeclarativeBaseMem.metadata


def init_model(engine1, engine2, engine3):
    """将engine绑定到session和metadata"""
    DBSessionWeb.configure(bind=engine1)
    DBSessionPbnet.configure(bind=engine2)
    DBSessionMem.configure(bind=engine3)

    metadata_web.bind = engine1
    metadata_pbnet.bind = engine2
    metadata_mem.bind = engine3


def get_db_url(db_dict):
    """将Django Settings DATABASES 数据库参数转化SQLAlchemy所需的连接url"""
    engine = db_dict['ENGINE'].split('.')[-1]
    return '%s://%s:%s@%s:%s/%s' % (engine, db_dict['USER'], db_dict['PASSWORD'], db_dict['HOST'], db_dict['PORT'], db_dict['NAME'])


# ---------------------初始化engine，并完成绑定--------------------------------
from InternetQOEmonitorSystemFront.settings import DATABASES, SHOW_SQL
engine_args = {
    'connect_args': {'charset': 'utf8'},
    'encoding': 'utf-8',
    'pool_size': 100,
    'pool_recycle': 7200,
    'pool_timeout': 7200,
    'echo': SHOW_SQL,
}
engine_web = create_engine(get_db_url(DATABASES['default']), **engine_args)
engine_pbnet = create_engine(get_db_url(DATABASES['backend']), **engine_args)
engine_mem = create_engine(get_db_url(DATABASES['mem']), **engine_args)
init_model(engine_web, engine_pbnet, engine_mem)


# -------------------------------Tables------------------------------------------

# ----Auth模块------
t_user = Table('auth_user', metadata_web, autoload=True)  # 用户
t_group = Table('auth_group', metadata_web, autoload=True)  # 角色(组)

# ----任务模块------
t_project = Table('task_test_plan', metadata_web, autoload=True, schema=engine_web.url.database)  # 测试计划
class T_Project(DeclarativeBaseWeb):
    __table__ = t_project

t_project_monitors = Table('task_test_plan_monitors', metadata_web, autoload=True, schema=engine_web.url.database)
class T_ProjectMonitor(DeclarativeBaseWeb):
    __table__ = t_project_monitors

t_tpg = Table('task_taskplangroup', metadata_web, autoload=True, schema=engine_web.url.database)  # TaskSchedule
class T_PlanGroup(DeclarativeBaseWeb):
    __table__ = t_tpg

t_dns_task = Table('task_dnsplan', metadata_web, autoload=True, schema=engine_web.url.database)
class T_DnsTask(DeclarativeBaseWeb):
    __table__ = t_dns_task

t_download_task = Table('task_downloadplan', metadata_web, autoload=True, schema=engine_web.url.database)
class T_DownloadTask(DeclarativeBaseWeb):
    __table__ = t_download_task

t_page_task = Table('task_pageplan', metadata_web, autoload=True, schema=engine_web.url.database)
class T_PageTask(DeclarativeBaseWeb):
    __table__ = t_page_task

t_ping_task = Table('task_pingplan', metadata_web, autoload=True, schema=engine_web.url.database)
class T_PingTask(DeclarativeBaseWeb):
    __table__ = t_ping_task

t_telnet_task = Table('task_telnetplan', metadata_web, autoload=True, schema=engine_web.url.database)
class T_TelnetTask(DeclarativeBaseWeb):
    __table__ = t_telnet_task

t_tracert_task = Table('task_tracertplan', metadata_web, autoload=True, schema=engine_web.url.database)
class T_TracertTask(DeclarativeBaseWeb):
    __table__ = t_tracert_task

t_task_dict = {
    'dns': t_dns_task,
    'download': t_download_task,
    'page': t_page_task,
    'ping': t_ping_task,
    'telnet': t_telnet_task,
    'tracert': t_tracert_task,
}
T_Task_Dict = {
    'dns': T_DnsTask,
    'download': T_DownloadTask,
    'page': T_PageTask,
    'ping': T_PingTask,
    'telnet': T_TelnetTask,
    'tracert': T_TracertTask,
}

t_dns_params = Table('task_taskparam_dns', metadata_web, autoload=True, schema=engine_web.url.database)
class T_DnsParams(DeclarativeBaseWeb):
    __table__ = t_dns_params

t_download_params = Table('task_taskparam_download', metadata_web, autoload=True, schema=engine_web.url.database)
class T_DownloadParams(DeclarativeBaseWeb):
    __table__ = t_download_params

t_page_params = Table('task_taskparam_page', metadata_web, autoload=True, schema=engine_web.url.database)
class T_PageParams(DeclarativeBaseWeb):
    __table__ = t_page_params

t_ping_params = Table('task_taskparam_ping', metadata_web, autoload=True, schema=engine_web.url.database)
class T_PingParams(DeclarativeBaseWeb):
    __table__ = t_ping_params

t_telnet_params = Table('task_taskparam_telnet', metadata_web, autoload=True, schema=engine_web.url.database)
class T_TelnetParams(DeclarativeBaseWeb):
    __table__ = t_telnet_params

t_tracert_params = Table('task_taskparam_tracert', metadata_web, autoload=True, schema=engine_web.url.database)
class T_TracertParams(DeclarativeBaseWeb):
    __table__ = t_tracert_params

t_params_dict = {
    'dns': t_dns_params,
    'download': t_download_params,
    'page': t_page_params,
    'ping': t_ping_params,
    'telnet': t_telnet_params,
    'tracert': t_tracert_params,
}
T_Params_Dict = {
    'dns': T_DnsParams,
    'download': T_DownloadParams,
    'page': T_PageParams,
    'ping': T_PingParams,
    'telnet': T_TelnetParams,
    'tracert': T_TracertParams,
}

t_dns_result = Table('tb_task_dns', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_DnsResult(DeclarativeBasePbnet):
    __table__ = t_dns_result

t_download_result = Table('tb_task_download', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_DownloadResult(DeclarativeBasePbnet):
    __table__ = t_download_result

t_page_result = Table('tb_task_page', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_PageResult(DeclarativeBasePbnet):
    __table__ = t_page_result

t_ping_result = Table('tb_task_ping', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_PingResult(DeclarativeBasePbnet):
    __table__ = t_ping_result

t_telnet_result = Table('tb_task_telnet', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_TelnetResult(DeclarativeBasePbnet):
    __table__ = t_telnet_result

t_tracert_result = Table('tb_task_tracert', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_TracertResult(DeclarativeBasePbnet):
    __table__ = t_tracert_result

t_result_dict = {
    'dns': t_dns_result,
    'download': t_download_result,
    'page': t_page_result,
    'ping': t_ping_result,
    'telnet': t_telnet_result,
    'tracert': t_tracert_result,
}

T_Result_Dict = {
    'dns': T_DnsResult,
    'download': T_DownloadResult,
    'page': T_PageResult,
    'ping': T_PingResult,
    'telnet': T_TelnetResult,
    'tracert': T_TracertResult,
}

t_alarm = Table('tb_alarm', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_Alarm(DeclarativeBasePbnet):
    __table__ = t_alarm

t_alarm_task = Table('tb_alarm_task', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_AlarmTask(DeclarativeBasePbnet):
    __table__ = t_alarm_task

t_job = Table('tb_job', metadata_pbnet, autoload=True)

t_fault = Table('tb_fault', metadata_pbnet, autoload=True)
t_symptom = Table('tb_symptom', metadata_pbnet, autoload=True)
t_fault_solution = Table('tb_fault_solution', metadata_pbnet, autoload=True)

# --------探针模块------------
t_prober = Table('tb_prober', metadata_pbnet, autoload=True, schema=engine_pbnet.url.database)
class T_Prober(DeclarativeBasePbnet):
    __table__ = t_prober

t_mem_prober = Table('tb_mem_prober', metadata_mem, autoload=True, schema=engine_mem.url.database)
class T_MemProber(DeclarativeBaseMem):
    __table__ = t_mem_prober

t_monitor = Table('prober_monitor', metadata_web, autoload=True, schema=engine_web.url.database)
class T_Monitor(DeclarativeBaseWeb):
    __table__ = t_monitor

t_monitor_users = Table('prober_monitor_users', metadata_web, autoload=True, schema=engine_web.url.database)
class T_MonitorUser(DeclarativeBaseWeb):
    __table__ = t_monitor_users

t_region = Table('prober_region', metadata_web, autoload=True, schema=engine_web.url.database)
class T_Region(DeclarativeBaseWeb):
    __table__ = t_region

    @property
    def tree_node(self):
        node = {'id': self.sid, 'text': self.name_cn, 'rdn': self.rdn}
        if self.level == 0:
            node['state'] = 'open'
        elif self.level == 3:
            session = DBSessionWeb()
            if session.query(T_Community).filter(T_Community.parent_id == self.sid).first():
                node['state'] = 'closed'
        else:
            node['state'] = 'closed'
        return node

t_community = Table('prober_community', metadata_web, autoload=True, schema=engine_web.url.database)
class T_Community(DeclarativeBaseWeb):
    __table__ = t_community

    @property
    def tree_node(self):
        return {'id': 'comm-' + str(self.sid), 'text': self.name_cn}

t_organization = Table('auth_organization', metadata_web, autoload=True, schema=engine_web.url.database)
class T_Organization(DeclarativeBaseWeb):
    __table__ = t_organization


#------------即时测试--------------------
t_dns_imm_result = Table('tb_imm_dns_task', metadata_web, autoload=True, schema=engine_web.url.database)
class T_DnsImmResult(DeclarativeBaseWeb):
    __table__ = t_dns_imm_result

t_download_imm_result = Table('tb_imm_download_task', metadata_web, autoload=True, schema=engine_web.url.database)
class T_DownloadImmResult(DeclarativeBaseWeb):
    __table__ = t_download_imm_result

t_page_imm_result = Table('tb_imm_page_task', metadata_web, autoload=True, schema=engine_web.url.database)
class T_PageImmResult(DeclarativeBaseWeb):
    __table__ = t_page_imm_result

t_ping_imm_result = Table('tb_imm_ping_task', metadata_web, autoload=True, schema=engine_web.url.database)
class T_PingImmResult(DeclarativeBaseWeb):
    __table__ = t_ping_imm_result

t_telnet_imm_result = Table('tb_imm_telnet_task', metadata_web, autoload=True, schema=engine_web.url.database)
class T_TelnetImmResult(DeclarativeBaseWeb):
    __table__ = t_telnet_imm_result

t_tracert_imm_result = Table('tb_imm_tracert_task', metadata_web, autoload=True, schema=engine_web.url.database)
class T_TracertImmResult(DeclarativeBaseWeb):
    __table__ = t_tracert_imm_result

t_dns_imm_job = Table('tb_imm_dns_job', metadata_web, autoload=True, schema=engine_web.url.database)
class T_DnsImmJob(DeclarativeBaseWeb):
    __table__ = t_dns_imm_result

t_telnet_imm_job = Table('tb_imm_telnet_job', metadata_web, autoload=True, schema=engine_web.url.database)
class T_TelnetImmJob(DeclarativeBaseWeb):
    __table__ = t_telnet_imm_result
    
t_page_imm_job = Table('tb_imm_page_job', metadata_web, autoload=True, schema=engine_web.url.database)
class T_PageImmJob(DeclarativeBaseWeb):
    __table__ = t_page_imm_result

t_download_imm_job = Table('tb_imm_download_job', metadata_web, autoload=True, schema=engine_web.url.database)
class T_DownloadImmJob(DeclarativeBaseWeb):
    __table__ = t_download_imm_result    
    
t_ping_imm_job = Table('tb_imm_ping_job', metadata_web, autoload=True, schema=engine_web.url.database)
class T_PingImmJob(DeclarativeBaseWeb):
    __table__ = t_ping_imm_job
    
t_tracert_imm_job = Table('tb_imm_tracert_job', metadata_web, autoload=True, schema=engine_web.url.database)
class T_TracertImmJob(DeclarativeBaseWeb):
    __table__ = t_tracert_imm_job
    
t_imm_plan = Table('tb_imm_job', metadata_web, autoload=True, schema=engine_web.url.database)
class T_ImmPlan(DeclarativeBaseWeb):
    __table__ = t_imm_plan

t_imm_result_dict = {
    'dns': t_dns_imm_result,
    'download': t_download_imm_result,
    'page': t_page_imm_result,
    'ping': t_ping_imm_result,
    'telnet': t_telnet_imm_result,
    'tracert': t_tracert_imm_result,
}

T_Imm_Result_Dict = {
    'dns': T_DnsImmResult,
    'download': T_DownloadImmResult,
    'page': T_PageImmResult,
    'ping': T_PingImmResult,
    'telnet': T_TelnetImmResult,
    'tracert': T_TracertImmResult,
}

T_Imm_Job_Dict = {
    'dns': T_DnsImmJob,
    'download': T_DownloadImmJob,
    'page': T_PageImmJob,
    'ping': T_PingImmJob,
    'telnet': T_TelnetImmJob,
    'tracert': T_TracertImmJob,
}

# ------------------------------测试--------------------------------------------
if __name__ == '__main__':
    from com.mylib.myalchemy import engine_web, t_group

    # 插入单条记录(方法一)
    #ins = t_group.insert().values(name='jack')
    #engine_web.execute(ins)

    # 插入单条记录(方法二)
    #ins = t_group.insert()
    #engine_web.execute(ins, name='jack2')

    # 插入多条记录
    #engine_web.execute(t_group.insert(), [
    #    {'name': 'jack3'},
    #    {'name': 'jack4'},
    #])

    # 查询所有记录，execute后返回ResultProxy对象，支持fetchone、fetchmany、fetchall操作
    from sqlalchemy.sql import select
    s = select([t_group])
    result = engine_web.execute(s)
    for row in result:
        print row

