from copy import deepcopy

from utils.utilPostgresql import sqlOperation
from utils.utilsExcelOperation import excelOperation
from config.httpDefaultManger import httpSamplerConfig
from config.config import Config
from utils.utilsLoadYaml import yamlOptions

import requests
import json
import time
import hashlib
import jsonpath
import platform


class PostgresqlDataBasic(object):

    def __init__(self, url, path, params, method, sql=''):
        self.sql = sql
        self.response_data = httpSamplerConfig(url, path, params, method).responseData()
        sql_path = Config().database_host

    def sqlData(self):
        data_value = sqlOperation().searchDB(self.sql)
        data_length = len(data_value)
        if data_length is not None and data_length >= 0:
            if data_length == 1:
                return str(data_value[0])
            if data_length > 1:
                datas = [str(data_value(i) for i in range(data_length))]
                return datas

    def countResponseData(self):
        response_data = json.loads(self.response_data)
        main_data = response_data['data']['tracks']
        return len(main_data)

    def countSqlResult(self):
        return len(self.sql)


class getExcelCase(object):
    def __init__(self):
        self.config = Config()
        self.url = self.config.sdc_api_url
        self.header = self.config.sdc_api_header
        self.unused_apis = ['/v1/trade/cargo/ore/port/statistics',
                            '/v1/trade/cargo/ore/port/list']
        self.unused_apiGroup = ['Swagger文档数据接口', '缓存管理接口', 'API缓存配置接口',
                                '服务缓存配置接口', '指标分析数据接口', 'BI数据分析报告接口',
                                '教育宝数据接口', '船舶船员宝数据接口', '关键节点数据编辑接口']

    def get_all_case(self, params, column):
        """
        获取所有的API接口
        return: 所有api总数，已经编写的api数量，没有编写api的具体数量，api脚本覆盖率
        """
        unused_apis = []
        url = self.url + params
        response_data = json.loads(requests.get(url=url, headers=self.header).text)
        all_apis = [list(response_data["paths"].keys())[x] for x in range(len(response_data["paths"]))]
        use_apis = excelOperation().get_column_data(column)
        for i in all_apis:
            if i not in use_apis:
                unused_apis.append(i)
            else:
                continue
        # unused_apis = list(set(all_apis).difference(set(use_apis)))
        apiCase_rate = round((len(all_apis) - len(unused_apis)) / len(all_apis), 2)
        return len(all_apis), len(use_apis), unused_apis, apiCase_rate

    def get_effective_cse(self, params, column=0):
        """
        获取有效的接口数据
        剔除已废弃、特殊不做统计的接口
        return: 所有api总数，已经编写的api数量，未编写的api数量，api脚本覆盖率
        """
        unused_apis = []
        url = self.url + params
        response_data = json.loads(requests.get(url=url, headers=self.header).text)
        apis = list(response_data['paths'].keys())
        copy_apis = deepcopy(apis)

        unused_api = []
        for i in copy_apis:
            if jsonpath.jsonpath(response_data, '$.paths.{}..deprecated'.format(i))[0]:
                unused_api.append(i)
                apis.remove(i)
            elif jsonpath.jsonpath(response_data, '$.paths.{}..tags[0]'.format(i))[0] in self.unused_apiGroup:
                unused_api.append(i)
                apis.remove(i)
            elif i in self.unused_apis:
                unused_api.append(i)
                apis.remove(i)
        use_apis = excelOperation().get_column_data(column)
        for i in apis:
            if i not in use_apis:
                unused_apis.append(i)
            else:
                continue
        # unused_apis = list(set(apis).difference(set(use_apis)))
        apiCase_rate = round((len(apis) - len(unused_apis)) / len(apis), 2)
        print(len(apis), len(use_apis), len(unused_apis), unused_apis,  apiCase_rate)
        return len(unused_apis), len(apis), len(use_apis), unused_apis, apiCase_rate


# auth2.0验证
# 包括auth_key,basic_auth,client_credentials
class authLogin(object):
    def __init__(self, env='UAT'):
        self.timestamp = str(int(time.time()))
        self.rand = '0'
        self.config = Config(env)
        self.appId = self.config.auth_appId
        self.appSecret = self.config.auth_appSecret

    def apiKeyLogin(self):
        secret = self.timestamp + '-' + self.rand + '-' + self.appId + '-' + self.appSecret
        secret_md5 = hashlib.md5(secret.encode('utf-8'))
        auth_key = self.timestamp + '-' + self.rand + '-' + self.appId + '-' + secret_md5.hexdigest()
        return auth_key


if __name__ == '__main__':
    data = '?group=1-数据中台业务接口'
    # print(getExcelCase().get_all_case(data, 5))
    getExcelCase().get_effective_cse(data, 5)
