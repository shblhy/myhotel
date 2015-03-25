# -*- encoding: utf-8 -*-
import datetime
import logging
import logging.handlers
import time

from MySQLdb import ProgrammingError, DatabaseError
from MySQLdb import OperationalError, IntegrityError

from wiwidebd.libs.facility import initializer
from wiwidebd.libs.facility import category

DATABASE_ERROR = (IntegrityError, OperationalError, ProgrammingError,
                DatabaseError)
LOG_FILE = 'update.log'


def getlogger():
    handler = logging.handlers.RotatingFileHandler(LOG_FILE,
                                                   maxBytes=10*1024*1024,
                                                   backupCount=5)
    fmt = '%(asctime)s-%(filename)s:%(lineno)s-%(name)s-%(message)s'

    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger('update')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def try_except(func):

    def wrapper(*args, **kwargs):
        try:
            message = "ok"
            status = 0
            result = func(*args, **kwargs)
        except DATABASE_ERROR as ex:
            status = -1
            message = " %s ." % ex
            result = ""
        result_data = {
            "status": status, "message": message,
            "result": result
        }
        return result_data

    return wrapper


def get_city_dict():
    '''
    sql = 'select District, DistrictID, ParentID  from entity_city_info
    where ParentID in (
    select ParentID from entity_city_info order by ParentID);
    '
    return city_dict_list = {
            "北京": {"ProvinceID": "1", "东城": "36", "西城": "37", "朝阳": "38"},
            "上海": {"ProvinceID": "2", }
    }'''

    pro_sql = 'select District, DistrictID from entity_city_info where ParentID=0;'
    conn = initializer.create_local_mysql()
    cursor = conn.cursor()
    cursor.execute(pro_sql)
    provinces = cursor.fetchall()
    pros = {}
    for pro in provinces:
        province = pro["District"].encode('utf-8') if isinstance(pro["District"], unicode) else pro["District"]
        pros[province] = int(pro["DistrictID"])

    for k, v in pros.iteritems():
        sql = 'select DistrictID, District from entity_city_info where ParentID=%d;' % v
        cursor.execute(sql)
        citys = cursor.fetchall()
        if not citys:
            continue
        pros[k] = {"ProvinceID": v}
        for city in citys:
            cy = city["District"].encode('utf-8') if isinstance(city["District"], unicode) else city["District"]
            pros[k][cy] = int(city["DistrictID"])
    cursor.close()
    conn.close()
    return pros


def get_user_list(tmp_str):
    '''根据传入的str，返回模糊查询到的前十个user中英文名字'''
    conn = None
    result_list = []
    tmp_str = tmp_str.replace('"', '\\"')
    if tmp_str.__contains__(';'):raise Exception('不应该包含;')
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        sql_str = '''SELECT id user_id,username,first_name FROM auth_user
            WHERE username like "%%%s%%" OR first_name like "%%%s%%" ORDER BY first_name DESC LIMIT 10''' %(tmp_str, tmp_str)
        #TODO.Dangerous bruce 有SQL注入风险，加了
        cursor.execute(sql_str)
        r = cursor.fetchall()
        for e in r:
            result_list.append((e["user_id"], e["username"], e["first_name"]))
        conn.commit()
        cursor.close()
    finally:
        if conn != None:
            conn.close()
    return result_list


def get_brand_list(tmp_str, only_cn=False):
    '''根据传入的str，返回模糊查询到的前十个品牌名称'''
    conn = None
    result_list = []
    tmp_str = tmp_str.replace('"', '\\"')
    if tmp_str.__contains__(';'):raise Exception('不应该包含;')
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        sql_str = '''SELECT BrandID,ChineseName,EnglishName FROM entity_brand_info
            WHERE ChineseName like "%%%s%%" or EnglishName like "%%%s%%" ORDER BY EnglishName DESC LIMIT 10''' %(tmp_str, tmp_str)
        #确定传入的查询字段为中文名称
        if only_cn:
            sql_str = '''SELECT BrandID,ChineseName,EnglishName FROM entity_brand_info
            WHERE ChineseName like "%%%s%%"''' %tmp_str
        #TODO.Dangerous bruce 粗看有SQL注入风险，待查  加了Exception('不应该包含;')
        cursor.execute(sql_str)
        r = cursor.fetchall()
        for e in r:
            result_list.append((e["BrandID"], e["ChineseName"], e["EnglishName"] if e["EnglishName"]<>None else ''))
        conn.commit()
        cursor.close()
    finally:
        if conn != None:
            conn.close()
    return result_list

