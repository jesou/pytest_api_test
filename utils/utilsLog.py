from loguru import logger
import os
import datetime


class logRecord(object):
    def __init__(self):
        self.logger_add()

    def get_log_path(self):
        logs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 'log')
        # 根据当天日期更新日志
        log_filename = 'logtime_{}.log'.format(datetime.date.today())
        project_log_path = os.path.join(logs_path, log_filename)
        return project_log_path

    def logger_add(self):
        logger.remove()
        logger.add(
            sink=self.get_log_path(),
            format="{time:YYYY-MM-DD hh:mm:ss}-{level}-{message}",
            retention='10 day',
            encoding="utf-8",
            enqueue=True
        )

    @property
    def get_logger(self):
        return logger


if __name__ == '__main__':
    """
    调用示例
    """
    logger = logRecord().get_logger
    logger.debug('测试01')
