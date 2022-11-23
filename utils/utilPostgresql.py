import decimal
import json
import datetime
from decimal import Decimal
from jsonpath import jsonpath

from string import Template

from utils.utilsLoadYaml import yamlOptions
from utils.utilsLog import logRecord
import psycopg2
import psycopg2.extras
import platform


class sqlOperation:
    def __init__(self, path='config/uat/configData.yaml', env='sdc_uat'):
        self.logger = logRecord().get_logger
        self._result = None
        self.path = path
        self.databases = yamlOptions(path).read_yaml("database")

        #  判断系统环境，按不同环境获取不同的数据库地址
        if platform.system().lower() == 'windows' or platform.system().lower() == 'macos':
            self.host = self.databases[env]['aliyun_host']
            self.port = self.databases[env]['aliyun_port']
        elif platform.system().lower() == 'linux':
            self.host = self.databases[env]['proxy_host']
            self.port = self.databases[env]['proxy_port']
        else:
            self.logger.error('该环境不支持连接数据库')

        self.database = self.databases[env]['database']
        self.username = self.databases[env]['username']
        self.password = self.databases[env]['password']
        self.db = psycopg2.connect(host=self.host,
                                   port=self.port,
                                   database=self.database,
                                   user=self.username,
                                   password=self.password
                                   )
        self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        try:
            json.dumps(value)
        except TypeError:
            for k, v in value.items():
                if isinstance(
                        v, (
                                datetime.datetime,
                                Decimal,
                        ),
                ):
                    value[k] = str(v)
        self._result = value

    def connectionDB(self):
        try:
            cursor = self.cursor
            return self.db, cursor
        except Exception as e:
            self.logger.debug('连接数据库出错：{}'.format(e))

    def __enter__(self):
        self.logger.info("数据库连接成功")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("数据库关闭成功")
        self.cursor.close()
        self.db.close()

    def datetime_hadler(self, result):
        if isinstance(result, datetime.date):
            return "{}-{}-{}".format(result.year, result.month, result.day)
        elif isinstance(result, decimal.Decimal):
            return str(result)

    def searchDB(self, sql: str):
        db, cursor = self.connectionDB()
        try:
            cursor.execute(sql)
            self.logger.info('开始执行sql：{}'.format(sql))
        except Exception as e:
            self.logger.debug('查询SQL出错：{}'.format(e))
        sql_result_json = json.dumps(cursor.fetchone(), default=self.datetime_hadler)
        if not isinstance(sql_result_json, dict):
            sql_result_json = eval(sql_result_json)
        self.result = sql_result_json
        db.commit()


if __name__ == '__main__':
    abc = sqlOperation()
    abc.searchDB("SELECT oil_price wti_price,price_date wti_pricedate FROM sdc_dw.ex_bunker_crude_oil_price where is_new = 1  and oil_type = 1")
    print(abc.result)
