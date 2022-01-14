#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:38:51 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.WriteUtils as wutils
import DataPlatForm.service_pb2 as pb2

#------------------------------------------------------------------------------
# 写入factor数据到clickhouse数据库中
#------------------------------------------------------------------------------
def write_factor(data, name):
    wutils.general_write_factor_data(data, name, factor_db, pb2.factor_auth_code, wutils.write_factor_data, "factor")
    
#------------------------------------------------------------------------------
# 删除factor表中指定日期之间的数据
#------------------------------------------------------------------------------
def delete_factor(name, start_date, end_date):
    wutils.general_delete_factor_data(name, pb2.factor_auth_code, factor_db, start_date, end_date, wutils.delete_factor_data, "factor")


