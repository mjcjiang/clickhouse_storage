#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:39:14 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.WriteUtils as wutils

from DataPlatForm.BasicUtils import *
import DataPlatForm.AccessControl as control
from clickhouse_driver import Client
import os

import grpc
import DataPlatForm.service_pb2 as service_pb2
import DataPlatForm.service_pb2_grpc as service_pb2_grpc

#------------------------------------------------------------------------------
# 二维frame数据写入接口
#------------------------------------------------------------------------------
def write_frame(data, name, date):
    wutils.general_write_raw_data(data, name, date, service_pb2.raw_auth_code, raw_frame_db, wutils.write_raw_data, "frame")
    
#------------------------------------------------------------------------------
# frame数据删除接口
#------------------------------------------------------------------------------
def delete_frame(name, date):
    wutils.general_delete_raw_data(name, service_pb2.raw_auth_code, raw_frame_db, date, wutils.delete_raw_data, "frame")

#------------------------------------------------------------------------------
# 列表数据写入接口
# data: list
# name: 列表名称, raw中所有列表数据存放在一个统一的数据库中，一个name是一张表
#------------------------------------------------------------------------------
def __write_list(data, name):
    client = control.get_session_client()

    #如果list数据库还不存在，创建list数据库
    create_database_query = "CREATE DATABASE IF NOT EXISTS " + raw_list_db
    client.execute(create_database_query)

    #user insert empty data, exist
    if len(data) == 0:
        return

    #如果用户传入的list是一个异质列表（其中有不同类型的元素），报错
    if not is_homogeneous_list(data):
        raise ValueError("Not homogeneous list write(Different data types in list), check your list")
    
    #如果name数据表还不存在，创建之
    column_name = 'value'
    if isinstance(data[0], str):
        column_type = 'String'
    elif isinstance(data[0], int):
        column_type = 'Int64'
    elif isinstance(data[0], float):
        column_type = 'Float64'
    else:
        raise ValueError("data type not String, Int Or Float!")
    
    create_table_query = "CREATE TABLE IF NOT EXISTS " + raw_list_db + "." + name
    create_table_query += " ("
    create_table_query += column_name + " " + column_type
    create_table_query += ") "
    create_table_query += " ENGINE = MergeTree() order by " + column_name
    client.execute(create_table_query)

    #将数据插入到数据表中
    insert_query = "insert into " + raw_list_db + "." + name + " "
    insert_query += "(" + column_name+ ") values "
    data_str = ""
    for x in data:
        data_str += "("
        if type(x) == str:
            data_str += "\'" + x + "\'"
        else:
            data_str += str(x)
        data_str += ")" + ","
    data_str = data_str[0:-1]
    insert_query += data_str
    
    client.execute(insert_query)

#------------------------------------------------------------------------------
# 通过权限校验的列表写入函数
# data: list
# name: 列表名称, raw中所有列表数据存放在一个统一的数据库中，一个name是一张表
#------------------------------------------------------------------------------
def write_list(data, name):
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()

        can_write = False
        
        stamp = get_current_timestamp()
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)

        acl_req = service_pb2.AclRequest(loginfo=loginfo, dataname=name, datacategory=service_pb2.raw_auth_code, operation=2)
        response = stub.CheckAcl(acl_req)
        if response.code == 0:
            can_write = True
        elif response.code == 2:
            datainfo = service_pb2.DataInfo(name=name, category=service_pb2.raw_auth_code, createtime=stamp, description="", remark="")
            data_req = service_pb2.DataRequest(loginfo=loginfo, datainfo=datainfo)
            response = stub.CreateNewData(data_req)

            if response.code == 0:
                can_write = True
            else:
                raise ValueError("Can't write list [%s], %s" % (name, response.detail,))
        else:
            raise ValueError("Can't write list [%s], %s" % (name, response.detail,))

        if can_write:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table

            control.set_user_and_password(db_account, db_password)
            __write_list(data, db_table)
            control.set_user_and_password(old_account, old_password)

#------------------------------------------------------------------------------
# 列表数据删除接口
# name: 列表名称, raw中所有列表数据存放在一个统一的数据库中，一个name是一张表
#------------------------------------------------------------------------------
def __delete_list(name):
    client = control.get_session_client()
    
    if not is_table_exist(client, raw_list_db, name):
        raise ValueError("%s not exist in database[%s]" % (name, raw_list_db))

    delete_query = "drop table " + raw_list_db + "." + name
    client.execute(delete_query)

def delete_list(name):
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()

        #登录信息和权限获取请求
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)
        aclreq = service_pb2.AclRequest(loginfo=loginfo,
                                          dataname=name,
                                          datacategory=service_pb2.raw_auth_code,
                                          operation=2)
        response = stub.CheckAcl(aclreq)
        if response.code == 0:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table

            control.set_user_and_password(db_account, db_password)
            __delete_list(db_table)
            control.set_user_and_password(old_account, old_password)
        else:
            raise ValueError("Can't delete list, %s" % (response.detail,))
