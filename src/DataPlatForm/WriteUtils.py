#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:39:14 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
from DataPlatForm.BasicUtils import *
import DataPlatForm.AccessControl as control
from DataPlatForm.ReadUtils import get_factor_columns

from clickhouse_driver import Client
from datetime import datetime

import numpy as np
import pandas as pd
import os

import grpc
import DataPlatForm.service_pb2 as service_pb2
import DataPlatForm.service_pb2_grpc as service_pb2_grpc

#------------------------------------------------------------------------------
# write_raw_data: 基础的写入raw数据函数
#------------------------------------------------------------------------------
def write_raw_data(data, database, name, date):
    client = control.get_session_client()
    
    if not check_date_string(date):
        raise ValueError("%s not valid(e.g 2005-01-04)" % date)

    #如果二维数据库不存在，创建之
    client.execute("create database if not exists %s" % (database))
    
    table_name = name + "_" + trans_date_string(date)
    #表已经存在，直接退出
    if is_table_exist(client, database, table_name):
        print("[WARN]: %s table alreay exists in database[%s], you can delete it and then wirte!" % (table_name, database))
        return

    #创建一个新的数据表
    create_table_query = "create table if not exists " + database + "." + table_name + " ("
    create_table_query += gen_table_fields_infos_from_dataframe(data) + ") "
    create_table_query += "ENGINE = MergeTree() order by " + "indexer"
    client.execute(create_table_query)
    
    #将frame中的数据插入到新创建的表中
    columns_str = gen_columns_str_from_dataframe(data)
    data_str = para_gen_data_insert_str(data)
    
    insert_query = "insert into " + database + "." + table_name + " " + columns_str + " " + "values " + data_str
    client.execute(insert_query)

#------------------------------------------------------------------------------
# 通用的权限校验写入raw数据的函数
#-----------------------------------------------------------------------------
def general_write_raw_data(data, name, date, category, database, write_func, comment):
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()

        stamp = get_current_timestamp()
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)
        can_write = False

        #权限服务平台只存通用表名
        acl_req = service_pb2.AclRequest(loginfo=loginfo, dataname=name, datacategory=category, operation=2)
        response = stub.CheckAcl(acl_req)
        
        if response.code == 0:
            can_write = True
        elif response.code == 2:
            datainfo = service_pb2.DataInfo(name=name, category=category, createtime=stamp, description="", remark="")
            data_req = service_pb2.DataRequest(loginfo=loginfo, datainfo=datainfo)
            response = stub.CreateNewData(data_req)

            if response.code == 0:
                can_write = True
            else:
                raise ValueError("Can't write %s[%s], %s" % (comment, name, response.detail,))
        else:
            raise ValueError("Can't write %s[%s], %s" % (comment, name, response.detail,))

        if can_write:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table
                
            control.set_user_and_password(db_account, db_password)
            write_func(data, database, db_table, date)
            control.set_user_and_password(old_account, old_password)

#------------------------------------------------------------------------------
# raw数据基本删除函数
#------------------------------------------------------------------------------
def delete_raw_data(name, database, date):
    client = control.get_session_client()

    if not check_date_string(date):
        raise ValueError("%s not valid(e.g 2005-01-04)" % date)

    table_name = name + "_" + trans_date_string(date)

    if not is_table_exist(client, database, table_name):
        raise ValueError("%s table not in database[%s], can not be deleted!" % (table_name, database))

    delete_query = "drop table " + database + "." + table_name
    client.execute(delete_query)
        
#------------------------------------------------------------------------------
# 通用的通过权限校验接口的raw数据删除函数
#------------------------------------------------------------------------------
def general_delete_raw_data(name, category, database, date, delete_func, comment):
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()

        #登录信息和权限获取请求
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)
        aclreq = service_pb2.AclRequest(loginfo=loginfo,
                                          dataname=name,
                                          datacategory=category,
                                          operation=2)
        response = stub.CheckAcl(aclreq)
        if response.code == 0:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table

            control.set_user_and_password(db_account, db_password)
            delete_func(db_table, database, date)
            control.set_user_and_password(old_account, old_password)
        else:
            raise ValueError("Can't delete %s, %s" % (comment, response.detail,))

