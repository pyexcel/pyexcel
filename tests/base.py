import pyexcel
import json
import os
import datetime


def to_json(iterator):
    array = pyexcel.utils.to_array(iterator)
    return json.dumps(array)


class PyexcelWriterBase:
    """
    Abstract functional test for writers

    testfile and testfile2 have to be initialized before
    it is used for testing
    """
    content = [
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5],
        [1,2,3,4,5]
    ]
    
    def test_write_array(self):
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()
        r = pyexcel.Reader(self.testfile)
        actual = pyexcel.utils.to_array(r.rows())
        assert actual == self.content

    def test_write_reader(self):
        """
        Use reader as data container

        this test case shows the file written by pyexcel
        can be read back by itself
        """
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()
        r = pyexcel.Reader(self.testfile)
        w2 = pyexcel.Writer(self.testfile2)
        w2.write_reader(r)
        w2.close()
        r2 = pyexcel.Reader(self.testfile2)
        actual = pyexcel.utils.to_array(r2.rows())
        assert actual == self.content


class PyexcelHatWriterBase:
    """
    Abstract functional test for hat writers
    """
    content = {
        "X": [1,2,3,4,5],
        "Y": [6,7,8,9,10],
        "Z": [11,12,13,14,15],
    }
    
    def test_series_table(self):
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        r = pyexcel.SeriesReader(self.testfile)
        actual = pyexcel.utils.to_dict(r)
        assert actual == self.content
    

