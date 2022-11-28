from config.config import Config
import xlrd
import os
import xlwt


class excelOperation:

    def __init__(self, envs='UAT'):
        self.config = Config(envs)
        self.cases_file = self.config.excel_case

    def _read_xls(self, table_name, sheet_names=''):
        """
        根据table_name 和 sheet_names 分别读取excel中的测试用例
        :param table_name: 表名
        :param sheet_names: 栏名
        :return: 所有的sheetList
        """
        file_path = os.path.join(self.cases_file, table_name)
        data = xlrd.open_workbook(file_path)
        table_sheet_names = data.sheet_names()
        if sheet_names == '' or sheet_names is None:
            # 获取所有的sheet_list
            sheet_list = [data.sheet_by_name(i) for i in table_sheet_names]
            return sheet_list
        else:
            table_sheet_names = [i for i in set(table_sheet_names) if i in set(sheet_names)]
            if len(table_sheet_names) != 0:
                sheet_list = [data.sheet_by_name(i) for i in table_sheet_names]
                return sheet_list
            else:
                return table_sheet_names

    def get_case_data(self, table_names='', sheet_names=''):
        if table_names == '' or table_names is None:
            table_names = os.listdir(self.cases_file)
        for table_name in table_names:
            sheet_list = self._read_xls(table_name, sheet_names)
            if len(sheet_list) != 0:
                for table in sheet_list:
                    row_num = table.nrows
                    for norw in range(1, row_num):
                        yield table.row_values(norw)

    def get_column_data(self, column_value=0):
        """获取所有的api列表"""
        api_list = []
        for filepath, dirnames, filenames in os.walk(self.cases_file):
            for filename in filenames:
                file_path = os.path.join(filepath, filename)
                if '.xls' in file_path:
                    table_list = self._read_xls(file_path)
                    for table in table_list:
                        api_rows = table.nrows
                        for i in range(1, api_rows):
                            if table.cell_value(i, column_value) not in api_list and table.cell_value(i, 4) != 'N':
                                api_list.append(table.cell_value(i, column_value))
        return api_list

    # def get_all_files(self, file_path):
    #     for filepath, dirnames, filenames in os.walk(file_path):
    #         for filename in filenames:
    #             yield os.path.join(filepath, filename)


if __name__ == '__main__':
    excelOperation()
