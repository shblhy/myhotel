# -*- encoding: utf-8 -*-
'''
todo.delete
用auth.models.PermissionTree代替
'''
from wiwidebd.libs.facility import initializer

def get_permission_tree():
    '''返回树结构图'''
    # 1.挑选出树
    family_dict = {} # 把父子关系记录下来
    user_cand_list = []
    tag_info_list = []
    tag_user_list = []
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        sql_str = '''SELECT NodeId, ParentId, NodeName FROM auth_permission_tree'''
        cursor.execute(sql_str)
        r = cursor.fetchall()
        for family_one in r:
            if family_one["ParentId"] == None: family_one["ParentId"] = 0
            else: family_dict[family_one["NodeId"]] = family_one["ParentId"]
            tag_info_list.append([family_one["NodeId"], family_one["ParentId"], family_one["NodeName"]])

        # 2.挑选出树的关联
        sql_str = '''
            SELECT ReferUserId, ReferNodeId, first_name, username
            FROM auth_permission_relation INNER JOIN auth_user U ON ReferUserId = U.id
        '''
        cursor.execute(sql_str)
        tagged_user_ids = set([0])  # 默认一个初始值，防止后续sql拼接的错误
        r = cursor.fetchall()
        for tag_user in r:
            tag_user_list.append((tag_user['ReferNodeId'], tag_user['ReferUserId'], tag_user['username'], tag_user['first_name'], False))
            tagged_user_ids.add(tag_user['ReferUserId'])

        # 4.遍历tag_info_list
        sql_str = '''
            SELECT auth_user.id userid, username, first_name FROM auth_user 
            INNER JOIN auth_user_groups ON auth_user_groups.user_id = auth_user.id
            WHERE group_id = 8 AND is_active = 1 AND auth_user.id NOT IN (%s)
        ''' % ",".join([str(e) for e in tagged_user_ids])
        cursor.execute(sql_str)
        r = cursor.fetchall()
        for user_cand in r:
            user_cand_list.append((user_cand["userid"], user_cand["username"], user_cand["first_name"]))
        cursor.close()

    finally:
        if conn != None:
            conn.close()
    result = {
        "tag_info_list" : tag_info_list,
        "tag_user_list" : tag_user_list,
        "user_cand_list" : user_cand_list,
        }
    return result

def add_permission_node(NodeName, ParentId):
    sql_str = '''INSERT INTO auth_permission_tree(NodeName, ParentId) Values(%s, %s) '''
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        cursor.execute(sql_str, (NodeName, ParentId))
        new_tag_id = cursor.lastrowid
        cursor.close()
        conn.commit()
    finally:
        if conn != None:
            conn.close()

    return new_tag_id

def upt_relation_ajax(parent_id, node_id, user_id, prev_parent_id):
    result = {"message": "false", "status": 1}
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        if node_id:
            sql_str = '''
                UPDATE auth_permission_tree SET ParentId = %s
                WHERE NodeId = %s
            '''
            cursor.execute(sql_str, (parent_id, node_id))
        if user_id:
            sql_str = '''
                UPDATE auth_permission_relation SET ReferNodeId = %s
                WHERE ReferNodeId = %s AND ReferUserId = %s
            '''
            cursor.execute(sql_str, (parent_id, prev_parent_id, user_id))
        cursor.close()
        conn.commit()
        result = {"message": "ok", "status": 0}
    finally:
        if conn != None:
            conn.close()

    return result

def upt_tag(node_id, node_name):
    result = {"message": "false", "status": 1}
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        sql_str = '''
            UPDATE auth_permission_tree SET NodeName = %s
                WHERE NodeId = %s
            '''
        cursor.execute(sql_str, (node_name, node_id))
        cursor.close()
        conn.commit()
        result = {"message": "ok", "status": 0}
    finally:
        if conn != None:
            conn.close()

    return result

def add_relation(node_id, user_id):
    result = {"message": "false", "status": 1}
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        sql_str = '''
            INSERT INTO auth_permission_relation (ReferNodeId, ReferUserId)
                VALUES (%s, %s)
        '''
        cursor.execute(sql_str, (node_id, user_id))
        cursor.close()
        conn.commit()
        result = {"message": "ok", "status": 0}
    finally:
        if conn != None:
            conn.close()

    return result

def del_relation(node_id, user_id):
    result = {"message": "false", "status": 1}
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        sql_str = '''
            DELETE FROM auth_permission_relation
        WHERE ReferNodeId = %s AND ReferUserId = %s
        '''
        cursor.execute(sql_str, (node_id, user_id))
        cursor.close()
        conn.commit()
        result = {"message": "ok", "status": 0}
    finally:
        if conn != None:
            conn.close()

    return result

def del_tag(node_id):
    result = {"message": "false", "status": 1}
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        sql_str = '''
            DELETE FROM auth_permission_tree WHERE NodeId = %s
        '''
        cursor.execute(sql_str, (node_id, ))
        cursor.close()
        conn.commit()
        result = {"message": "ok", "status": 0}
    finally:
        if conn != None:
            conn.close()

    return result


def find_subordinates(current_id, include_me = True, include_public = True):
    child_users = []
    all_nodes = []
    current_node = 16
    sql_str_node = '''SELECT NodeId, ParentId, ReferUserId FROM auth_permission_tree T
                        INNER JOIN auth_permission_relation R ON R.ReferNodeId=T.NodeId
                 '''
    conn = None
    try:
        conn = initializer.create_local_mysql()
        cursor = conn.cursor()
        cursor.execute(sql_str_node)
        r = cursor.fetchall()
        for node_detail in r:
            if node_detail["ReferUserId"] == current_id: current_node = node_detail["NodeId"]
            all_nodes.append((node_detail["NodeId"], node_detail["ParentId"]))
        child_nodes = find_child_id(all_nodes, current_node)
        if child_nodes:
            sql_str_child = '''SELECT ReferNodeId, ReferUserId FROM auth_permission_relation WHERE ReferNodeId in (%s);'''% ','.join([str(e) for e in child_nodes])
            cursor.execute(sql_str_child)
            r = cursor.fetchall()
            for child_one in r:
                child_users.append(child_one["ReferUserId"])
        cursor.close()
    finally:
        if conn != None:
            conn.close()

    if include_me: child_users.append(current_id)
    if include_public: child_users.append(16)
    return child_users

def find_child_id(all_users, current_id, child_users = []):
    if isinstance(current_id, long) or isinstance(current_id, int):
        current_id = [current_id, ]
    new_list = []
    while current_id:
        temp_id = current_id.pop(0)
        for user_id, parent_id in all_users:
            if parent_id == temp_id:
                child_users.append(user_id)
                new_list.append(user_id)
                find_child_id(all_users, new_list, child_users)
    return child_users
