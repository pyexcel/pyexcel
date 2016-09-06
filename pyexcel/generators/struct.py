from pyexcel._compact import OrderedDict
from pyexcel_io.sheet import NamedContent
from pyexcel.sheets.iterators import SheetIterator


class SheetStream(NamedContent):
    """
    A container to hold generator as sheet content
    """
    def __init__(self, name, payload):
        NamedContent.__init__(self, name, payload)
        self.colnames = []

    def to_array(self):
        """
        Simply return the generator
        """
        return self.payload


class BookStream(object):
    """Read an excel book that has one or more sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, sheets=None, filename="memory", path=None):
        """Book constructor

        Selecting a specific book according to filename extension
        :param OrderedDict/dict sheets: a dictionary of data
        :param str filename: the physical file
        :param str path: the relative path or absolute path
        :param set keywords: additional parameters to be passed on
        """
        self.path = path
        self.filename = filename
        self.name_array = []
        if sheets:
            self.load_from_sheets(sheets)
        else:
            self.sheets = {}

    def load_from_sheets(self, sheets):
        """Load content from existing sheets

        :param dict sheets: a dictionary of sheets. Each sheet is
        a list of lists
        """
        if sheets is None:
            return
        self.sheets = OrderedDict()
        keys = sheets.keys()
        if not isinstance(sheets, OrderedDict):
            # if the end user does not care about the order
            # we put alphatical order
            keys = sorted(keys)
        for name in keys:
            sheet = SheetStream(name, sheets[name])
            # this sheets keep sheet order
            self.sheets.update({name: sheet})
            # this provide the convenience of access the sheet
            self.__dict__[name] = sheet
        self.name_array = list(self.sheets.keys())

    def to_dict(self):
        """
        Get book data structure as a dictionary
        """
        the_dict = OrderedDict()
        for sheet in self:
            the_dict.update({sheet.name: sheet.payload})
        return the_dict

    def __iter__(self):
        return SheetIterator(self)

    def number_of_sheets(self):
        """Return the number of sheets"""
        return len(self.name_array)

    def __getitem__(self, index):
        if index < len(self.name_array):
            sheet_name = self.name_array[index]
            return self.sheets[sheet_name]
