"""
    pyexcel.sheets.filterablesheet
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Building on top of formattablesheet, adding filtering feature

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .formattablesheet import FormattableSheet
from ..filters import ColumnIndexFilter, RowIndexFilter, RegionFilter
from ..constants import _IMPLEMENTATION_REMOVED


class FilterableSheet(FormattableSheet):
    """
    A represetation of Matrix that can be filtered
    by as many filters as it is applied
    """
    def __init__(self, sheet):
        FormattableSheet.__init__(self, sheet)

    def add_filter(self, afilter):
        """Apply a filter
        """
        print(_IMPLEMENTATION_REMOVED + "Please use filter().")
        self.filter(afilter)

    def remove_filter(self, afilter):
        """Remove a named filter
        """
        raise NotImplementedError(_IMPLEMENTATION_REMOVED)

    def clear_filters(self):
        """Clears all filters"""
        raise NotImplementedError(_IMPLEMENTATION_REMOVED)

    def filter(self, afilter):
        """Apply the filter with immediate effect"""
        if isinstance(afilter, ColumnIndexFilter):
            self._apply_column_filters(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self._apply_row_filters(afilter)
        elif isinstance(afilter, RegionFilter):
            afilter.validate_filter(self)
            decending_list = sorted(afilter.row_indices, reverse=True)
            for i in decending_list:
                del self.row[i]
            decending_list = sorted(afilter.column_indices, reverse=True)
            for i in decending_list:
                del self.column[i]
        else:
            raise NotImplementedError("Invalid Filter!")

    def _apply_row_filters(self, afilter):
        afilter.validate_filter(self)
        decending_list = sorted(afilter.indices, reverse=True)
        for i in decending_list:
            del self.row[i]

    def _apply_column_filters(self, afilter):
        """Private method to apply column filter"""
        afilter.validate_filter(self)
        decending_list = sorted(afilter.indices, reverse=True)
        for i in decending_list:
            del self.column[i]

    def validate_filters(self):
        """Re-apply filters

        It is called when some data is updated
        """
        raise NotImplementedError(_IMPLEMENTATION_REMOVED)

    def freeze_filters(self):
        """Apply all filters and delete them"""
        raise NotImplementedError(_IMPLEMENTATION_REMOVED)
