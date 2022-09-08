import pytest
import json
import allure
from utils.core import httpSamplerConfig
from utils.utilsLogConfig import testLogDefine
from utils.utilsExcelOperation import excelOperation
from utils.utilsLoadYaml import yamlOptions
from utils.utilPostgresql import sqlOperation


@allure.feature('航运数据中台项目')
class Test_sdc:
    @allure.severity('critical')
    @pytest.mark.parametrize("apiType,apiName,purpose,url,method,postType,parameter,"
                             "verify_method,verify_values,expectValue", excelOperation().get_case_data())
    def test_start(self, apiType, apiName, purpose, url, method, post_type, parameter, executeSql, sql, header_code, expectCode, expectValue):
        production_url = yamlOptions('config/requestDefault.yaml').read_yaml('server')['url']['uat_url']
        allure.dynamic.story(apiType)
        allure.dynamic.title(apiName)
        allure.dynamic.link(production_url)
        allure.dynamic.testcase("http:?")
        response_data1 = httpSamplerConfig(url=production_url, path=url, params=parameter, method=method).responseData(post_type)
        response_data = json.loads(response_data1)
        main_data = response_data['status']
        expect_data = int(expectValue)
        if main_data == expect_data:
            testLogDefine().successLog(main_data)
        else:
            testLogDefine().failureLog(expect_data, main_data)
    assert main_data == expect_data
