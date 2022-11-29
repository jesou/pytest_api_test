import allure
import json

from typing import Optional
from typing import Union
from typing import Dict
from typing import Any


class allureReportConfig:
    """allure 报告配置"""

    @staticmethod
    def step(step: str, names: str, result: Optional[Union[str, Dict[str, Any]]] = None):
        with allure.step(step):
            if isinstance(result, dict):
                allure.attach(
                    json.dumps(result, ensure_ascii=False),
                    names,
                    allure.attachment_type.JSON
                )
            elif isinstance(result, str):
                allure.attach(
                    result,
                    names,
                    allure.attachment_type.TEXT
                )

    @staticmethod
    def dynamic_comment(feature=None, story=None, title=None,
                        testcase=None, issue=None, description=None,
                        severity=None, link=None):
        """
        动态添加allure样式
        :param feature: 模块名称
        :param story: 用户故事
        :param title: 用例的标题
        :param testcase: 测试用例的链接地址
        :param issue: 对应缺陷链接
        :param description: 用例描述
        :param severity: 用例等级
        :param link: 链接
        """
        allure.dynamic.feature(feature) if feature is not None or feature != '' else 1
        allure.dynamic.story(story) if story is not None or story != '' else 1
        allure.dynamic.title(title) if title is not None or title != '' else 1
        allure.dynamic.testcase(testcase) if testcase is not None or testcase != '' else 1
        allure.dynamic.issue(issue) if testcase is not None or issue != '' else 1
        allure.dynamic.description(description) if description is not None or description != '' else 1
        allure.dynamic.severity(severity) if severity is not None or severity != '' else 1
        allure.dynamic.link(link) if link is not None or link != '' else 1
