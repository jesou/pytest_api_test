import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from utils.core import httpSamplerConfig
from utils.utilsExcelDataProcess import DataProcess
from utils.utilsRequests import RequestConfig
from utils.utilsExcelOperation import excelOperation
from utils.utilsLoadYaml import yamlOptions
from utils.reportConfig import allureReportConfig

data_process = DataProcess()


# @pytest.mark.flaky(reruns=2, reruns_delay=2)
@pytest.mark.parametrize("api_type, title, purpose, severity, is_skip, url, method, data_type, data, extra, "
                         "sql, expect_value", excelOperation().get_case_data(table_names=['sdc_app_case.xls']))
def test_main(api_type, title, purpose, severity, is_skip, url, method, data_type, data, extra, sql,
              expect_value, get_db, get_env_config):
    """
    :param get_db: db数据
    :return:
    """
    env, production_url = get_env_config
    # 设置allure样式
    allureReportConfig.dynamic_comment(feature=api_type, story=title, title=purpose,
                                       severity=severity, link=production_url + url)

    data_process.skip = is_skip
    data_process.sql = sql
    # 先执行pre_sql
    pre_sql = data_process.pre_sql(url, get_db)
    if not pre_sql:
        data_process.data_type = data_type
        data_process.handle_case(method, data)
        # 执行请求，返回响应结果
        response_data = httpSamplerConfig(url=production_url, path=url, params=data_process.data, method= data_process.
                                          method).httpSampler(data_process.data_type)
        # 提取后置参数
        data_process.handle_extra(extra, response_data.json())
        # 使用后置sql执行
        data_process.handle_sql(get_db)
        # 断言
        DataProcess.assert_result(response_data.json(), expect_value)
    else:
        assert pre_sql


if __name__ == '__main__':
    pytest.main(['-s', 'test_case3.py'])
    os.system('allure generate --clean ../report/result -o ../report/html')
    os.system('allure server ../report/result')
