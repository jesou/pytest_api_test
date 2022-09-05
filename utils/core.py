from utils.utilPostgresql import sqlOperation
from config.httpDefaultManger import httpSamplerConfig
from utils.utilsLoadYaml import yamlOptions
import json
import time
import hashlib
import pytest


class PostgresqlDataBasic(object):

    def __init__(self, url, params, method, sql=''):
        self.sql = sql
        self.response_data = httpSamplerConfig(url, params, method).ResponseData()

    def sqlData(self):
        data = sqlOperation().searchDB(self.sql)
        datas = []
        data_length = len(data)
        if data_length is not None and data_length >= 0:
            if data_length == 1:
                return str(data[0])
            if data_length > 1:
                for i in range(data_length):
                    datas.append(str(data[i]))
                return datas

    def countResponseData(self):
        response_data = json.loads(self.response_data)
        main_data = response_data['data']['tracks']
        return len(main_data)

    def countSqlResult(self):
        return len(self.sql)


# auth2.0验证
# 包括auth_key,basic_auth,client_credentials
class authLogin(object):
    def __init__(self):
        self.timestamp = str(int(time.time()))
        self.rand = '0'
        self.appId = yamlOptions().read_yaml('auth_login')['api_key']['appId']
        self.appSecret = yamlOptions().read_yaml('auth_login')['api_key']['appSecret']

    def apiKeyLogin(self):
        secret = self.timestamp + '-' + self.rand + '-' + self.appId + '-' + self.appSecret
        secret_md5 = hashlib.md5(secret.encode('utf-8'))
        auth_key = self.timestamp + '-' + self.rand + '-' + self.appId + '-' + secret_md5.hexdigest()
        return auth_key
