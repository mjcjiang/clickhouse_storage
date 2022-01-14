#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 25 14:18:59 2021
#-------------------------------------------------------------------------------
clickhouse_addr = "192.168.222.221"     #clickhouse数据库地址
factor_db = "factor_database"           #因子数据库名
alpha_db  = "alpha_database"            #高阶因子数据库名
label_db  = "label_database"            #label数据库名

raw_frame_db = "raw_frame_database"     #raw二维frame数据库名
raw_feature_db = "raw_feature_database" #raw二维feature数据库名
raw_list_db = "raw_list_database"       #raw列表数据库名

parallel_size = 80  
parallel_level = 2

factor_timestamp_size = 10
factor_value_size = 8

#默认账户是低权限的客户账户
local_user = "jheng"
local_password = "123456"

grpc_addr = "192.168.222.221:50078"
