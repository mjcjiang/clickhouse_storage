#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:38:41 2021
# 存取控制设置模块，供数据库管理员使用
#-------------------------------------------------------------------------------
import DataPlatForm.BasicUtils as utils
from clickhouse_driver import Client
from DataPlatForm.configs import *
import re

#------------------------------------------------------------------------------
# 设置会话使用的账户和密码
#------------------------------------------------------------------------------
def set_user_and_password(user, passwd):
    global local_user
    global local_password
    local_user = user
    local_password = passwd

#------------------------------------------------------------------------------
# 获取会话用户名
#------------------------------------------------------------------------------
def get_user():
    global local_user
    return local_user

#------------------------------------------------------------------------------
# 获取会话用户密码
#------------------------------------------------------------------------------
def get_password():
    global local_password
    return local_password

#------------------------------------------------------------------------------
# 获取一个数据库会话
#------------------------------------------------------------------------------
def get_session_client():
    user_name = get_user()
    user_passwd = get_password()
    client = Client(host=clickhouse_addr, user=user_name, password=user_passwd)
    return client

#-------------------------------------------------------------------------------
# 查看某个用户当前被设置的权限
# 返回值是当前用户role被授予权限的列表关系列表
# ['SELECT', 'raw_2d_database.*']
#-------------------------------------------------------------------------------
def get_user_permissions(user_name):
    client = get_session_client()
    role_name = "role_for_" + user_name
    accesses = client.execute("show access")
    permissions = []
    for access in accesses:
        if "TO " + role_name in access[0]:
            grant_end_index = access[0].find("GRANT") + 6
            to_start_index = access[0].find("TO") - 1
            permission = access[0][grant_end_index:to_start_index]
            permissions.append(tuple(permission.split(" ON ")))
    return permissions

#-------------------------------------------------------------------------------
# 创建新用户
# 如果cloned_user为一个已经存在的合法用户
# 那么新创建的用户和cloned_user保持相同的权限
#-------------------------------------------------------------------------------
def create_user(user_name, password, cloned_user=""):
    client = get_session_client()
    
    #the user is exist, can't create it again!
    if utils.is_user_exist(client, user_name):
        raise ValueError("The user[%s] which you want to create is exist!" % (user_name,))
    
    #just create the new user
    create_user_query = "create user " + user_name
    create_user_query += " IDENTIFIED WITH plaintext_password BY " + "\'" + password + "\'"
    client.execute(create_user_query)

    #create role for this new user
    role_for_user = "role_for_" + user_name
    create_role_query = "create role " + role_for_user
    client.execute(create_role_query)

    #grant role for this new user
    grant_role_query = "GRANT " + role_for_user + " TO " + user_name
    client.execute(grant_role_query)

    #clone the permissions of an existed user for previous created user
    if not cloned_user == "":
        if not is_user_exist(cloned_user):
            raise ValueError("The user[%s] which you want to clone permission is not exist!" % (cloned_user,))

        perm_ships = get_user_permissions(cloned_user)
        for ship in perm_ships:
            perm = ship[0]  #权限
            dest = ship[1]  #目标
            grant_perm_query = "GRANT " + perm + " ON " + dest + " TO " + role_for_user
            client.execute(grant_perm_query)
        
    #grant role to user
    grant_role_to_user = "GRANT " + role_for_user + " TO " + user_name

#-------------------------------------------------------------------------------
# 删除用户(并删除赋予这个用户的role)
#-------------------------------------------------------------------------------
def delete_user(user_name):
    client = get_session_client()
    
    if not utils.is_user_exist(client, user_name):
        raise ValueError("The user[%s] which you want to delete is not exist!" % (user_name,))

    drop_user_query = "DROP USER " + user_name
    client.execute(drop_user_query)

    drop_role_query = "DROP ROLE " + "role_for_" + user_name
    client.execute(drop_role_query)

#-------------------------------------------------------------------------------
# 赋予或收回某用户以权限
#-------------------------------------------------------------------------------
def __grant_or_revoke_permission(user_name, permission, database, table, direction=0):
    client = get_session_client()

    grant_revoke_info = [("GRANT ", " TO "), ("REVOKE ", " FROM ")]
    
    if not utils.is_user_exist(client, user_name):
        raise ValueError("The user[%s] which you want to grant permission is not exist!" % (user_name,))
    
    if not utils.is_database_exist(client, database):
        raise ValueError("The database[%s] which you want to grant permission is not exist!" % (database,))
    
    role_for_user = "role_for_" + user_name
    upcase_permission = permission.upper()


    action = grant_revoke_info[direction][0]
    decorator = grant_revoke_info[direction][1]
    
    #为用户的role赋予整个数据库的权限        
    if table == "" or table == "*":
        grant_query = action + upcase_permission + " ON " + database + ".*" + decorator + role_for_user
        client.execute(grant_query)
        return

    #用户设定数据库中某特定表格的权限
    match = re.search("^([\w-]+)$", table)
    if match:
        grant_query = action + upcase_permission + " ON " + database + "." + table + decorator + role_for_user
        client.execute(grant_query)
        return
    
    #用户设定数据库中通配表格的权限
    match = re.search("^([\w-]+)[*]?$", table)
    if match:
        prefix = match.group(1)
        all_tables = utils.get_all_tables_in_database(client, database)
        #为用户赋予数据库中特定表格的权限
        for table in all_tables:
            if table.startswith(prefix):
                grant_query = action + upcase_permission + " ON " + database + "." + table + decorator + role_for_user
                client.execute(grant_query)

#-------------------------------------------------------------------------------
# 赋予某用户的因子权限
#-------------------------------------------------------------------------------
def grant_factor_permission_to_user(user_name, permission, factor):
    __grant_or_revoke_permission(user_name, permission, factor_db, factor, direction=0)
                
#-------------------------------------------------------------------------------
# 收回某用户的因子权限
#-------------------------------------------------------------------------------
def revoke_factor_permission_from_user(user_name, permission, factor):
    __grant_or_revoke_permission(user_name, permission, factor_db, factor, direction=1)

#-------------------------------------------------------------------------------
# 赋予某用户的二维数据权限
#-------------------------------------------------------------------------------
def grant_2d_permission_to_user(user_name, permission, name):
    __grant_or_revoke_permission(user_name, permission, raw_2d_db, name, direction=0)
                
#-------------------------------------------------------------------------------
# 收回某用户的二维数据权限
#-------------------------------------------------------------------------------
def revoke_2d_permission_from_user(user_name, permission, name):
    __grant_or_revoke_permission(user_name, permission, raw_2d_db, name, direction=1)

#-------------------------------------------------------------------------------
# 赋予某用户的列表数据权限
#-------------------------------------------------------------------------------
def grant_list_permission_to_user(user_name, permission, name):
    __grant_or_revoke_permission(user_name, permission, raw_list_db, name, direction=0)
                
#-------------------------------------------------------------------------------
# 收回某用户的列表数据权限
#-------------------------------------------------------------------------------
def revoke_list_permission_from_user(user_name, permission, list_name):
    __grant_or_revoke_permission(user_name, permission, raw_list_db, list_name, direction=1)
    
#------------------------------------------------------------------------------
# 返回因子数据的创建者
#------------------------------------------------------------------------------
def get_factor_creator(factor):
    client = get_session_client()
    select_query = "SELECT name, comment FROM system.tables WHERE name LIKE "
    select_query += "\'%" + factor + "%\'"
    res = client.execute(select_query)
    return res
