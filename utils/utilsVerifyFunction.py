from utils.core import httpSamplerConfig
import json


class verifyFunction:

    def __init__(self, url, path, parameter, method, post_type):
        self.url = url
        self.path = path
        self.parameter = parameter
        self.method = method
        self.post_type = post_type

    def verifyResponseHeader(self):
        response_status = httpSamplerConfig(url=self.url, path=self.path, params=self.parameter, method=self.method).\
            responseStatus(self.post_type)
        return response_status

    def verifyResponseBody(self):
        response_data1 = httpSamplerConfig(url=self.url, path=self.path, params=self.parameter, method=self.method).\
            responseData(self.post_type)
        response_data = json.loads(response_data1)
        return response_data

