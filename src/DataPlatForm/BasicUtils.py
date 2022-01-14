#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 25 14:18:20 2021
#-------------------------------------------------------------------------------
from clickhouse_driver import Client
from datetime import datetime, timedelta
from multiprocessing import Pool
from DataPlatForm.configs import *

import numpy as np
import pandas as pd
import re

import time
import os

#------------------------------------------------------------------------------
# 判断一个列表是不是同质列表(列表中所有的元素类型都相同)
#------------------------------------------------------------------------------
def is_homogeneous_list(lst):
    if len(lst) == 0:
        return True
    
    return all(isinstance(x, type(lst[0])) for x in lst[1:])

#------------------------------------------------------------------------------
# 获取开始时间到结束时间之间的日期列表
#------------------------------------------------------------------------------
def gen_date_list(start_date, end_date):
    sdate = datetime.strptime(start_date, "%Y-%m-%d")
    edate = datetime.strptime(end_date, "%Y-%m-%d")
    timestamp_list = list(pd.date_range(sdate, edate, freq='d'))
    return [x.date().strftime("%Y-%m-%d") for x in timestamp_list]

#------------------------------------------------------------------------------
# 从2d表中提取indexer之外的属性列表
#------------------------------------------------------------------------------
def get_2d_table_columns_list(client, database, table):
    if is_table_exist(client, database, table):
        desc_query = "desc " + database + "." + table
        desc_res = client.execute(desc_query)
        return [x[0] for x in desc_res[1:]]
    else:
        return []

#------------------------------------------------------------------------------
# 从dataframe构建出 clickhouse表插入字段信息
#------------------------------------------------------------------------------
def gen_columns_str_from_dataframe(frame):
    columns_str = "(" + "indexer,"
    for x in list(frame.columns.values):
        columns_str += x + ","
    columns_str = columns_str[0:-1]
    columns_str += ")"
    return columns_str

#------------------------------------------------------------------------------
# 从dataframe构建出 clickhouse表字段信息
#------------------------------------------------------------------------------
def gen_table_fields_infos_from_dataframe(frame):
    columns = list(frame.columns.values)
    columns_types = [x for x in list(frame.dtypes)]
    
    index_type = str(frame.index.dtype)
    res = list(zip(columns, [str(x) for x in columns_types]))
    res.insert(0, ('indexer', index_type))
    
    table_fields_str = ""
    for x in res:
        field = x[0]
        field_type = x[1]
        if field_type == 'object':
            table_fields_str += str(field) + " " + "String" + ", "
        if "datetime" in field_type:
            table_fields_str += str(field) + " " + "Datetime" + ", "
        if field_type == 'float64':
            table_fields_str += str(field) + " " + "Float64" + ", "
        if field_type == 'float32':
            table_fields_str += str(field) + " " + "Float32" + ", "
        if field_type == 'int64':
            table_fields_str += str(field) + " " + "Int64" + ", "
        if field_type == 'int32':
            table_fields_str += str(field) + " " + "Int32" + ", "
            
    table_fields_str = table_fields_str[0:-2]
    return table_fields_str

#------------------------------------------------------------------------------
# 检验日期字符串是否满足YYYY-MM-DD的形式
#------------------------------------------------------------------------------
def check_date_string(date_str):
    pattern = '^\d{4}-\d{2}-\d{2}$'
    return re.match(pattern, date_str)

def trans_date_string(date_str):
    pattern = '^(\d{4})-(\d{2})-(\d{2})$'
    res = re.search(pattern, date_str)
    return res.group(1) + "_" + res.group(2) + "_" + res.group(3)

def recover_date_string(date_str):
    pattern = '^(\d{4})_(\d{2})_(\d{2})$'
    res = re.search(pattern, date_str)
    return res.group(1) + "-" + res.group(2) + "-" + res.group(3)

#-------------------------------------------------------------------------------
# 查看某个用户是否存在
#-------------------------------------------------------------------------------
def is_user_exist(client, user_name):
    all_users = client.execute("SHOW USERS")
    for u in all_users:
        if u[0] == user_name:
            return True
    return False

#------------------------------------------------------------------------------
# 验证一个数据库是否存在
#------------------------------------------------------------------------------
def is_database_exist(client, database_name):
    res = client.execute("show databases")
    for tp in res:
        if tp[0] == database_name:
            return True
    return False

