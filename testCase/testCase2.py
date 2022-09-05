import pytest
import json
import allure
from utils.core import httpSamplerConfig
from utils.utilsLogConfig import testLogDefine
from utils.utilsExcelOperation import excelOperation

"""
执行xsl测试用例
"""


class Test_xlsCase:

    @pytest.mark.parametrize("apiType,apiName,purpose,url,method,postType,parameter,executeSql,"
                             "sql,header_code,expectCode,expectValue", excelOperation().get_case_data())
    def test_xls(self, apiType, apiName, purpose, url, method, postType, parameter, executeSql, sql, header_code, expectCode, expectValue):
        response_data = httpSamplerConfig(url=url, params=parameter, method=method).responseStatus()
        expectValue = int(expectValue)
        # response_data = json.loads(response_data)
        # main_data = response_data['data']
        if response_data == expectValue:
            testLogDefine().successLog(response_data)
        else:
            testLogDefine().failureLog(expectValue, response_data)
        assert response_data == expectValue
