#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:38:51 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.WriteUtils as wutils
import DataPlatForm.service_pb2 as pb2

#------------------------------------------------------------------------------
# 写入label数据到clickhouse数据库中
#------------------------------------------------------------------------------
def write_label(data, name):
    wutils.general_write_factor_data(data, name, label_db, pb2.label_auth_code, wutils.write_factor_data, "label")

#------------------------------------------------------------------------------
# 删除label表中指定日期之间的数据
#------------------------------------------------------------------------------
def delete_label(name, start_date, end_date):
    wutils.general_delete_factor_data(name, pb2.label_auth_code, label_db, start_date, end_date, wutils.delete_factor_data, "label")
