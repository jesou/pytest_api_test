import pytest
import requests
import allure
from utils.core import PostgresqlDataBasic
from utils.utilsLogConfig import testLogDefine


class TestClass:
    @allure.feature('航线规划')
    @allure.story('根据节点查询航线路由')
    @allure.testcase('v1/routes/routing/nodes')
    @allure.severity('critical')
    def test_line_plan(self):
        data_num = PostgresqlDataBasic('/v1/routes/routing/nodes',
                                       '{"startPortCode":"CNWGQ","startPoint":{"lat":31.353633,"lon":121.617967},'
                                       '"endPortCode":"CNHUA", '
                                       '"endPoint":{"lat":38.316667,"lon":117.866667},"excludeNodes":[],'
                                       '"excludeSeaAreas":[], '
                                       '"withECA":true} ',
                                       'post').countResponseData()
        if data_num == 99:
            testLogDefine().successLog(data_num)
        else:
            testLogDefine().failureLog(data_num, 99)
        assert data_num == 99


if __name__ == '__main__':
    pytest.main()
