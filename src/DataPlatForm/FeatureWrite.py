#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:39:14 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.WriteUtils as wutils
import DataPlatForm.service_pb2 as pb2

#------------------------------------------------------------------------------
# 写入feature数据
#------------------------------------------------------------------------------
def write_feature(data, name, date):
    wutils.general_write_raw_data(data, name, date, pb2.feature_auth_code, raw_feature_db, wutils.write_raw_data, "feature")

#------------------------------------------------------------------------------
# 删除某日期的feature数据
#------------------------------------------------------------------------------
def delete_feature(name, date):
    wutils.general_delete_raw_data(name, pb2.feature_auth_code, raw_feature_db, date, wutils.delete_raw_data, "feature")
