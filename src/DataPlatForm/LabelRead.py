#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:38:41 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.ReadUtils as rutils
import DataPlatForm.service_pb2 as pb2

#------------------------------------------------------------------------------
# 读取label数据
#------------------------------------------------------------------------------
def read_label(name, start_date="", end_date="", symbols=[]):
    return rutils.general_read_factor_data(name, pb2.label_auth_code, label_db, start_date, end_date, symbols, rutils.read_factor_data)

#------------------------------------------------------------------------------
# 返回因子数据表的日期索引列
#------------------------------------------------------------------------------
def get_label_index(name):
    return rutils.general_get_factor_index_columns(name, pb2.label_auth_code, label_db, rutils.get_factor_indexes, "label index")

#------------------------------------------------------------------------------
# 返回label表中的所有列名（股票列表）
#------------------------------------------------------------------------------
def get_label_columns(name):
    return rutils.general_get_factor_index_columns(name, pb2.label_auth_code, label_db, rutils.get_factor_columns, "label columns")

