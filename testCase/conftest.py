import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import allure
from utils.utilPostgresql import sqlOperation


@pytest.fixture(scope="session")
def get_db():
    """获取数据库"""
    with sqlOperation() as db:
        yield db

# @pytest.fixture(params=excelOperation().get_case_data())
# def case(request):
#     """读取excel测试用例"""
#     return request.param
