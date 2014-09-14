from base import PyexcelMultipleSheetBase
import os

class TestOdsMultipleSheets(PyexcelMultipleSheetBase):
    def setUp(self):
        self.testfile = "multiple.ods"
