import xlrd
import xlwt


class excelOperation:

    def __init__(self):
        self.file_path = '../excelCase/testCase1.xls'
        self.sheet_name = 'Sheet1'

    def _read_xls(self):
        data = xlrd.open_workbook(self.file_path)
        table = data.sheet_by_name(self.sheet_name)
        return table

    def get_case_data(self):
        table = self._read_xls()
        row_num = table.nrows
        cases_list = [table.row_values(i, start_colx=1, end_colx=None) for i in range(1, row_num) if table.cell_value(i,0) == 'Y']
        return cases_list


if __name__ == '__main__':
    excelOperation().get_case_data()
