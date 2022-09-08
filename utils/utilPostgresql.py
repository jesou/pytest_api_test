import json
from datetime import datetime
from decimal import Decimal

from string import Template

from utils.utilsLoadYaml import yamlOptions
from utils.utilsLog import logRecord
import psycopg2
import psycopg2.extras


class sqlOperation:
    def __init__(self):
        self._result = None
        self.logger = logRecord().get_logger
        self.databases = yamlOptions('config/configData.yaml').read_yaml("database")
        self.host = self.databases['host']
        self.port = self.databases['port']
        self.database = self.databases['database']
        self.username = self.databases['username']
        self.password = self.databases['password']
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
                                datetime,
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

    def searchDB(self, sql: str):
        db, cursor = self.connectionDB()
        try:
            cursor.execute(sql)
            self.logger.info('开始执行sql：{}'.format(sql))
        except Exception as e:
            self.logger.debug('查询SQL出错：{}'.format(e))
        self.result = cursor.fetchone()
        db.commit()


if __name__ == '__main__':
    abc = sqlOperation()
    abc.searchDB('select mmsi,imo from sdc_dw.fm_vessel limit 10')
    print(abc.result)
