from utils.utilsLog import logRecord


class testLogDefine:
    def __init__(self):
        self.get_logger = logRecord().get_logger

    def successLog(self, expect):
        self.get_logger.info("测试通过，\n实际结果为\n{}".format(expect))

    def failureLog(self, expect, result):
        self.get_logger.debug("断言结果错误：期望结果是\n{}，\n但实际结果为\n{}".format(expect, result))


if __name__ == '__main__':
    testLogDefine().successLog(1)

