# -*- coding: utf-8 -*-
from django.db import models,connection,connections
from django.core.cache import cache
from InternetQOEmonitorSystemFront.settings import CACHE_PREFIX
import hashlib
from InternetQOEmonitorSystemFront.base import dictfetchall
#import thread
import threading

class Sequence(models.Model):#唯一序列号
    name=models.CharField(primary_key=True,max_length=128,unique=True,verbose_name='名称')
    seq=models.BigIntegerField(default=0,db_column='val',verbose_name='值')
    @staticmethod
    def get_seq(name):
        #todo FOR UPDATE
        maxItem = Sequence.objects.get_or_create(name=name)[0]
        maxItem.seq=maxItem.seq+1
        maxItem.save()
        return maxItem.seq
    class Meta:
        db_table='tb_seq'
        db_connection='backend'
        #db_for_read='backend'
        
class File(models.Model):
    '''附件存于templates\file文件夹中,在数据库中保存其地址'''
    file = models.FileField(upload_to='auto',null=True)
    note = models.CharField(max_length=255,verbose_name='目标',null=True)
    name = models.CharField(max_length=255,verbose_name='文件名',null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=0,verbose_name='状态',help_text='1')
    class Meta:
        db_table= 'site_file'
        db_connection='backend'
        mysql_engine='InnoDB'        

def get_key_list(model):
    return cache.get(CACHE_PREFIX+'_'+model.__name__,set([]))
class CacheObj(object):
    @classmethod    
    def get_model_key(model_class):
        return CACHE_PREFIX+'_'+model_class.__name__
    @property
    def model_key(self):
        return self.__class__.get_model_key()
    @classmethod
    def clear_cache(model_class):
        for i in model_class.get_cache_keys_list():
            cache.set(i,None)
        cache.set(model_class.get_model_key(),[])
    @classmethod    
    def get_cache_model(model_class,key):
        newKey=model_class.get_model_key()+'_'+hashlib.md5(str(key)).hexdigest()[0:32]
        return cache.get(newKey,None)
        #return CACHE_PREFIX+'_'+model_class.__name__
    def add_to_cache(self,key):
        keyList=get_key_list(self.__class__)
        newKey=self.model_key+'_'+hashlib.md5(str(key)).hexdigest()[0:32]
        keyList.add(newKey)        
        cache.set(newKey,self)
        cache.set(self.model_key,keyList)
    def update_cache(self,key):
        newKey=self.model_key+'_'+hashlib.md5(str(key)).hexdigest()[0:32]
        cache.set(newKey,self)

def get_isplist_bak(ip_list):
    #ip_list可能重复，应该先去重，再进行查询
    #可以用memcache进行保存
    if not ip_list:return []
    query_ip_list=list(set(ip_list))
    #一次最多只允许查询500个IP
    r=0
    query_ip_lists=[]
    l=len(query_ip_list)
    onePageLen=300
    while True:
        query_ip_lists.append(query_ip_list[r*onePageLen:(r+1)*onePageLen])
        if r*onePageLen>l:break
        r+=1
    oDict={}
    for qList in query_ip_lists:
        oDict.update(get_ispdict(qList,None))
    return [oDict[item] for item in ip_list]

def get_ispdict(query_ip_list,cursor):
    cursor=connections['mem'].cursor()
    ips=';'.join(query_ip_list)+';'
    cursor.execute(r'call ip_info("'+ips+r'")');
    result= dictfetchall(cursor)
    oriisplist=result[0]['info'].split(';')
    ori_ip_isp_dict=dict([(query_ip_list[i],oriisplist[i]) for i in range(0,len(query_ip_list))])
    return ori_ip_isp_dict

def get_isplist(ip_list):
    #ip_list可能重复，应该先去重，再进行查询
    #可以用memcache进行保存
    if not ip_list:return []
    query_ip_list=[ip for ip in set(ip_list) if ip]
    #一次最多只允许查询500个IP
    r=0
    query_ip_lists=[]
    l=len(query_ip_list)
    onePageLen=300
    while True:
        if r*onePageLen>=l:break
        query_ip_lists.append(query_ip_list[r*onePageLen:(r+1)*onePageLen])
        r+=1
    oDict={}
    ispGetterList=[]
    for qList in query_ip_lists:
        ispGetter = ISPGetter(qList)
        ispGetterList.append(ispGetter)
        ispGetter.start()
    for i in ispGetterList:
        i.join()
    for i in ispGetterList:
        oDict.update(i.result)
    return [oDict.get(item) for item in ip_list]

class ISPGetter(threading.Thread): 
    #使用多线程来提高获取isp的速度
    def __init__(self, query_ip_list):
        threading.Thread.__init__(self)
        self.query_ip_list=query_ip_list
        self.result = {}
        
    def run(self): #Overwrite run() method, put what you want the thread do here  
        cursor=connections['mem'].cursor()
        ips=';'.join(self.query_ip_list)
        cursor.execute(r'call ip_info("'+ips+r'")');
        result= dictfetchall(cursor)
        oriisplist=result[0]['info'].split(';')
        if len(oriisplist) != len(self.query_ip_list):
            raise Exception(u'调用call ip_info返回isp数量与ip数量不一致')
        else:
            self.result=dict([(self.query_ip_list[i],oriisplist[i]) for i in range(0,len(self.query_ip_list))])

def set_isp(model_list,ipattrname='ip',ispattrname='isp'):
    query_ips=[]
    for model in model_list:
        query_ips.append(getattr(model,ipattrname))
    isplist=get_isplist(query_ips)
    for i in range(0,len(model_list)):
        setattr(model_list[i],ispattrname,isplist[i])