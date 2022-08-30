from utils.utilsRequests import RequestConfig


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


