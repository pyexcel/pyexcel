"""
    pyexcel.io.csvbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level csv file format handler.

    :copyright: (c) 2014-2015 by C. W.
    :license: GPL v3
"""
import re
import os
import csv
import codecs
from abc import abstractmethod
import glob
from pyexcel_io import (
    BookReader,
    SheetReaderBase,
    SheetWriter,
    BookWriter,
    DEFAULT_SHEETNAME,
    NamedContent
)
from .._compact import is_string, StringIO, BytesIO, PY2, text_type, Iterator


DEFAULT_SEPARATOR = '__'


class UTF8Recorder(Iterator):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8.
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.reader).encode('utf-8')


class CSVSheetReader(SheetReaderBase):
    def __init__(self, sheet, encoding="utf-8", **keywords):
        SheetReaderBase.__init__(self, sheet, **keywords)
        self.encoding = encoding

    @property
    def name(self):
        return self.native_sheet.name

    @abstractmethod
    def get_file_handle(self):
        pass

    def to_array(self):
        reader = csv.reader(self.get_file_handle(), **self.keywords)
        longest_row_length = -1
        array = []
        for row in reader:
            myrow = []
            for element in row:
                if PY2:
                    myrow.append(element.decode(self.encoding))
                else:
                    myrow.append(element)
            if longest_row_length == -1:
                longest_row_length = len(myrow)
            elif longest_row_length < len(myrow):
                longest_row_length = len(myrow)
            array.append(myrow)
        if len(array) > 0:
            if len(array[0]) < longest_row_length:
                array[0] = (array[0] +
                            [""] * (longest_row_length - len(array[0])))
        return array


class CSVFileReader(CSVSheetReader):
    def get_file_handle(self):
        if PY2:
            f1 = open(self.native_sheet.payload, 'rb')
            f = UTF8Recorder(f1, self.encoding)
        else:
            f = open(self.native_sheet.payload, 'r')
        return f


class CSVinMemoryReader(CSVSheetReader):
    def get_file_handle(self):
        if PY2:
            f = UTF8Recorder(StringIO(self.native_sheet.payload),
                             self.encoding)
        else:
            if isinstance(self.native_sheet.payload, str):
                f = StringIO(self.native_sheet.payload)
            else:
                f = StringIO(self.native_sheet.payload.decode(self.encoding))
        return f


class CSVBook(BookReader):
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, filename, file_content=None,
                 load_sheet_with_name=None,
                 load_sheet_at_index=None, **keywords):
        if filename is None and file_content is None:
            self.keywords = keywords
            self.mysheets = {"csv": []}
        else:
            BookReader.__init__(self, filename, file_content=file_content,
                                load_sheet_with_name=load_sheet_with_name,
                                load_sheet_at_index=load_sheet_at_index,
                                **keywords)

    def load_from_memory(self, file_content, **keywords):
        return [NamedContent('csv', file_content)]

    def load_from_file(self, filename, **keywords):
        names = filename.split('.')
        filepattern = "%s%s*%s*.%s" % (names[0],
                                       DEFAULT_SEPARATOR,
                                       DEFAULT_SEPARATOR,
                                       names[1])
        filelist = glob.glob(filepattern)
        if len(filelist) == 0:
            file_parts = os.path.split(filename)
            return [NamedContent(file_parts[-1], filename)]
        else:
            matcher = "%s%s(.*)%s(.*).%s" % (names[0],
                                             DEFAULT_SEPARATOR,
                                             DEFAULT_SEPARATOR,
                                             names[1])
            tmp_file_list = []
            for filen in filelist:
                result = re.match(matcher, filen)
                tmp_file_list.append((result.group(1), result.group(2), filen))
            ret = []
            for lsheetname, index, filen in sorted(tmp_file_list,
                                                   key=lambda row: row[1]):
                if self.sheet_name is not None:
                    if self.sheet_name == lsheetname:
                        ret.append(NamedContent(lsheetname, filen))
                elif self.sheet_index is not None:
                    if self.sheet_index == int(index):
                        ret.append(NamedContent(lsheetname, filen))
                else:
                    ret.append(NamedContent(lsheetname, filen))
            if len(ret) == 0:
                if self.sheet_name is not None:
                    raise ValueError("%s cannot be found" % self.sheet_name)
                elif self.sheet_index is not None:
                    raise IndexError("Index %d of out bound %d." % (self.sheet_index,
                                                                    len(filelist)))
            return ret

    def sheetIterator(self):
        return self.native_book

    def getSheet(self, native_sheet):
        if self.load_from_memory_flag:
            return CSVinMemoryReader(native_sheet, **self.keywords)
        else:
            return CSVFileReader(native_sheet, **self.keywords)


class CSVSheetWriter(SheetWriter):
    """
    csv file writer

    """
    def __init__(self, filename, name,
                 encoding="utf-8", single_sheet_in_book=False,
                 sheet_index=None, **keywords):
        self.encoding = encoding
        sheet_name = name
        if single_sheet_in_book:
            sheet_name = None
        self.sheet_index = sheet_index
        SheetWriter.__init__(self, filename,
                             sheet_name, sheet_name,
                             **keywords)

    def set_sheet_name(self, name):
        if is_string(type(self.native_book)):
            if name != DEFAULT_SHEETNAME:
                names = self.native_book.split(".")
                file_name = "%s%s%s%s%s.%s" % (names[0],
                                               DEFAULT_SEPARATOR,
                                               name,              # sheet name
                                               DEFAULT_SEPARATOR,
                                               self.sheet_index,  # sheet index
                                               names[1])
            else:
                file_name = self.native_book
            if PY2:
                self.f = open(file_name, "wb")
            else:
                self.f = open(file_name, "w", newline="")
        else:
            self.f = self.native_book
        self.writer = csv.writer(self.f, **self.keywords)

    def write_row(self, array):
        """
        write a row into the file
        """
        if PY2:
            self.writer.writerow(
                [text_type(s if s is not None else '').encode(self.encoding)
                 for s in array])
        else:
            self.writer.writerow(array)

    def close(self):
        """
        This call close the file handle
        """
        if not isinstance(self.f, StringIO) and not isinstance(self.f, BytesIO):
            self.f.close()


class CSVWriter(BookWriter):
    """
    csv file writer

    if there is multiple sheets for csv file, it simpily writes
    multiple csv files
    """
    def __init__(self, file, **keywords):
        self.index = 0
        BookWriter.__init__(self, file, **keywords)

    def create_sheet(self, name):
        self.index = self.index + 1
        return CSVSheetWriter(self.file, name,
                              sheet_index=(self.index-1),
                              **self.keywords)

    def close(self):
        """
        This call close the file handle
        """
        pass
