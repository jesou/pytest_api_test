import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from utils.utilPostgresql import sqlOperation
from config.config import Config


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
def get_env_config(envs='UAT'):
    params_config = Config(envs)
    # db_host = params_config.database_host
    # db_port = params_config.database_port
    # proxy_host = params_config.proxy_host
    # proxy_port = params_config.proxy_port
    # database_name = params_config.database_name
    # database_username = params_config.database_username
    # database_password = params_config.database_password
    # auth_appId = params_config.auth_appId
    # auth_appSecret = params_config.auth_appSecret
    url = params_config.url
    return envs, url

