from utils.utilsExcelDataProcess import DataProcess

import json
import jsonpath
import re

# data_process = DataProcess()
# str1 = ''
# str2 = json.loads(str1)
# print(str2)

# def format_userid(match):
#     '''
#     格式化用户id:
#     :return:
#     '''
#     # match.group(0) 匹配的语句
#     # match.group(1) 匹配后的第一个分组语句,()里的为分组语句
#     if match.group(1) != "None":
#         user_id: str = match.group(1)
#         format_userid = user_id.replace(user_id[4:-4], "*" * len(user_id[4:-4]))
#         return f"脱敏后用户id为:{format_userid};"
#
#
# line = "用户id:440300016765;用户名称:人员26946;用户ip:192.168.1.80"
# format_userid = re.sub(r'用户id:(.*?);', format_userid, line)
# print(format_userid)

d = '{"mmsi":"$sailing_vessel_mmsi","dest":"$dest","speed":"$speed","softLink":true}'
path = json.loads(d)
print(type(path))
