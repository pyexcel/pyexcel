"""
    pyexcel.excel
    ~~~~~~~~~~~~~~~~~~~

    One stop interface between Pythonic data structures and excel files

    :copyright: (c) 2015 by C. W.
    :license: GPL v3
"""
from .sheets import Sheet, load, load_from_dict, load_from_records
from .book import load_book, Book


class ExcelInput(object):
    """A generic interface for an excel file to be converted

    The source could be from anywhere, memory or file system
    """
    def load_single_sheet(self, file_name, sheet_name=None, **keywords):
        """Abstract method
        
        :param form_field_name: the file field name in the html form for file upload
        :param sheet_name: For an excel book, there could be multiple sheets. If it is left
                         unspecified, the sheet at index 0 is loaded. For 'csv', 'tsv' file,
                         *sheet_name* should be None anyway.
        :param keywords: additional key words
        :returns: A sheet object
        """
        raise NotImplementedError("Please implement this function")

    def load_book(self, file_name, **keywords):
        """Abstract method
        
        :param form_field_name: the file field name in the html form for file upload
        :param keywords: additional key words
        :returns: A instance of :class:`Book`
        """
        raise NotImplementedError("Please implement this function")
        
    def get_sheet(self, file_name, sheet_name=None, **keywords):
        """
        Get a :class:`Sheet` instance from the file
        
        :param form_field_name: the file field name in the html form for file upload
        :param sheet_name: For an excel book, there could be multiple sheets. If it is left
                         unspecified, the sheet at index 0 is loaded. For 'csv', 'tsv' file,
                         *sheet_name* should be None anyway.
        :param keywords: additional key words
        :returns: A sheet object
        """
        return self.load_single_sheet(file_name, sheet_name, **keywords)
        
    def get_array(self, file_name, sheet_name=None, **keywords):
        """
        Get a list of lists from the file
        
        :param form_field_name: the file field name in the html form for file upload
        :param sheet_name: For an excel book, there could be multiple sheets. If it is left
                         unspecified, the sheet at index 0 is loaded. For 'csv', 'tsv' file,
                         *sheet_name* should be None anyway.
        :param keywords: additional key words
        :returns: A list of lists
        """
        sheet = self.get_sheet(file_name, sheet_name, **keywords)
        return sheet.to_array()

    def get_dict(self, file_name, sheet_name=None, name_columns_by_row=0, name_rows_by_column=-1, **keywords):
        """Get a dictionary from the file
        
        :param form_field_name: the file field name in the html form for file upload
        :param sheet_name: For an excel book, there could be multiple sheets. If it is left
                         unspecified, the sheet at index 0 is loaded. For 'csv', 'tsv' file,
                         *sheet_name* should be None anyway.
        :param keywords: additional key words
        :returns: A dictionary
        """
        sheet = self.load_single_sheet(file_name, sheet_name,
                                        name_columns_by_row=name_columns_by_row,
                                        name_rows_by_column=name_rows_by_column, **keywords)
        return sheet.to_dict()

    def get_records(self, file_name, sheet_name=None, name_columns_by_row=0, name_rows_by_column=-1, **keywords):
        """Get a list of records from the file
  
        :param form_field_name: the file field name in the html form for file upload
        :param sheet_name: For an excel book, there could be multiple sheets. If it is left
                         unspecified, the sheet at index 0 is loaded. For 'csv', 'tsv' file,
                         *sheet_name* should be None anyway.
        :param keywords: additional key words
        :returns: A list of records
        """
        sheet = self.load_single_sheet(file_name, sheet_name,
                                        name_columns_by_row=name_columns_by_row,
                                        name_rows_by_column=name_rows_by_column, **keywords)
        return sheet.to_records()

    def get_book(self, file_name, **keywords):
        """Get a instance of :class:`Book` from the file
        :param form_field_name: the file field name in the html form for file upload
        :param keywords: additional key words
        :returns: A instance of :class:`Book`
        """
        return self.load_book(file_name, **keywords)

    def get_book_dict(self, file_name, **keywords):
        """Get a dictionary of two dimensional array from the file

        :param form_field_name: the file field name in the html form for file upload
        :param keywords: additional key words
        :returns: A dictionary of two dimensional arrays
        """
        book = self.get_book(file_name, **keywords)
        return book.to_dict()


class FileIO(ExcelInput):
    """One stop interface between Pythonic data structures and excel files
    """
    def load_single_sheet(self, file_name, sheet_name=None, **keywords):
        return load(file_name, sheet_name, **keywords)

    def load_book(self, file_name):
        return load_book(file_name)

    def save(self, pyexcel_instance, filename):
        """Save a pyexcel instance to a file
        """
        pyexcel_instance.save_as(filename)

    def save_array(self, array, filename):
        """Save an array to an excel file
        """
        self.save(Sheet(array), filename)

    def save_dict(self, adict, filename):
        """Save a dictionary to an excel file
        """
        self.save(load_from_dict(adict), filename)

    def save_records(self, records, filename):
        """Save a list of records to an excel file
        """
        self.save(load_from_records(records), filename)

    def save_book_dict(self, book_dict, filename):
        """Save a dicionary of 2 dimensional array to an excel file
        """
        self.save(Book(book_dict), filename)

