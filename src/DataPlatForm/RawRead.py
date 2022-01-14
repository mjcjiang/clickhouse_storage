#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:40:09 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.ReadUtils as rutils
from DataPlatForm.BasicUtils import *
from clickhouse_driver import Client
import DataPlatForm.AccessControl as control

import grpc
import DataPlatForm.service_pb2 as service_pb2
import DataPlatForm.service_pb2_grpc as service_pb2_grpc

#------------------------------------------------------------------------------
# frame数据读取接口
#------------------------------------------------------------------------------
def read_frame(name, start_date=None, end_date=None, fields=[]):
    return rutils.general_read_raw_data(name, service_pb2.raw_auth_code, raw_frame_db, start_date, end_date, fields, rutils.read_raw_data, "frame")


#------------------------------------------------------------------------------
# 读取列表内容
# name: 列表名
#------------------------------------------------------------------------------
def __read_list(name):
    client = control.get_session_client()
    
    if not is_table_exist(client, raw_list_db, name):
        raise ValueError("%s not in %s database!" % (name, raw_list_db))

    select_query = "select * from " + raw_list_db + "." + name
    res = client.execute(select_query)

    return [x[0] for x in res]

#------------------------------------------------------------------------------
# 通过权限校验的列表读取
#------------------------------------------------------------------------------
def read_list(name): 
    with grpc.insecure_channel(grpc_addr) as channel:
        stub = service_pb2_grpc.DACStub(channel)

        old_account = control.get_user()
        old_password = control.get_password()

        #登录信息和权限获取请求
        loginfo = service_pb2.LoginInfo(account=old_account, password=old_password)
        aclreq = service_pb2.AclRequest(loginfo=loginfo, dataname=name, datacategory=service_pb2.raw_auth_code, operation=1)
        response = stub.CheckAcl(aclreq)
        if response.code == 0:
            db_account = response.db_account
            db_password = response.db_password
            db_table = response.db_table

            control.set_user_and_password(db_account, db_password)
            res = __read_list(db_table)
            control.set_user_and_password(old_account, old_password)
            return res
        else:
            raise ValueError("Can't delete list, %s" % (response.detail,))
