import sys
import os

import allure

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.core import getExcelCase


class TestCaseCount:
    @allure.story('接口覆盖率统计')
    @allure.title('统计结果')
    @allure.severity('critical')
    def test_count_num(self):
        data = '?group=1-数据中台业务接口'
        all_apis_len, use_apis_len, unused_apis, apiCase_rate = getExcelCase().get_all_case(data, 5)
        with allure.step('目前中台接口总数为:%s个' % all_apis_len):
            pass
        with allure.step('目前已实现的接口数为:%s个' % use_apis_len):
            pass
        with allure.step('接口覆盖率：%s' % apiCase_rate):
            pass
        with allure.step('还未使用的接口：%s' % unused_apis):
            pass




