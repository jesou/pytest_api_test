import xlrd
import os
import xlwt


class excelOperation:

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                      'excelCase/testCase2.xls')
        self.sheet_name = 'Sheet1'

    def _read_xls(self):
        data = xlrd.open_workbook(self.file_path)
        table = data.sheet_by_name(self.sheet_name)
        return table

    def get_case_data(self):
        table = self._read_xls()
        row_num = table.nrows
        for norw in range(1, row_num):
            yield table.row_values(norw)


if __name__ == '__main__':
    print(excelOperation().get_case_data())
