# -*- encoding: utf-8 -*-

def connect_where_sql(search_keys, db_keys = [], replace_key = {}, skip_keys = []):
    sql_where = ''
    for skip_key in skip_keys:
        search_keys.pop(skip_key)
    value_list = []
    for key, value in search_keys.iteritems():
        if not value:
            continue
        if db_keys and key not in db_keys:
            continue
        if replace_key.get(key, None):  key = replace_key[key]
        sql_where += ' AND ' + key + '= %s '
        value_list.append(value)
    return sql_where, value_list

def  major_connect_where_sql(search_keys, db_keys = [], replace_key = {}, skip_keys = []):
    '''
    升级的connect_where_sql，涵盖上述所有功能，且增加对in的支持，通过（__in）实现，因担心无测试引起其它问题未直接替换方法。
    #todo.Bruce 该方法将使得索引失效(升级的connect_where_sql方法也一样)，高性能要求下不宜使用。按索引来排布查询条件的顺序更为合理。
    '''
    sql_where = ''
    in_keys = {}
    for skip_key in skip_keys:
        search_keys.pop(skip_key)
    for key in search_keys:
        if key.endswith('__in'):
            #in_keys.append(key)
            in_keys[key] = search_keys[key]
    for key in in_keys:
        search_keys.pop(key)
    value_list = []
    for key, value in search_keys.iteritems():
        if not value:
            continue
        if db_keys and key not in db_keys:
            continue
        if replace_key.get(key, None):  key = replace_key[key]
        sql_where += ' AND ' + key + '= %s '
        value_list.append(value)
    for key in in_keys:
        if not  in_keys[key] or not type(in_keys[key]) == list:
            raise '__in must match a value list'  
        sql_where += ' AND ' + key.replace('__in','') + ' in (' + ','.join(['%s']*len(in_keys[key])) +')'
        value_list.extend(in_keys[key])
    return sql_where, value_list

def insert_key_sql(db_name, params, db_keys = []):
    insert_keys = []
    values_s = []
    insert_values = []
    for key, values in params.iteritems():
        if db_keys and key not in db_keys:
            continue
        insert_keys.append(key)
        values_s.append('%s')
        insert_values.append(values)
    insert_sql = ''' INSERT INTO ''' + db_name + '''( ''' + ",".join([str(e) for e in insert_keys]) + ''') VALUES ( ''' + ','.join([str(e) for e in values_s]) + ')'
    return insert_sql, insert_values

def update_key_sql(db_name, params, db_keys = []):
    update_sql = []
    sql_value = []
    update_values = []
    for key, values in params.iteritems():
        if db_keys and key not in db_keys:
            continue
        update_sql.append(key)
        sql_value.append(key + ''' =%s ''')
        update_values.append(values)
    update_sql = ''' UPDATE ''' + db_name + ''' SET ''' + ",".join([str(e) for e in sql_value])
    return update_sql, update_values

def dictfetchall(cursor):
    #基本的数据读取方法，将获得数据组织为字典。
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]