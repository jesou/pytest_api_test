import time
import hashlib

t = str(int(time.time()))  # 获取10位时间戳
rand = '0'  # 随机值
appId = '00015412_APP01'  # appId
appSecret = 'rvdkc20kimy5w1jgt9wqhjmpteokfq'  # appSecret
# 拼接数据做md5加密
auth_key1 = t + '-' + rand + '-' + appId + '-' + appSecret
auth_key_md5 = hashlib.md5(auth_key1.encode('utf-8'))
# 再次拼接
auth_key = t + '-' + rand + '-' + appId + '-' + auth_key_md5.hexdigest()
print(auth_key)
