#-------------------------------------------------------------------------------
# Author: hjiang
# Email: heng.jiang@jingle.ai
# Time: Thu Nov 18 13:38:51 2021
#-------------------------------------------------------------------------------
from DataPlatForm.configs import *
import DataPlatForm.WriteUtils as wutils

#------------------------------------------------------------------------------
# 写入高阶因子数据
#------------------------------------------------------------------------------
def write_alphafactor(data, name, category, author, describes, source="", remark=""):
    wutils.general_write_alpha_data(data, name, alpha_db, category, author, describes, source, remark, wutils.write_factor_data, "alpha factor")

#------------------------------------------------------------------------------
# 删除alphafactor表中指定日期之间的数据
#------------------------------------------------------------------------------
def delete_alphafactor(name, category, start_date, end_date):
    wutils.general_delete_alpha_data(name, category, alpha_db, start_date, end_date, wutils.delete_factor_data, "alpha factor")
