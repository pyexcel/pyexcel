"""
    pyexcel.cookbook
    ~~~~~~~~~~~~~~~~~~~

    Cookbook for pyexcel

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .sheets import Sheet, load, load_from_dict, load_from_records
from .book import load_book, Book


class ExcelInput(object):
    def load_single_sheet(self, file_name, sheet_name=None, **keywords):
        raise NotImplementedError("Please implement this function")

    def load_book(self, file_name):
        raise NotImplementedError("Please implement this function")
        
    def get_sheet(self, file_name, sheet_name=None):
        return self.load_single_sheet(file_name, sheet_name)
        
    def get_array(self, file_name, sheet_name=None):
        sheet = self.get_sheet(file_name, sheet_name)
        return sheet.to_array()

    def get_dict(self, file_name, sheet_name=None, name_columns_by_row=0, name_rows_by_column=-1):
        sheet = self.load_single_sheet(file_name, sheet_name,
                                        name_columns_by_row=name_columns_by_row,
                                        name_rows_by_column=name_rows_by_column)
        return sheet.to_dict()

    def get_records(self, file_name, sheet_name=None, name_columns_by_row=0, name_rows_by_column=-1):
        sheet = self.load_single_sheet(file_name, sheet_name,
                                        name_columns_by_row=name_columns_by_row,
                                        name_rows_by_column=name_rows_by_column)
        return sheet.to_records()

    def get_book(self, file_name):
        return self.load_book(file_name)

    def get_book_dict(self, file_name):
        book = self.get_book(file_name)
        return book.to_dict()


class FileIO(ExcelInput):
    def load_single_sheet(self, file_name, sheet_name=None, **keywords):
        return load(file_name, sheet_name, **keywords)

    def load_book(self, file_name):
        return load_book(file_name)

    def save(self, pyexcel_instance, filename):
        pyexcel_instance.save_as(filename)

    def save_array(self, array, filename):
        self.save(Sheet(array), filename)

    def save_dict(self, adict, filename):
        self.save(load_from_dict(adict), filename)

    def save_records(self, records, filename):
        self.save(load_from_records(records), filename)

    def save_book_dict(self, book_dict, filename):
        self.save(Book(book_dict), filename)

