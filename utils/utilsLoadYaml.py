import os
import yaml
from utils.utilsLog import logRecord


class yamlOptions:

    def __init__(self, yaml_file='config/configData.yaml'):
        self.logger = logRecord().get_logger
        self.yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                      yaml_file)

    def read_yaml(self, keyValue):
        try:
            with open(self.yaml_path, "r", encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
                mainData = data[keyValue]
                return mainData
        except ValueError as e:
            self.logger.debug("输入内容有错:{}".format(e))

    def read_full_yaml(self):
        try:
            with open(self.yaml_path, "r", encoding="utf-8") as f:
                yaml_data = yaml.full_load(f)
                return yaml_data
        except ValueError as e:
            self.logger.debug("yaml文件错误")


if __name__ == '__main__':
    print(yamlOptions("config/configData.yaml").read_yaml('database')['host'])
    print(yamlOptions("config/configData.yaml").read_full_yaml())
