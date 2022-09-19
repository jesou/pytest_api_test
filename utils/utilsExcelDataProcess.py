import re
from string import Template
from typing import Optional, Dict, Any

from utils.utilPostgresql import sqlOperation
from utils.utilsLog import logRecord

from jsonpath import jsonpath
import json


class DataProcess:
    """数据依赖实现"""

    extra_pool = {}

    def __init__(self):
        self.logger = logRecord().get_logger
        self.sql = None

    @classmethod
    def handle_data(cls, value: str) -> Optional[Dict[str, Any]]:
        """处理数据的方法"""
        if value == "":
            return
        try:
            return json.loads(DataProcess.rep_expr(value))
        except json.decoder.JSONDecodeError:
            return eval(DataProcess.rep_expr(value))

    @classmethod
    def rep_expr(cls, content: str):
        content = Template(content).safe_substitute(DataProcess.extra_pool)
        return content

    def handle_sql(self, db_session: sqlOperation):
        for sql_str in self.sql.split(';'):
            sql_str = sql_str.strip()
            if sql_str == '':
                continue
            db_session.searchDB(sql_str)
            self.logger.info(f'执行sql: {sql_str} \n 查询结果：{db_session.result}')
            if db_session.result is not None:
                DataProcess.extra_pool.update(db_session.result)

    @staticmethod
    def extractor(obj: dict, expr: str = ".") -> Any:
        """
        提取字典中的value
        :param obj:
        :param expr:
        :return:
        """
        try:
            result = jsonpath(obj, expr)[0]
        except Exception as e:
            logRecord().get_logger.error(f"{expr} - 无法提取到内容 {e}")
            result = expr
        return result

    @classmethod
    def assert_result(cls, response_value: dict, expect_value: str):
        """
        结果断言
        :param response_value: 实际响应结果
        :param expect_value: 预计响应结果
        :return:
        """
        i = 0
        for k, v in DataProcess.handle_data(expect_value).items():
            actual_value = DataProcess.extractor(response_value, k)
            i += 1
            logRecord().get_logger.info(f"断言{i}：实际结果: - {actual_value}，期望结果：- {v}")
            if type(actual_value) != type(v):
                actual_value = str(actual_value)
                v = str(v)
                return actual_value, v
            else:
                return actual_value, v
