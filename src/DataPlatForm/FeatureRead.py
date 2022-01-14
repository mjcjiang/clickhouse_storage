#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:40:09 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.ReadUtils as rutils
import DataPlatForm.service_pb2 as pb2

#------------------------------------------------------------------------------
# featureÊý¾Ý¶ÁÈ¡
#------------------------------------------------------------------------------
def read_feature(name, start_date=None, end_date=None, fields=[]):
    return rutils.general_read_raw_data(name, pb2.feature_auth_code, raw_feature_db, start_date, end_date, fields, rutils.read_raw_data, "feature")
