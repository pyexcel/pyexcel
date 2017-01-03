"""
series.py
:copyright: (c) 2014-2017 by Onni Software Ltd.
:license: New BSD License, see LICENSE for more details

This shows how to use `name_columns_by_row` to get the data in various ways.

you will need to do  `pip install pyexcel-ods3`

"""
# please install pyexcel-ods
import os
import pyexcel as pe
import json


def main(base_dir):
    # print all in json
    #
    # Column 1 Column 2 Column 3
    # 1        4        7
    # 2        5        8
    # 3        6        9
    sheet = pe.get_sheet(file_name=os.path.join(base_dir,
                                                "example_series.xls"),
                         name_columns_by_row=0)
    print(json.dumps(sheet.to_dict()))
    # output:
    # {"Column 2": [4.0, 5.0, 6.0], "Column 3": [7.0, 8.0, 9.0],
    #  "Column 1": [1.0, 2.0, 3.0]}

    # get the column headers
    print(sheet.colnames)
    # [u'Column 1', u'Column 2', u'Column 3']

    # get the content in one dimensional array
    data = list(sheet.enumerate())
    print(data)
    # [1.0, 4.0, 7.0, 2.0, 5.0, 8.0, 3.0, 6.0, 9.0]

    # get the content in one dimensional array
    # in reverse order
    data = list(sheet.reverse())
    print(data)

    # get the content in one dimensional array
    # but iterate it vertically
    data = list(sheet.vertical())
    print(data)
    # [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

    # get the content in one dimensional array
    # but iterate it vertically in revserse
    # order
    data = list(sheet.rvertical())
    print(data)
    # [9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0]

    # get a two dimensional array
    data = list(sheet.rows())
    print(data)
    # [[1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]]

    # get a two dimensional array in reverse
    # order
    data = list(sheet.rrows())
    print(data)
    # [[3.0, 6.0, 9.0], [2.0, 5.0, 8.0], [1.0, 4.0, 7.0]]

    # get a two dimensional array but stack columns
    data = list(sheet.columns())
    print(data)
    # [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]

    # get a two dimensional array but stack columns
    # in reverse order
    data = list(sheet.rcolumns())
    print(data)
    # [[7.0, 8.0, 9.0], [4.0, 5.0, 6.0], [1.0, 2.0, 3.0]]

    # and you can write the results
    # into a file
    sheet.save_as("example_series.xls")


if __name__ == '__main__':
    main(os.getcwd())
