import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from utils.utilPostgresql import sqlOperation
from utils.utilsLoadYaml import yamlOptions


# 注册自定义的命令行参数
def pytest_addoption(parser):
    parser.addoption("--envs",
                     action="store",
                     default="test",
                     choices=["uat", "test", "uat", "pro"],
                     help="dev:dev环境，test:测试环境，uat:uat环境，pro:生成环境，默认为test环境")


@pytest.fixture(scope="session")
def get_db():
    """获取数据库"""
    with sqlOperation() as db:
        yield db


# 读取自定义参数的值
@pytest.fixture(scope="session")
def envs(request):
    return request.config.getoption("--envs")


# 读取yaml配置文件内容
@pytest.fixture(scope="session", autouse=True)
def get_env_config(envs):
    if envs == 'dev':
        yaml_dev_option = yamlOptions('config/test/configData.yaml')
        dev_request_option = yamlOptions('config/test/requestDefault.yaml')
        dev_db = yaml_dev_option.read_yaml('database')['sdc_dev']
        dev_db_host = dev_db['aliyun_host']
        dev_db_port = dev_db['aliyun_port']
        dev_proxy_host = dev_db['proxy_host']
        dev_proxy_port = dev_db['proxy_port']
        dev_database = dev_db['database']
        dev_username = dev_db['username']
        dev_password = dev_db['password']
        dev_auth_login = yaml_dev_option.read_yaml('auth_login')['appId']
        dev_appId = dev_auth_login['appId']
        dev_appSecret = dev_auth_login['appSecret']
        dev_server = dev_request_option.read_yaml('server')
        dev_url = dev_server['url']
        return dev_db_host, dev_db_port, dev_proxy_host, dev_proxy_port, dev_database, dev_username, dev_password, \
               dev_appId, dev_appSecret, dev_url
    elif envs == 'uat':
        yaml_uat_option = yamlOptions('config/uat/configData.yaml')
        uat_request_option = yamlOptions('config/uat/requestDefault.yaml')
        uat_db = yaml_uat_option.read_yaml('database')['sdc_uat']
        uat_db_host = uat_db['aliyun_host']
        uat_db_port = uat_db['aliyun_port']
        uat_proxy_host = uat_db['proxy_host']
        uat_proxy_port = uat_db['proxy_port']
        uat_database = uat_db['database']
        uat_username = uat_db['username']
        uat_password = uat_db['password']
        uat_auth_login = yaml_uat_option.read_yaml('auth_login')['appId']
        uat_appId = uat_auth_login['appId']
        uat_appSecret = uat_auth_login['appSecret']
        uat_server = uat_request_option.read_yaml('server')
        uat_url = uat_server['url']['uat_url']
        return uat_db_host, uat_db_port, uat_proxy_host, uat_proxy_port, uat_database, uat_username, uat_password, \
               uat_appId, uat_appSecret, uat_url
    else:
        return ValueError


# @pytest.fixture(params=excelOperation().get_case_data())
# def case(request):
#     """读取excel测试用例"""
#     return request.param
