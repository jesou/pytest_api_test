import requests
import re

from typing import Text
from config.config import Config
from requests.auth import HTTPBasicAuth
from utils.reportConfig import allureReportConfig
from utils.utilsLoadYaml import yamlOptions
from utils.utilsLog import logRecord


class RequestConfig:
    def __init__(self, env='UAT'):
        """
        :param env: 选择执行环境
        """
        self.logger = logRecord().get_logger
        self.pattern = r'{[A-Za-z0-9|/]+}'
        self.config = Config(env)
        try:
            self.url = self.config.url
            self.user = self.config.auth_appId
            self.password = self.config.auth_appSecret
            print(self.user, self.password)
            self.uat_header = self.config.request_header
        except Exception as e:
            self.logger.exception('获取用例基本信息失败,{}'.format(e))

    # auth使用未完成
    # def _request_auth(self, url: Text, header, params=None, method="get", use_auth=True):
    #     if use_auth:
    #         response_data = self._request_method(url=url, headers=header, data=params, method=method, auth=HTTPBasicAuth(self.user, self.password))
    #     else:
    #         response_data = self._request_method(url=url, header=header, data=params, method=method)
    #     return response_data

    # @staticmethod
    # def get_auth_type(user, password, auth_type = None):
    #     if auth_type == '':

    def request_sampler(self, url: Text, params=None, method="get", postType=''):
        header = self.uat_header
        if type(params) is str:
            params = params.encode('UTF-8').decode("latin1")
        else:
            params = str(params)
        # 替换url中的{}
        if '{' in url:
            if ',' in params:
                params_list = params.split(',')
                for i in params_list:
                    url = re.sub(self.pattern, i, url, count=1)
            elif params is not None or params != '':
                url = re.sub(self.pattern, params, url, count=1)
            params = ''

        self.logger.info('请求地址：%r, 请求方法：%s, 请求头：%s, 请求参数：%s'
                         % (url, method.lower(), header, params))
        # auth_type = get_auth_type(self.user, self.password) if (self.user is not None or self.password is not
        #                                                                    None) else None
        if method.upper() == 'GET':
            if '{' not in params:
                if params != '' or params is not None:
                    url = url + params
                response_data = requests.get(url=url, headers=header, auth=HTTPBasicAuth(self.user, self.password))
                self.logger.info('响应码: %r, 响应结果: %s' % (response_data.status_code, response_data.text))
                allureReportConfig.step("响应内容", "responseBody", response_data.text)
                return response_data
            else:
                response_data = requests.get(url=url, headers=header, params=params, auth=HTTPBasicAuth(self.user,
                                                                                                        self.password))
                self.logger.info('响应码: %r, 响应结果: %s' % (response_data.status_code, response_data.text))
                allureReportConfig.step("响应内容", "responseBody", response_data.text)
                return response_data
        elif method.upper() == 'POST':
            if postType == 'params':
                url = url + str(params)
                response_data = requests.post(url=url, headers=header, auth=HTTPBasicAuth(self.user, self.password))
                self.logger.info('响应码: %r, 响应结果: %s' % (response_data.status_code, response_data.text))
                allureReportConfig.step("响应内容", "responseBody", response_data.text)
                return response_data
            else:
                response_data = requests.post(url=url, headers=header, data=params,
                                              auth=HTTPBasicAuth(self.user, self.password))
                self.logger.info('响应码: %r, 响应结果: %s' % (response_data.status_code, response_data.text))
                allureReportConfig.step("响应内容", "responseBody", response_data.text)
            return response_data
        else:
            try:
                response_data = requests.request(method.lower(), url=url, headers=header,
                                                 data=params, auth=HTTPBasicAuth(self.user, self.password))
                self.logger.info('响应码: %r' % response_data.status_code)
                allureReportConfig.step("响应内容", "responseBody", response_data.text)
                return response_data
            except ValueError as e:
                self.logger.debug('请求失败{}'.format(e))


if __name__ == '__main__':
    RequestConfig()
    # response = RequestConfig(). \
    #     request_sampler(f'{Config().url}/v1/routes/routing/nodes',
    #                     params='{"startPortCode":"CNWGQ","startPoint":{"lat":31.353633,"lon":121.617967},'
    #                            '"endPortCode":"CNHUA", '
    #                            '"endPoint":{"lat":38.316667,"lon":117.866667},"excludeNodes":[],"excludeSeaAreas":[],'
    #                            '"withECA":true} ',
    #                     method='post'
    #                     )
