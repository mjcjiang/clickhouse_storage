#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:38:41 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.ReadUtils as rutils

#------------------------------------------------------------------------------
# 读取高级factor数据
#------------------------------------------------------------------------------
def read_alphafactor(name, category, start_date="", end_date="", symbols=[]):
    return rutils.general_read_alpha_data(name, category, alpha_db, start_date, end_date, symbols, rutils.read_factor_data)

#------------------------------------------------------------------------------
# 返回alpha因子数据表的日期索引
#------------------------------------------------------------------------------
def get_alphafactor_index(name, category):
    return rutils.general_get_alpha_index_columns(name, category, alpha_db, rutils.get_factor_indexes, "alpha factor index")

#------------------------------------------------------------------------------
# 返回alphafactor表中的所有列名（股票列表）
#------------------------------------------------------------------------------
def get_alphafactor_columns(name, category):
    return rutils.general_get_alpha_index_columns(name, category, alpha_db, rutils.get_factor_columns, "alpha factor columns")

#------------------------------------------------------------------------------
# 返回alphafactor表的附属信息(返回dict)
#------------------------------------------------------------------------------
def get_alphafactor_info(name, category):
    return rutils.general_get_alphafactor_info(name, category)

