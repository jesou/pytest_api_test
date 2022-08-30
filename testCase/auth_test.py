import pytest
import allure
from utils.core import authLogin
from config.httpDefaultManger import httpSamplerConfig
from utils.utilsLogConfig import testLogDefine


class TestAuth:
    @allure.feature('api_key验证方式的登录校验')
    @allure.description('验证通过auth_key方式的APP授权，'
                        '授权后的APP能否正常访问')
    @allure.testcase('https://emb.data.myvessel.cn/microapps/vesselschedule')
    @allure.severity('critical')
    def test_apiKeys(self):
        auth_key = authLogin().apiKeyLogin()
        urls = 'https://emb.data.myvessel.cn/microapps/vesselschedule' + '?' + 'auth_key =' + auth_key
        httpSamplerConfig()