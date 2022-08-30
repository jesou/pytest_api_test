from utils.utilsLoadYaml import yamlOptions
from utils.utilsLog import logRecord
import psycopg2


class sqlOperation:
    def __init__(self):
        self.logger = logRecord().get_logger
        self.databases = yamlOptions('config/configData.yaml').read_yaml("database")
        self.host = self.databases['host']
        self.port = self.databases['port']
        self.database = self.databases['database']
        self.username = self.databases['username']
        self.password = self.databases['password']

    def connectionDB(self):
        try:
            db = psycopg2.connect(host=self.host,
                                  port=self.port,
                                  database=self.database,
                                  user=self.username,
                                  password=self.password)
            cursor = db.cursor()
            return db, cursor
        except Exception as e:
            self.logger.debug('连接数据库出错：{}'.format(e))

    def closeDBConnection(self, cursor, db):
        cursor.close()
        db.close()

    def searchDB(self, sql):
        db, cursor = self.connectionDB()
        try:
            cursor.execute(sql)
            self.logger.info('开始执行sql：{}'.format(sql))
        except Exception as e:
            self.logger.debug('查询SQL出错：{}'.format(e))
        data = cursor.fetchall()
        self.closeDBConnection(db, cursor)
        return data


if __name__ == '__main__':
    print(sqlOperation().searchDB('select mmsi,imo from sdc_dw.fm_vessel limit 2'))