#------------------------------------------------------------------------------
# 根据用户dataframe中的股票列表，生成clickhouse表中的股票列名
# (test_passed)
#------------------------------------------------------------------------------
def __gen_table_symbols_list(symbols):
    res = ''
    if len(symbols) == 0:
        return res

    for i in range(len(symbols) - 1):
        res += 'S' + symbols[i] + ' Float64,'
    res += 'S' + symbols[len(symbols) - 1] + ' Float64'

    return res

#------------------------------------------------------------------------------
# 创建因子数据表
# (test_passed)
#------------------------------------------------------------------------------
def __create_table(client, database_name, table_name, symbols):
    client.execute("create database if not exists %s" % (database_name))
    
    #表名命名规则，用户名 ＋ 用户输入的表名
    table_create_query = "create table if not exists " + database_name + "." + table_name + "("
    table_create_query += " timestamp FixedString(" + str(factor_timestamp_size) + "),"
    table_create_query += __gen_table_symbols_list(symbols) + ")"
    table_create_query += " ENGINE = MergeTree() PRIMARY KEY(timestamp) order by timestamp"

    curr_user = control.get_user()
    curr_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    table_create_query += " COMMENT " + "\'" + curr_user + ";" + curr_date + "\'"
    client.execute(table_create_query)

#------------------------------------------------------------------------------
# 创建插入语句中列名序列
#------------------------------------------------------------------------------
def __gen_columns_str(symbols):
    res = "(timestamp,"
    for symbol in symbols:
        res += "S" + symbol + ","
    res = res[0:-1]
    res += ")"
    return res

#------------------------------------------------------------------------------
# 写入因子数据到clickhouse数据库中
# 使用请注意：正常的使用场景是，先创建好一张大表，然后再向其中每次更新少量数据
#           如果用户反过来使用，每次更新大量的数据，且存在大量的新列，将导致写入时间大大延长
#------------------------------------------------------------------------------
def write_factor_data(data, database, name):
    client = control.get_session_client()
    user_symbols = [x.replace(".", "") for x in list(data.index.values)]   #000001.SH转化成000001SH
    table_name = gen_real_table_name(name)

    #数据库不存在，创建之
    client.execute("create database if not exists %s" % (database))
    
    #数据属于一个全新的因子，那么先在因子数据库中创建一张表,随后直接将传入的数据写入到表中
    #这种情况下，不存在 "数据" 和 "表" 列数不一致的情况
    if not is_table_exist(client, database, table_name):
        __create_table(client, database, table_name, user_symbols)

        columns_str = __gen_columns_str(user_symbols)                 #生成列名串
        data_str = para_gen_data_insert_column_str(data)              #生成数据串
        insert_query = "insert into " + database + "." + table_name + " "
        insert_query += columns_str + " values " + data_str           #插入语句
        
        client.execute(insert_query)
        return

    #比较 "用户传入数据中的股票列表" 和 "表中现有的股票列表"
    # "传入的股票列表" 有 不在表中存在的股票, 那么要扩展表列
    table_symbols = get_factor_columns(name, database)
    table_symbols = [x.replace(".", "") for x in table_symbols]
    diff_symbols = list(set(user_symbols) - set(table_symbols))
    diff_symbols.sort()

    #如果新写入的数据有新的列，扩展数据表
    if len(diff_symbols) != 0:
        add_column_query = "alter table " + database + "." + table_name
        for symbol in diff_symbols:
            add_column_query += " add column " + "S" + symbol + " Float64" + ","
        add_column_query = add_column_query[0:-1]
        client.execute(add_column_query)

    #将用户传入的数据写入表中（不改变原来的数据，只是增加新的数据）
    user_dates = list(data.columns)
    user_dates.sort()

    #提取已经存在的所有行的时间戳列表
    table_dates = get_all_row_timestamps(client, database, table_name)

    #如果用户输入的日期已经存在，不写入该日期的数据
    valid_dates = list(set(user_dates) - set(table_dates))
    if len(valid_dates) == 0:
        return

    #截取有效写入数据
    valid_data = data[valid_dates]
    
    columns_str = __gen_columns_str(user_symbols)                       #生成列名串
    data_str = para_gen_data_insert_column_str(valid_data)              #生成数据串
    insert_query = generate_insert_query(database, table_name, columns_str, data_str)
    client.execute(insert_query)

