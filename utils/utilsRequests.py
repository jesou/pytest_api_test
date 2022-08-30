import requests
from requests.auth import HTTPBasicAuth
from typing import Text
from utils.utilsLoadYaml import yamlOptions
from utils.utilsLog import logRecord


class RequestConfig:
    def __init__(self, yaml_file):
        self.uat_url = yamlOptions(yaml_file).read_yaml('server')['uat']['url']
        self.user = yamlOptions(yaml_file).read_yaml('server')['uat']['user']
        self.password = yamlOptions(yaml_file).read_yaml('server')['uat']['password']
        self.uat_header = yamlOptions(yaml_file).read_yaml('requestCon')['uatHeader']
        self.logger = logRecord().get_logger

    def request_basic_config(self, path: Text):
        url = self.url + path
        header = self.uat_header
        return url, header

    def request_sampler(self, path: Text, params=None, method="get"):
        url_data, header = self.request_basic_config(path)
        if method.upper() == 'GET':
            response_data = requests.get(url=url_data, headers=header, params=params,
                                         auth=HTTPBasicAuth(self.user, self.password))
            return response_data
        elif method.upper() == 'POST':
            response_data = requests.post(url=url_data, headers=header, data=params,
                                          auth=HTTPBasicAuth(self.user, self.password))
            return response_data
        else:
            try:
                response_data = requests.request(method.lower(), url=url_data, headers=header,
                                                 data=params, auth=HTTPBasicAuth(self.user, self.password))
                return response_data
            except ValueError as e:
                self.logger.debug('请求错误{}'.format(e))


if __name__ == '__main__':
    response = RequestConfig(yaml_file="config/requestDefault.yaml").\
        request_sampler('/v1/routes/routing/nodes',
                        params='{"startPortCode":"CNWGQ","startPoint":{"lat":31.353633,"lon":121.617967},'
                               '"endPortCode":"CNHUA", '
                               '"endPoint":{"lat":38.316667,"lon":117.866667},"excludeNodes":[],"excludeSeaAreas":[],'
                               '"withECA":true} ',
                        method='post'
                        )
    print(type(response.text))
