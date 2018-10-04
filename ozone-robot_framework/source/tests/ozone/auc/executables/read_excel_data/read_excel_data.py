"""
Python file to Start the Ozone REST Session
"""
from ozone.auc.executables.baseusecase import BaseUseCase
from ozone.utils.excel_parser import ExcelParser
from robot.api import logger
import os


class ReadExcelData(BaseUseCase):
    """
    Reads Excel Data
    """

    def read_excel_data(self):
        """"
        To Read Excel Data
        """
        sheet = ExcelParser()
        path = os.path.split(self.excel_path.encode('string-escape'))
        sheet.get_sheet_view(*path)
        self.json_file = sheet.create_json()


    def runTest(self):
        self.read_excel_data()

    def _validate_context(self):

        if self.ctx_in:
            self.excel_path = self.ctx_in.excel_details.path


    def _finalize_context(self):
        if self.json_file:
            with open(r'..\config\ozoneinput.json', 'w') as fp:
                fp.write(str(self.json_file))
            logger.info('Excel to Json conversion Successful')
        else:
            logger.error('Excel to Json conversion Failed')
            raise AssertionError, 'Excel to Json conversion Failed'

