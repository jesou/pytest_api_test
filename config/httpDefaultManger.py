from utils.utilsRequests import RequestConfig
import json


class httpSamplerConfig:
    def __init__(self, url, path, params, method):
        self.response = RequestConfig(yaml_file="config/uat/requestDefault.yaml")
        self.url = url + path
        self.params = params
        self.method = method

    def httpSampler(self, postType=''):
        return self.response.request_sampler(self.url, self.params, self.method, postType)

    def responseData(self, postType=''):
        return self.httpSampler(postType).text

    def mainData(self, postType=''):
        response_data = self.httpSampler(postType).text
        main_data = json.loads(response_data)['data']
        return main_data

    def responseStatus(self, postType=''):
        return self.httpSampler(postType).status_code
