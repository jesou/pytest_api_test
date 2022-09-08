import pytest
import allure
from utils.core import httpSamplerConfig
from utils.utilsExcelDataProcess import DataProcess
from utils.utilsRequests import RequestConfig
from utils.utilPostgresql import sqlOperation
from utils.utilsExcelOperation import excelOperation
from utils.utilsLoadYaml import yamlOptions


data_process = DataProcess()


@pytest.fixture(scope="session")
def get_db():
    """获取数据库"""
    with sqlOperation() as db:
        yield db


@pytest.fixture(params=excelOperation().get_case_data())
def case(request):
    """读取excel测试用例"""
    return request.param


def test_main(case, get_db):
    """
    :param case: 测试用例
    :param get_db: db数据
    :return:
    """
    api_type, title, purpose, is_skip, url, method, data_type, params, verify_content, sql, expect_value = case
    production_url = yamlOptions('config/requestDefault.yaml').read_yaml('server')['url']['uat_url']
    allure.dynamic.story(api_type)
    allure.dynamic.title(title)
    allure.dynamic.link(production_url)
    allure.dynamic.testcase("http:?")
    response_data = httpSamplerConfig(url=production_url, path=url, params=params, method=method).httpSampler(
        data_type)
    print(response_data.json())
    # 使用后置sql执行
    data_process.sql = sql
    data_process.handle_sql(get_db)
    # 断言
    DataProcess.assert_result(response_data.json(), expect_value)