def get_store_list(tmp_str,brand_id=None):
    '''根据传入的str，返回模糊查询到的前十个店面名称
        第二关键字other_key为品牌名称,other_key为空,检索所有店铺名;否则检索相关品牌下店铺
    '''
    conn = None
    tmp_str = tmp_str.replace('"', '\\"')
    if tmp_str.__contains__(';'):raise Exception('不应该包含;')
    result_list = []
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        if brand_id:
            sql_str = '''SELECT StoreID,StoreName FROM entity_store_info
                WHERE StoreName like "%%%s%%" AND ReferBrandID="%s" ORDER BY StoreName DESC LIMIT 10''' %(tmp_str, brand_id)
        else:
            sql_str = '''SELECT StoreID,StoreName FROM entity_store_info
                WHERE StoreName like "%%%s%%" ORDER BY StoreName DESC LIMIT 10''' %(tmp_str)
        #TODO.Dangerous bruce 粗看有SQL注入风险，待查  加了Exception('不应该包含;')
        cursor.execute(sql_str)
        r = cursor.fetchall()
        for e in r:
            result_list.append((e["StoreID"], e["StoreName"]))
        conn.commit()
        cursor.close()
    finally:
        if conn != None:
            conn.close()
    return result_list


def get_brand_id(brand_name, type=None):
    '''根据传入的brand_name，返回对应的品牌id
        type="chinese",传入品牌中文名;
        type="english",传入品牌英文名;
        type="mixture",传入品牌中英文名;
    '''
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        if type == "chinese":
            sql_str = '''SELECT BrandID FROM entity_brand_info WHERE ChineseName=%s'''
            cursor.execute(sql_str, (brand_name, ))
        elif type == "english":
            sql_str = '''SELECT BrandID FROM entity_brand_info WHERE EnglishName=%s'''
            cursor.execute(sql_str, (brand_name, ))
        elif type == "mixture":
            if brand_name.find("/") < 0: return None
            chi_name, eng_name = brand_name.rsplit("/", 1)
            sql_str = '''SELECT BrandID FROM entity_brand_info WHERE ChineseName=%s OR EnglishName=%s'''
            cursor.execute(sql_str, (chi_name, eng_name, ))
        r = cursor.fetchone()
        brand_id = r["BrandID"]
        conn.commit()
        cursor.close()
    finally:
        if conn != None:
            conn.close()
    return brand_id

def handle_uploaded_file(filefd):
    return filefd.read()


def get_limit_and_offset(page_size, page_num):
    limit = min(page_size, 30)
    offset = (page_num - 1) * limit 
    return (limit, offset)


def get_paging_params(request):
    page_size = int(request.POST.get("page_size", 20))
    page_num = int(request.POST.get("page_num", 1))
    limit, offset = get_limit_and_offset(page_size, page_num)
    return (page_size, page_num, limit, offset)


def get_industry_type(type_name, key):
    return category.value(type_name, key)


def deal_params(detail):
    for key, value in detail.items():
        if value == "" or value == "None" or value == "null" or value == 'NULL':
            detail[key] = None
        if key == 'BrandName':
            detail[key] = value.split("/")[0]


def get_days(old, now):
    '''
    这里可以处理两种类型的时间。
    如字符串："2014-09-22 10:22:34", "2014-09-23 10:22:34" 。返回 1
    如datetime.datetime.now() 即就是datetime.datetime 对象，这样此函数就可以
    处理四种组合类型的时间了。
    '''
    if isinstance(old, basestring):
        date1 = time.strptime(old, "%Y-%m-%d %H:%M:%S")
        date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3],
                                  date1[4], date1[5])
    elif isinstance(old, datetime.datetime):
        date1 = old
    if isinstance(now, basestring):
        date2 = time.strptime(now, "%Y-%m-%d %H:%M:%S")
        date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3],
                                  date2[4], date2[5])
    elif isinstance(now, datetime.datetime):
        date2 = now
    re = date2 - date1
    return re.days
