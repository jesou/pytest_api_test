import xlrd
import os
import xlwt


class excelOperation:

    def __init__(self):
        self.project_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'excelCase')

    def _read_xls(self, table_name, sheet_names=''):
        file_path = os.path.join(self.project_file, table_name)
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
            table_names = os.listdir(self.project_file)
        for table_name in table_names:
            sheet_list = self._read_xls(table_name, sheet_names)
            if len(sheet_list) != 0:
                for table in sheet_list:
                    row_num = table.nrows
                    for norw in range(1, row_num):
                        yield table.row_values(norw)

    def get_column_data(self, column_value=0):
        file_list = os.listdir(self.project_file)
        api_list = []
        for file in file_list:
            table_list = self._read_xls(file)
            for table in table_list:
                api_rows = table.nrows
                for i in range(1, api_rows):
                    if table.cell_value(i, column_value) not in api_list and table.cell_value(i, 4) != 'N':
                        api_list.append(table.cell_value(i, column_value))
        return api_list


if __name__ == '__main__':
    print(excelOperation().get_case_data())