#------------------------------------------------------------------------------
# 通用的通过权限检查的写入普通因子的函数
#------------------------------------------------------------------------------
def general_write_factor_data(data, name, database, category, write_func, comment):
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()
        
        stamp = get_current_timestamp()
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)
        can_write = False 
        
        #判断表是否已经存在，如果不存在，直接创建;如果存在，追加写入
        acl_req = service_pb2.AclRequest(loginfo=loginfo, dataname=name, datacategory=category, operation=2)
        response = stub.CheckAcl(acl_req)
        
        if response.code == 0:
            can_write = True
        elif response.code == 2:
            datainfo = service_pb2.DataInfo(name=name, category=category, createtime=stamp, description="", remark="")
            data_req = service_pb2.DataRequest(loginfo=loginfo, datainfo=datainfo)
            response = stub.CreateNewData(data_req)
            if response.code == 0:
                can_write = True
            else:
                raise ValueError("Can't write %s[%s], %s" % (comment, name, response.detail,))
        else:
            raise ValueError("Can't write %s[%s], %s" % (comment, name, response.detail,))

        if can_write:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table
            
            control.set_user_and_password(db_account, db_password)
            write_func(data, database, db_table)
            control.set_user_and_password(old_account, old_password)

#------------------------------------------------------------------------------
# 通用的通过权限检查的写入高级因子的函数
#------------------------------------------------------------------------------
def general_write_alpha_data(data, name, database, category, author, describes, source, remark, write_func, comment):
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()
        
        stamp = get_current_timestamp()
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)
        can_write = False

        acl_req = service_pb2.FcAclRequest(loginfo=loginfo, factorname=name, factorcategory=category, operation=2)
        response = stub.CheckFcAcl(acl_req)
        
        if response.code == 0:
            can_write = True
        elif response.code == 2:
            factor = service_pb2.Factor(name=name, category=category, author=author, createtime=stamp, description=describes, remark=remark, source=source)
            factor_req = service_pb2.FactorRequest(loginfo = loginfo, factor = factor)
            response = stub.CreateAlphaFactor(factor_req)
            
            if response.code == 0:
                can_write = True
            else:
                raise ValueError("Can't write %s[%s], %s" % (comment, name, response.detail,))
        else:
            raise ValueError("Can't write %s[%s], %s" % (comment, name, response.detail,))

        if can_write:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table
            
            control.set_user_and_password(db_account, db_password)
            write_func(data, database, db_table)
            control.set_user_and_password(old_account, old_password)

#------------------------------------------------------------------------------
# 删除因子表中指定日期之间的数据
#------------------------------------------------------------------------------
def delete_factor_data(name, database, start_date, end_date):
    client = control.get_session_client()
    table_name = gen_real_table_name(name)
    
    delete_query = "alter table " + database + "." + table_name + " delete where " 
    delete_query += "substring(timestamp, 1, 10) >= " + "\'" + start_date + "\'" + " and "
    delete_query += "substring(timestamp, 1, 10) <= " + "\'" + end_date + "\'"
    client.execute(delete_query)

#------------------------------------------------------------------------------
# 通用的数据删除函数
#------------------------------------------------------------------------------
def general_delete_factor_data(name, category, database, start_date, end_date, delete_func, comment):
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()

        #登录信息和权限获取请求
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)
        aclreq = service_pb2.AclRequest(loginfo=loginfo,
                                          dataname=name,
                                          datacategory=category,
                                          operation=2)
        response = stub.CheckAcl(aclreq)
        if response.code == 0:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table

            control.set_user_and_password(db_account, db_password)
            delete_func(db_table, database, start_date, end_date)
            control.set_user_and_password(old_account, old_password)
        else:
            raise ValueError("Can't delete in %s table, %s" % (comment, response.detail,))

#------------------------------------------------------------------------------
# 通用的高阶因子数据删除函数
#------------------------------------------------------------------------------
def general_delete_alpha_data(name, category, database, start_date, end_date, delete_func, comment):
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()

        #登录信息和权限获取请求
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)
        aclreq = service_pb2.FcAclRequest(loginfo=loginfo,
                                          factorname=name,
                                          factorcategory=category,
                                          operation=2)
        response = stub.CheckFcAcl(aclreq)
        if response.code == 0:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table

            control.set_user_and_password(db_account, db_password)
            delete_func(db_table, database, start_date, end_date)
            control.set_user_and_password(old_account, old_password)
        else:
            raise ValueError("Can't delete in %s table, %s" % (comment, response.detail,))
