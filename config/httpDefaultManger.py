from utils.utilsRequests import RequestConfig
import json


class httpSamplerConfig:
    def __init__(self, url, params, method):
        self.response = RequestConfig(yaml_file="config/requestDefault.yaml")
        self.url = url
        self.params = params
        self.method = method

    def httpSampler(self):
        return self.response.request_sampler(self.url, self.params, self.method)

    def ResponseData(self):
        return self.httpSampler().text

    def mainData(self):
        response_data = self.httpSampler().text
        main_data = json.loads(response_data)['data']
        return main_data

    def responseStatus(self):
        return self.httpSampler().status_code
