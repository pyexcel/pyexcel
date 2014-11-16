from textwrap import dedent

from pyexcel.texttable import Texttable, get_color_string, bcolors

def test_colored():
    table = Texttable()
    table.set_cols_align(["l", "r", "c"])
    table.set_cols_valign(["t", "m", "b"])
    table.add_rows([
        [get_color_string(bcolors.GREEN, "Name Of Person"), "Age", "Nickname"],
         ["Mr\nXavier\nHuon", 32, "Xav'"],
         [get_color_string(bcolors.BLUE,"Mr\nBaptiste\nClement"),
          1,
          get_color_string(bcolors.RED,"Baby")] ])
    expected_output = dedent("""
        +----------------+-----+----------+
        | [92mName Of Person[0m | Age | Nickname |
        +================+=====+==========+
        | Mr             |     |          |
        | Xavier         |  32 |          |
        | Huon           |     |   Xav'   |
        +----------------+-----+----------+
        | [94mMr[0m             |     |          |
        | [94mBaptiste[0m       |   1 |          |
        | [94mClement[0m        |     |   [91mBaby[0m   |
        +----------------+-----+----------+
        """).strip('\n')

    assert table.draw() == expected_output

def test_typed_columns():
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t',  # text
                          'f',  # float (decimal)
                          'e',  # float (exponent)
                          'i',  # integer
                          'a']) # automatic
    table.set_cols_align(["l", "r", "r", "r", "l"])
    table.add_rows([["text",    "float", "exp", "int", "auto"],
                    ["abcd",    "67",    654,   89,    128.001],
                    ["efghijk", 67.5434, .654,  89.6,  12800000000000000000000.00023],
                    ["lmn",     5e-78,   5e-78, 89.4,  .000000000000128],
                    ["opqrstu", .023,    5e+78, 92.,   12800000000000000000000]])
    expected_output = dedent("""
         text     float       exp      int     auto    
        ==============================================
        abcd      67.000   6.540e+02    89   128.001   
        efghijk   67.543   6.540e-01    90   1.280e+22 
        lmn        0.000   5.000e-78    89   0.000     
        opqrstu    0.023   5.000e+78    92   1.280e+22 
        """).strip('\n')

    assert table.draw() == expected_output
