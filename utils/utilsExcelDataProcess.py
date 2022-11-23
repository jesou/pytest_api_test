import re
from string import Template
from typing import Optional, Dict, Any

import pytest

from utils.utilPostgresql import sqlOperation
from utils.utilsLog import logRecord
from utils.reportConfig import allureReportConfig

from jsonpath import jsonpath
import json


class DataProcess:
    """数据依赖实现"""

    extra_pool = {}

    def __init__(self):
        self._skip = None
        self._path = None
        self._method = None
        self._data_type = None
        self._data = None
        self._sql = None
        self._files = None
        self.logger = logRecord().get_logger

    @property
    def skip(self):
        return self._skip

    @skip.setter
    def skip(self, value: str):
        """
        只跳过value判断正确，或value为'N'的测试用例
        :param value:
        :return:
        """
        if value.upper() == 'N' or value == '':
            raise pytest.skip('不执行该测试用例')
        elif value and value.upper() != 'Y':
            raise pytest.skip("结果正确，跳过该测试用例")

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        if self._data_type != "":
            self._data_type = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: str):
        self._data = DataProcess.handle_parameter(value)

    @property
    def sql(self):
        return self._sql

    @sql.setter
    def sql(self, value: str):
        self._sql = DataProcess.rep_expr(value)

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        if value != "" and value is not None:
            for k, v in DataProcess.handle_data(value).items():
                # 多文件上传
                if isinstance(v, list):
                    self._files = [(k, (open(path, "rb"))) for path in v]
                else:
                    # 单文件上传
                    self._files = {k: open(v, "rb")}
        else:
            self._files = None

    @classmethod
    def handle_data(cls, value: str) -> Optional[Dict[str, Any]]:
        """处理数据，并转换为json格式"""
        if value == "":
            return
        try:
            return json.loads(DataProcess.rep_expr(value))
        except json.decoder.JSONDecodeError:
            return eval(DataProcess.rep_expr(value))

    @classmethod
    def handle_parameter(cls, value: str):
        """
        # 处理请求参数
        # 1、先转参数为dict类型，在转回str
        # 2、再去掉$.内容的前后'号，eval函数转换为dict
        # 3、替换掉$.中的内容，使用json.dumps，将dict转为str
        """
        # if data_type == 'params':
        #     return DataProcess.rep_par(value)
        # else:
        # parameter = str(json.loads(value))
        # return json.dumps(eval(DataProcess.rep_par(parameter)))
        return DataProcess.rep_par(value)

    @classmethod
    def rep_par(cls, content: str):
        """
        :param content:
        :return:
        """
        if "$" in content:
            content = Template(content).safe_substitute(DataProcess.extra_pool)
            if '\'' in content:
                content = content.replace('\'', '"')
            if 'None' in content:
                content = content.replace('None', 'null')
            for func in re.findall("\\${(.*?)}", content):
                try:
                    content = content.replace("${%s}" % func, DataProcess.exec_func(func))
                except Exception as e:
                    logRecord().get_logger.error(e)
            return content
        else:
            content = Template(content).safe_substitute(DataProcess.extra_pool)
            for func in re.findall("\\${(.*?)}", content):
                try:
                    content = content.replace("${%s}" % func, DataProcess.exec_func(func))
                except Exception as e:
                    logRecord().get_logger.error(e)
            return content

    @classmethod
    def rep_expr(cls, content: str):
        content = Template(content).safe_substitute(DataProcess.extra_pool)
        for func in re.findall("\\${(.*?)}", content):
            try:
                content = content.replace("${%s}" % func, DataProcess.exec_func(func))
            except Exception as e:
                logRecord().get_logger.error(e)
        return content

    def handle_case(self, method, data, file=None):
        self.method = method
        self.data = data
        self.files = file

    def pre_sql(self, url, db_session: sqlOperation):
        for sql_str in self.sql.split(';'):
            sql_str = sql_str.strip()
            if db_session != '' and (url == '' or url is None):
                db_session.searchDB(sql_str)
                if db_session.result is not None:
                    allureReportConfig.step("sql内容", "执行结果", db_session.result)
                    logRecord().get_logger.info(f"sql内容:{db_session.result}")
                    DataProcess.extra_pool.update(db_session.result)
                    return True
            else:
                continue

    def handle_sql(self, db_session: sqlOperation):
        for sql_str in self.sql.split(';'):
            sql_str = sql_str.strip()
            if sql_str == '':
                continue
            db_session.searchDB(sql_str)
            self.logger.info(f'执行sql: {sql_str} \n 查询结果：{db_session.result}')
            if db_session.result is not None:
                allureReportConfig.step("sql内容", "执行结果", db_session.result)
                DataProcess.extra_pool.update(db_session.result)

    @staticmethod
    def extractor(obj: dict, expr: str = ".") -> Any:
        """
        根据表达式提取字典中的value，表达式, . 提取字典所有内容
        :param obj: 被提取内容
        :param expr: jsonpath对应语法
        :return:
        """
        try:
            result = jsonpath(obj, expr)[0]
        except Exception as e:
            logRecord().get_logger.error(f"{expr} - 无法提取到内容 {e}")
            result = expr
        return result

    @classmethod
    def handle_extra(cls, extra_str: str, response: dict):
        """
        提取响应参数
        :param extra_str: excel中 提取参数栏内容， {"参数名": "jsonpath提取式"}
        :param response: 当前用例的响应结果
        :return:
        """
        if extra_str != "":
            extra_dict = json.loads(extra_str)
            for k, v in extra_dict.items():
                DataProcess.extra_pool[k] = DataProcess.extractor(response, v)
                logRecord().get_logger.info(f"加入依赖字典,key: {k}, 对应value: {v}")

    @classmethod
    def assert_result(cls, response_value: dict, expect_value: str):
        """
        结果断言
        :param response_value: 实际响应结果
        :param expect_value: 预计响应结果
        :return:
        """
        allureReportConfig.step("当前可用参数", "参数内容", DataProcess.extra_pool)
        i = 0
        for k, v in DataProcess.handle_data(expect_value).items():
            actual_value = DataProcess.extractor(response_value, k)
            i += 1
            logRecord().get_logger.info(f"断言{i}：实际结果: - {actual_value}，期望结果：- {v}")
            if type(actual_value) != type(v):
                actual_value = str(actual_value)
                v = str(v)
                assert actual_value == v
            else:
                assert actual_value == v

    @staticmethod
    def exec_func(func: str) -> str:
        """执行函数(exec可以执行Python代码)
        :params func 字符的形式调用函数
        : return 返回的将是个str类型的结果
        """
        # 得到一个局部的变量字典，来修正exec函数中的变量，在其他函数内部使用不到的问题
        loc = locals()
        exec(f"result = {func}")
        return str(loc["result"])
