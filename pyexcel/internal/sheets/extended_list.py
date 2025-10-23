from collections import Counter
from pyexcel import get_sheet


class PyexcelList(list):
    def value_counts(self):
        c = Counter(self)
        sheet = get_sheet(adict=c)
        sheet.rownames = ["names", "counts"]
        return sheet
