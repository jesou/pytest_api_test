import os
import threading
from utils.utilsLoadYaml import yamlOptions


class Config(object):
    """
    配置文件
    """
    # file
    EXCEL_FILE = 'excelCase'
    CONFIG_FILE = 'config'

    # yaml_name
    CONFIG_YAML = 'configData.yaml'
    REQUEST_YAML = 'requestDefault.yaml'

    # file_name
    DEV = 'dev'
    TEST = 'test'
    UAT = 'uat'

    # env:
    SDC_DEV = 'sdc_dev'
    SDC_UAT = 'sdc_uat'

    # DB:
    DB = 'database'
    DB_HOST = 'aliyun_host'
    DB_PORT = 'aliyun_port'
    DB_PROXY_HOST = 'proxy_host'
    DB_PROXY_PROT = 'proxy_port'
    DB_SCHEMATA = 'sdc-prd'
    DB_USERNAME = 'username'
    DB_PASSWORD = 'password'

    # auth:
    AUTH_LOGIN = 'auth_login'
    AUTH_KEY = 'api_key'
    AUTH_ID = 'appId'
    AUTH_PASSWORD = 'appSecret'

    # url:
    URL_VALUE = 'url'

    # request
    REQUEST_VALUE = 'requestCon'
    REQUEST_HEADER = 'uatHeader'

    # restful
    RESTFUL_VALUE = 'apiData'

    _instance_lock = threading.Lock()

    def __init__(self, env='UAT'):
        # 项目目录
        self.path = os.path.dirname(os.path.abspath(__file__))

        if env == 'DEV':
            self._case_path = os.path.join(os.path.join(os.path.dirname(self.path), 'excelCase'), Config.TEST)
            self.dev_path = os.path.join(os.path.join(os.path.dirname(self.path), Config.CONFIG_FILE),
                                            Config.TEST)
            self._config_data = yamlOptions(f'{self.dev_path}/configData.yaml').read_full_yaml()
            self._config_request = yamlOptions(f'{self.dev_path}/requestDefault.yaml').read_full_yaml()
        elif env == 'UAT':
            self._case_path = os.path.join(os.path.join(os.path.dirname(self.path), 'excelCase'), Config.UAT)
            self.uat_path = os.path.join(os.path.join(os.path.dirname(self.path), Config.CONFIG_FILE),
                                            Config.UAT)
            self._config_data = yamlOptions(f'{self.uat_path}/configData.yaml').read_full_yaml()
            self._config_request = yamlOptions(f'{self.uat_path}/requestDefault.yaml').read_full_yaml()
        else:
            raise EnvironmentError('输入环境有错')

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            with Config._instance_lock:
                if not hasattr(Config, "_instance"):
                    Config._instance = object.__new__(cls)
        return Config._instance

    # 测试用例表存储地址
    @property
    def excel_case(self):
        return self._case_path

    # 数据库地址
    @property
    def database_host(self):
        return self._config_data['database']['aliyun_host']

    # 数据库端口号
    @property
    def database_port(self):
        return self._config_data['database']['aliyun_port']

    # 数据库代理地址
    @property
    def proxy_host(self):
        return self._config_data['database']['proxy_host']

    # 数据库代理端口号
    @property
    def proxy_port(self):
        return self._config_data['database']['proxy_port']

    # 数据库表名
    @property
    def database_name(self):
        return self._config_data['database']['database_name']

    # 数据库用户名
    @property
    def database_username(self):
        return self._config_data['database']['username']

    # 数据库密码
    @property
    def database_password(self):
        return self._config_data['database']['password']

    # auth 账户id
    @property
    def auth_appId(self):
        return self._config_data['auth_login']['api_key']['appId']

    # auth 账户密码
    @property
    def auth_appSecret(self):
        return self._config_data['auth_login']['api_key']['appSecret']

    # url
    @property
    def url(self):
        return self._config_request['server']['url']

    # 请求头
    @property
    def request_header(self):
        return self._config_request['requestCon']['header']

    # api文档地址
    @property
    def sdc_api_url(self):
        return self._config_request['apiData']['url']

    # api 请求头
    @property
    def sdc_api_header(self):
        return self._config_request['apiData']['header']


if __name__ == '__main__':
    print(Config().sdc_api_header)