class PyexcelBase:
    def _write_test_file(self, file):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.rows = 3
        w = pyexcel.Writer(file)
        for i in range(0,self.rows):
            row = i + 1
            array = [row, row, row, row]
            w.write_row(array)
        w.close()
        
    def test_number_of_rows(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == r.number_of_rows()

    def test_cell_value(self):
        r = pyexcel.Reader(self.testfile)
        for i in range(0, self.rows):
            row = i + 1
            assert row == r.cell_value(i,1)
        for i in r.row_range():
            assert i+1 == r.cell_value(i,1)
        assert 3 == r.cell_value(2, 3)
            
    def test_row_range(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == len(r.row_range())
            
    def test_number_of_columns(self):
        r = pyexcel.Reader(self.testfile)
        assert 4 == r.number_of_columns()

    def test_json(self):
        r = pyexcel.Reader(self.testfile)
        assert to_json(r.rows()) == '[[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]'

    def test_slice(self):
        r = pyexcel.Reader(self.testfile)
        content1 = [[1, 1, 1, 1]]
        assert content1 == r[0:1]
        content2 = [[1, 1, 1, 1], [2, 2, 2, 2]]
        assert content2 == r[0:2]
        assert content2 == r[:2]
        content3 = [[2, 2, 2, 2], [3,3,3,3]]
        assert content3 == r[1:]
        assert r[2:1] == None
        content4 = [[1, 1, 1, 1], [2, 2, 2, 2]]
        assert content4 == r[0:2:1]
        content5 = [1, 1, 1, 1]
        assert content5 == r[0:0]

class PyexcelXlsBase(PyexcelBase):

    def test_json(self):
        r = pyexcel.Reader(self.testfile)
        assert to_json(r.rows()) == '[[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0], [3.0, 3.0, 3.0, 3.0]]'


class PyexcelMultipleSheetBase:

    def _write_test_file(self, filename):
        w = pyexcel.BookWriter(filename)
        w.write_book_from_dict(self.content)
        w.close()

    def _clean_up(self):
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

    def test_sheet_names(self):
        r = pyexcel.BookReader( self.testfile)
        expected = [ "Sheet1", "Sheet2", "Sheet3"]
        sheet_names = r.sheet_names()
        for name in sheet_names:
            assert name in expected

    def test_reading_through_sheets(self):
        b = pyexcel.BookReader(self.testfile)
        data = pyexcel.utils.to_array(b["Sheet1"].rows())
        expected = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
        assert data == expected
        data = pyexcel.utils.to_array(b["Sheet2"].rows())
        expected = [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]
        assert data == expected
        data = pyexcel.utils.to_array(b["Sheet3"].rows())
        expected = [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected
        sheet3 = b["Sheet3"]
        sheet3.become_series()
        data = pyexcel.utils.to_array(b["Sheet3"].rows())
        expected = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected

    def test_iterate_through_sheets(self):
        b = pyexcel.BookReader(self.testfile)
        for s in b:
            data = pyexcel.utils.to_array(s)
            assert self.content[s.name] == data
        si = pyexcel.iterators.SheetIterator(b)
        for s in si:
            data = pyexcel.utils.to_array(s)
            assert self.content[s.name] == data

    def test_write_a_book_reader(self):
        b = pyexcel.BookReader(self.testfile)
        bw = pyexcel.BookWriter(self.testfile2)
        for s in b:
            data = pyexcel.utils.to_array(s)
            sheet = bw.create_sheet(s.name)
            sheet.write_array(data)
            sheet.close()
        bw.close()
        x = pyexcel.BookReader(self.testfile2)
        for s in x:
            data = pyexcel.utils.to_array(s)
            assert self.content[s.name] == data

    def test_random_access_operator(self):
        r = pyexcel.BookReader(self.testfile)
        value = r["Sheet1"][0][1]
        assert value == 1
        value = r["Sheet3"][0][1]
        assert value == 'Y'
        value = r["Sheet3"].become_series()[0][1]
        assert value == 4
        value = r["Sheet3"].become_sheet()[0][1]
        assert value == 'Y'

        
class PyexcelIteratorBase:
    def test_random_access(self):
        assert self.iteratable.cell_value(100, 100) == None

    def test_set_value(self):
        self.iteratable.cell_value(0, 0, 1)
        assert self.iteratable.cell_value(0, 0) == 1

    def test_horizontal_iterator(self):
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pyexcel.utils.to_array(self.iteratable.enumerate())
        assert result == actual

    def test_row_iterator(self):
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pyexcel.utils.to_one_dimensional_array(self.iteratable.rows())
        assert result == actual

    def test_row_iterator_2_dimensions(self):
        result = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
        actual = pyexcel.utils.to_array(self.iteratable.rows())
        assert result == actual

    def test_horizontal_reverse_iterator(self):
        result = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        actual = pyexcel.utils.to_array(self.iteratable.reverse())
        assert result == actual

    def test_row_reverse_iterator(self):
        result = [9, 10, 11, 12, 5, 6, 7, 8, 1, 2, 3, 4]
        actual = pyexcel.utils.to_one_dimensional_array(self.iteratable.rrows())
        assert result == actual

    def test_row_reverse_iterator_2_dimensions(self):
        result = [[9, 10, 11, 12], [5, 6, 7, 8], [1, 2, 3, 4]]
        actual = pyexcel.utils.to_array(self.iteratable.rrows())
        assert result == actual

    def test_vertical_iterator(self):
        result = [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
        actual = pyexcel.utils.to_array(self.iteratable.vertical())
        assert result == actual

    def test_column_iterator(self):
        result = [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
        actual = pyexcel.utils.to_one_dimensional_array(self.iteratable.columns())
        assert result == actual

    def test_column_iterator_2_dimensions(self):
        result = [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
        actual = pyexcel.utils.to_array(self.iteratable.columns())
        assert result == actual

    def test_vertical_reverse_iterator(self):
        result = [12, 8, 4, 11, 7, 3, 10, 6, 2, 9, 5, 1]
        actual = pyexcel.utils.to_array(self.iteratable.rvertical())
        assert result == actual

    def test_column_reverse_iterator(self):
        result = [4, 8, 12, 3, 7, 11, 2, 6, 10, 1, 5, 9]
        actual = pyexcel.utils.to_one_dimensional_array(self.iteratable.rcolumns())
        assert result == actual

    def test_column_reverse_iterator_2_dimensions(self):
        result = [[4, 8, 12], [3, 7, 11], [2, 6, 10], [1, 5, 9]]
        actual = pyexcel.utils.to_array(self.iteratable.rcolumns())
        assert result == actual

    def test_horizontal_top_right_2_bottom_left_iterator(self):
        result = [4, 3, 2, 1, 8, 7, 6, 5, 12, 11, 10, 9]
        actual = pyexcel.utils.to_array(pyexcel.iterators.HTRBLIterator(self.iteratable))
        assert result == actual

    def test_horizontal_bottom_left_2_top_right_iterator(self):
        result = [9, 10, 11, 12, 5, 6, 7, 8, 1, 2, 3, 4]
        actual = pyexcel.utils.to_array(pyexcel.iterators.HBLTRIterator(self.iteratable))
        assert result == actual

    def test_vertical_bottom_left_2_top_right_iterator(self):
        result = [9, 5, 1, 10, 6, 2, 11, 7, 3, 12, 8, 4]
        actual = pyexcel.utils.to_array(pyexcel.iterators.VBLTRIterator(self.iteratable))
        assert result == actual

    def test_vertical_top_right_2_bottom_left_iterator(self):
        result = [4, 8, 12, 3, 7, 11, 2, 6, 10, 1, 5, 9]
        actual = pyexcel.utils.to_array(pyexcel.iterators.VTRBLIterator(self.iteratable))
        assert result == actual


class PyexcelSheetRWBase:
    def test_extend_rows(self):
        r = self.testclass(self.testfile)
        content = [['r', 's', 't', 'o'],
                   [1, 2, 3, 4],
                   [True],
                   [1.1, 2.2, 3.3, 4.4, 5.5]]
        r.extend_rows(content)
        assert r[3] == ['r', 's', 't', 'o']
        assert r[4] == [1, 2, 3, 4]
        assert r[5] == [True, "", "", ""]
        assert r[6] == [1.1, 2.2, 3.3, 4.4]
        r2 = self.testclass(self.testfile)
        r2 += content
        assert r2[3] == ['r', 's', 't', 'o']
        assert r2[4] == [1, 2, 3, 4]
        assert r2[5] == [True, "", "", ""]
        assert r2[6] == [1.1, 2.2, 3.3, 4.4]        
        r3 = self.testclass(self.testfile)
        sheet = pyexcel.sheets.Sheet(content, "test")
        r3 += sheet
        assert r3[3] == ['r', 's', 't', 'o']
        assert r3[4] == [1, 2, 3, 4]
        assert r3[5] == [True, "", "", ""]
        assert r3[6] == [1.1, 2.2, 3.3, 4.4]
        try:
            r3 += 12
            assert 1==2
        except ValueError:
            assert 1==1
            
    def test_extend_columns(self):
        r = self.testclass(self.testfile)
        columns = [['c1', 'c2', 'c3'],
                   ['x1', 'x2', 'x4']]
        r.extend_columns(columns)
        assert r[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r[2] == ['i', 'j', 1.1, 1, '', '', '']
        r2 = self.testclass(self.testfile)
        columns2 = [['c1', 'c2', 'c3'],
                   ['x1', 'x2', 'x4'],
                   ['y1', 'y2'],
                   ['z1']]
        r2.extend_columns(columns2)
        assert r2[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r2[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r2[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r2[3] == ['', '', '', '', 'z1', '', '']

    def test_add_as_columns(self):
        # test += operator
        columns2 = [['c1', 'c2', 'c3'],
                   ['x1', 'x2', 'x4'],
                   ['y1', 'y2'],
                   ['z1']]
        r3 = self.testclass(self.testfile)
        r3 += pyexcel.sheets.AS_COLUMNS(columns2)
        assert r3[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r3[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r3[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r3[3] == ['', '', '', '', 'z1', '', '']
        r4 = self.testclass(self.testfile)
        sheet = pyexcel.sheets.Sheet(columns2, "test")
        r4 += pyexcel.sheets.AS_COLUMNS(sheet)
        assert r4[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r4[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r4[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r4[3] == ['', '', '', '', 'z1', '', '']

    def test_delete_rows(self):
        r = self.testclass(self.testfile)
        r.delete_rows([0,1])
        assert r[0] == ['i', 'j', 1.1, 1]
        try:
            r.delete_rows("hi")
            assert 1==2
        except ValueError:
            assert 1==1

    def test_delete_columns(self):
        r = self.testclass(self.testfile)
        r.delete_columns([0,2])
        assert r[0] == ['b', 'd']
        try:
            r.delete_columns("hi")
            assert 1==2
        except ValueError:
            assert 1==1
    