from utils.utilPostgresql import sqlOperation
from utils.utilsRequests import RequestConfig
from utils.utilsExcelOperation import excelOperation
from config.httpDefaultManger import httpSamplerConfig
from utils.utilsLoadYaml import yamlOptions
import requests
import json
import time
import hashlib


class PostgresqlDataBasic(object):

    def __init__(self, url, path, params, method, sql=''):
        self.sql = sql
        self.response_data = httpSamplerConfig(url, path, params, method).responseData()

    def sqlData(self):
        data = sqlOperation().searchDB(self.sql)
        data_length = len(data)
        if data_length is not None and data_length >= 0:
            if data_length == 1:
                return str(data[0])
            if data_length > 1:
                datas = [str(data(i) for i in range(data_length))]
                return datas

    def countResponseData(self):
        response_data = json.loads(self.response_data)
        main_data = response_data['data']['tracks']
        return len(main_data)

    def countSqlResult(self):
        return len(self.sql)


class getExcelCase(object):
    def __init__(self):
        self.path = 'config/requestDefault.yaml'
        self.url = yamlOptions(self.path).read_yaml('apiData')['url']
        self.header = yamlOptions(self.path).read_yaml('apiData')['header']

    def get_all_case(self, params, column):
        """
        获取
        :return:
        """
        url = self.url + params
        response_data = json.loads(requests.get(url=url, headers=self.header).text)
        all_apis = [list(response_data["paths"].keys())[x] for x in range(len(response_data["paths"]))]
        use_apis = excelOperation().get_column_data(column)
        unused_apis = list(set(all_apis).difference(set(use_apis)))
        apiCase_rate = round((len(all_apis) - len(unused_apis)) / len(all_apis), 2)
        return len(all_apis), len(use_apis), unused_apis, apiCase_rate


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


if __name__ == '__main__':
    data = '?group=1-数据中台业务接口'
    print(getExcelCase().get_all_case(data, 5))