#------------------------------------------------------------------------------
# 验证某个因子数据表是否存在
# (test_passed)
#------------------------------------------------------------------------------
def is_table_exist(client, database_name, table_name):
    res = False
    show_query = "show tables from " + database_name + " like " + "\'%" + table_name + "%\'"
    res = client.execute(show_query)
    for tp in res:
        if tp[0] == table_name:
            res = True
    return res

#------------------------------------------------------------------------------
# 获取一个数据库中所有table的列表
#------------------------------------------------------------------------------
def get_all_tables_in_database(client, database_name):
    show_query = "show tables from " + database_name
    return [x[0] for x in client.execute(show_query)]

#------------------------------------------------------------------------------
# 验证表中是否已经存在某个日期的数据
# (test_passed)
#------------------------------------------------------------------------------
def is_date_already_exist(client, database_name, table_name, date):
    select_query = "select timestamp from " + database_name + "." + table_name + " where timestamp = " + "\'"+ date + "\'"
    res = client.execute(select_query)
    if len(res) > 0:
        return True
    return False

#------------------------------------------------------------------------------
# 获取因子数据表中第一行的时间戳
#------------------------------------------------------------------------------
def get_first_row_timestamp(client, database, table):
    select_query = "select timestamp from " + database + "." + table
    res = client.execute(select_query)
    timestamps = [x[0] for x in res]

    timestamps.sort()
    if len(timestamps) > 0:
        return timestamps[0]
    else:
        return ""

#------------------------------------------------------------------------------
# 获取因子数据表中最后一行的时间戳
#------------------------------------------------------------------------------
def get_last_row_timestamp(client, database, table):
    select_query = "select timestamp from " + database + "." + table
    res = client.execute(select_query)
    timestamps = [x[0] for x in res]

    timestamps.sort()
    if len(timestamps) > 0:
        return timestamps[-1]
    else:
        return ""

#------------------------------------------------------------------------------
# 获取因子数据表中所有时间戳组成的列表
#------------------------------------------------------------------------------
def get_all_row_timestamps(client, database, table):
    select_query = "select timestamp from " + database + "." + table
    res = client.execute(select_query)
    return [x[0] for x in res]

#------------------------------------------------------------------------------
# 生成clickhouse插入语句
#------------------------------------------------------------------------------
def generate_insert_query(database, table, columns_str, data_str):
    return "insert into " + database + "." + table + " " + columns_str + " values " + data_str

#------------------------------------------------------------------------------
# 检验日期以及日期范围是否有效
#------------------------------------------------------------------------------
def check_date_range(start_date, end_date):
    #检查日期有效性性
    if not check_date_string(start_date):
        raise ValueError("start_date[%s] syntex error! yyyy-mm-dd!" % start_date)

    if not check_date_string(end_date):
        raise ValueError("end_date[%s] syntex error! yyyy-mm-dd!" % end_date)

    if start_date > end_date:
        raise ValueError("start_date[%s] > end_date[%s], error!" % (start_date, end_date))

#------------------------------------------------------------------------------
# 生成测试使用的因子dataframe
#------------------------------------------------------------------------------
def gen_factor_dataframe(symbols, start_date, daynum):
    dt_start = datetime.strptime(start_date, "%Y-%m-%d")
    date_list = []
    for i in range(daynum):
        dt_curr = dt_start + timedelta(days = i)
        date_list.append(dt_curr.strftime("%Y-%m-%d"))
    data = np.random.rand(len(symbols), len(date_list))
    return pd.DataFrame(data, index=symbols, columns=date_list)
    
#------------------------------------------------------------------------------
# 生成随机时间序列frame
#------------------------------------------------------------------------------
def gen_random_frame(columns, start_time, record_num):
    if len(columns) == 0:
        return pd.DataFrame()

    tm_start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")    
    tm_list = []
    for i in range(record_num):
        tm_curr = tm_start + timedelta(minutes=i)
        tm_list.append(tm_curr.strftime("%Y-%m-%d %H:%M:%S"))

    data = np.random.rand(len(tm_list), len(columns))
    return pd.DataFrame(data, index=tm_list, columns=columns)

