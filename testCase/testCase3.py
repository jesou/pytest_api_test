import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import allure
from utils.core import httpSamplerConfig
from utils.utilsExcelDataProcess import DataProcess
from utils.utilsRequests import RequestConfig
from utils.utilsExcelOperation import excelOperation
from utils.utilsLoadYaml import yamlOptions

data_process = DataProcess()


@pytest.mark.parametrize("api_type, title, purpose, severity, is_skip, url, method, data_type, params, verify_content, "
                         "sql, expect_value", excelOperation().get_case_data())
def test_main(api_type, title, purpose, severity, is_skip, url, method, data_type, params, verify_content, sql,
              expect_value, get_db):
    """
    :param get_db: db数据
    :return:
    """
    production_url = yamlOptions('config/requestDefault.yaml').read_yaml('server')['url']['uat_url']
    allure.dynamic.story(api_type)
    allure.dynamic.title(title)
    allure.dynamic.severity(severity)
    allure.dynamic.link(production_url + url)
    allure.dynamic.testcase("https://jira.csntcorp.com/secure/Tests.jspa#/testCase/SDC-T904")
    if is_skip.upper() == 'Y' or is_skip is None:
        with allure.step('获取响应结果：'):
            response_data = httpSamplerConfig(url=production_url, path=url, params=params, method=method).httpSampler(
                data_type)
            # 使用后置sql执行
            data_process.sql = sql
            data_process.handle_sql(get_db)
            # 断言
            actual_value, expect_v = DataProcess.assert_result(response_data.json(), expect_value)
            assert actual_value == expect_v


if __name__ == '__main__':
    pytest.main(['-s', 'testCase3.py'])
    os.system('allure generate --clean ../report/result -o ../report/html')
