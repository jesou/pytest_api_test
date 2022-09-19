import xlrd
import os
import xlwt


class excelOperation:

    def __init__(self):
        self.project_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'excelCase')

    def _read_xls(self, file_name):
        file_path = os.path.join(self.project_file, file_name)
        data = xlrd.open_workbook(file_path)
        sheet_names = data.sheet_names()
        table_list = [data.sheet_by_name(i) for i in sheet_names]
        return table_list

    def get_case_data(self):
        file_list = os.listdir(self.project_file)
        for file in file_list:
            table_list = self._read_xls(file)
            for table in table_list:
                row_num = table.nrows
                for norw in range(1, row_num):
                    yield table.row_values(norw)


if __name__ == '__main__':
    print(excelOperation().get_case_data())