#------------------------------------------------------------------------------
# transform a list(or a series) to a tuple string
# [1, 2, 3] => "1,2,3"
#------------------------------------------------------------------------------
def gen_tuple_str(lst, quotation_add=True):
    res = ""
    for e in lst:
        if isinstance(e, datetime):
            res += "\'" + str(e) + "\'" + ","
            continue
        
        if not isinstance(e, str):
            res += str(e) + ","
        else:
            if quotation_add:
                res += "\'" + e + "\'" + ","
            else:
                res += e + ","
    res = res[0:-1]
    return res

#------------------------------------------------------------------------------
# 串行生成插入语句中得数据字段
#------------------------------------------------------------------------------
"""
def serial_gen_data_insert_str(data):
    res = ""
    for index, row in data.iterrows():
        res += "("
        res += gen_tuple_str([index])
        res += ","
        res += gen_tuple_str(row)
        res += ")"
        res += ","
    return res
"""

#------------------------------------------------------------------------------
# 串行生成插入语句中得数据字段
#------------------------------------------------------------------------------
def serial_gen_data_insert_str(data):
    res = ""
    data["insert_res"] = data.apply(gen_tuple_str, axis=1)

    #add list() fix a bug
    insert_list = list(data["insert_res"])
    indexer_list = list(data.index)

    for i in range(len(indexer_list)):
        if isinstance(indexer_list[i], datetime) or isinstance(indexer_list[i], str):
            res += "(" + "\'" + str(indexer_list[i]) + "\'" + ","
        else:
            res += "(" + str(indexer_list[i]) + ","

        res += insert_list[i] + ")" + ","
    return res

#------------------------------------------------------------------------------
# 串行生成插入语句中的数据字段（列构成）
#------------------------------------------------------------------------------
def serial_gen_data_insert_column_str(dataframe):
    res = ""
    for column in dataframe:
        res += "("
        res += gen_tuple_str([column])
        res += ","
        res += gen_tuple_str(dataframe[column])
        res += "),"
    return res

#------------------------------------------------------------------------------
# 并发生成插入语句中的数据字段
#------------------------------------------------------------------------------
def para_gen_data_insert_str(data):
    #并发进程数目
    process_num = os.cpu_count() // parallel_level
    #每个进程并发行数
    all_row_num = len(data.index)

    #小于200行的dataframe不再做分割
    block_num = 0
    block_size = 0
    remain_size = all_row_num

    if all_row_num > 200:
        block_num = process_num
        block_size = all_row_num // block_num 
        remain_size = all_row_num % block_num
        
    with Pool(processes=process_num) as p:
        #任务分配
        tmp = []
        for i in range(block_num):
            subblock = data[i * block_size: (i+1) * block_size]
            res = p.apply_async(serial_gen_data_insert_str, (subblock,))
            tmp.append(res)

        remain_block = data[block_num * block_size:]
        res = p.apply_async(serial_gen_data_insert_str, (remain_block,))
        tmp.append(res)

        res_str = ""
        for t in tmp:
            res_str += t.get()
        res_str = res_str[:-1] #去掉最后一个逗号
        return res_str
    
#------------------------------------------------------------------------------
# 并发生成插入语句中的数据字段(列构成)
#------------------------------------------------------------------------------
def para_gen_data_insert_column_str(data):
    #并发进程数目
    process_num = os.cpu_count() // parallel_level
    #每个进程并发行数
    all_columns_num = len(data.columns)

    #小于200列的dataframe不再做分割
    block_num = 0
    block_size = 0
    remain_size = all_columns_num

    if all_columns_num > 200:
        block_num = process_num - 1
        block_size = all_columns_num // block_num 
        remain_size = all_columns_num % block_num
        
    with Pool(processes=process_num) as p:
        #任务分配
        tmp = []
        for i in range(block_num):
            subblock = data.iloc[:, i * block_size: (i+1) * block_size]
            res = p.apply_async(serial_gen_data_insert_column_str, (subblock,))
            tmp.append(res)

        remain_block = data.iloc[:, block_num * block_size:]
        res = p.apply_async(serial_gen_data_insert_column_str, (remain_block,))
        tmp.append(res)

        res_str = ""
        for t in tmp:
            res_str += t.get()
        res_str = res_str[:-1] #去掉最后一个逗号
        return res_str

#------------------------------------------------------------------------------
# 根据用户输入的表名生成实际使用的表名
#------------------------------------------------------------------------------
def gen_real_table_name(user_input_name):
    return user_input_name

#------------------------------------------------------------------------------
# 得到本地时间戳
#------------------------------------------------------------------------------
def get_current_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
