import os
from configparser import ConfigParser
from utils.utilsLoadYaml import yamlOptions


class Config(object):
    """
    ：配置文件
    """
    # yaml_name
    CONFIG_YAML = 'configData.yaml'
    REQUEST_YAML = 'requestDefault.yaml'

    # file_name
    TEST = 'test'

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

    # 获取当前文件所在的目录

    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      Config.TEST_CONFIG_YAML)
        print(self.path)


if __name__ == '__main__':
    Config()
