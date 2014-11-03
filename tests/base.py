import json
import os
import pyexcel as pe
from _compact import BytesIO
from nose.tools import raises


def clean_up_files(file_list):
    for f in file_list:
        if os.path.exists(f):
            os.unlink(f)


def to_json(iterator):
    array = pe.utils.to_array(iterator)
    return json.dumps(array)


def create_sample_file1(file):
    w = pe.Writer(file)
    data=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
    table = []
    table.append(data[:4])
    table.append(data[4:8])
    table.append(data[8:12])
    w.write_array(table)
    w.close()


def create_sample_file1_series(file):
    w = pe.Writer(file)
    data=['c1', 'c2', 'c3', 'c4', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
    table = []
    table.append(data[:4])
    table.append(data[4:8])
    table.append(data[8:12])
    table.append(data[12:16])
    w.write_array(table)
    w.close()

def create_sample_file2(file):
    """
    1,2,3,4
    5,6,7,8
    9,10,11,12
    """    
    w = pe.Writer(file)
    table = []
    for i in [0, 4, 8]:
        array = [i+1, i+2, i+3, i+4]
        table.append(array)
    w.write_array(table)
    w.close()


def create_sample_file2_in_memory(file_type):
    """
    1,2,3,4
    5,6,7,8
    9,10,11,12
    """
    io = BytesIO()
    w = pe.Writer((file_type, io))
    table = []
    for i in [0, 4, 8]:
        array = [i+1, i+2, i+3, i+4]
        table.append(array)
    w.write_array(table)
    w.close()
    return io
    

class PyexcelWriterBase:
    """
    Abstract functional test for writers

    testfile and testfile2 have to be initialized before
    it is used for testing
    """
    content = [
        ['a', 'b', 'c'],
        ['e', 'f', 'g']
    ]

    def _create_a_file(self, file):
        w = pe.Writer(file)
        w.write_array(self.content)
        w.close()
    
    def test_write_array(self):
        self._create_a_file(self.testfile)
        r = pe.Reader(self.testfile)
        actual = pe.utils.to_array(r.rows())
        assert actual == self.content

    def test_write_reader(self):
        """
        Use reader as data container

        this test case shows the file written by pe
        can be read back by itself
        """
        self._create_a_file(self.testfile)
        r = pe.Reader(self.testfile)
        w2 = pe.Writer(self.testfile2)
        w2.write_reader(r)
        w2.close()
        r2 = pe.Reader(self.testfile2)
        actual = pe.utils.to_array(r2.rows())
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
        w = pe.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        r = pe.SeriesReader(self.testfile)
        actual = pe.utils.to_dict(r)
        assert actual == self.content
        
    def test_write_records(self):
        w = pe.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        r = pe.SeriesReader(self.testfile)
        records = pe.utils.to_records(r)
        w2 = pe.Writer(self.testfile)
        w2.write_records(records)
        w2.close()
        r2 = pe.SeriesReader(self.testfile)
        actual = pe.utils.to_dict(r2)
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
        w = pe.Writer(file)
        table = []
        for i in range(0,self.rows):
            row = i + 1
            array = [str(row)] * 4
            table.append(array)
        w.write_rows(table)
        w.close()
        
    def test_number_of_rows(self):
        r = pe.Reader(self.testfile)
        assert self.rows == r.number_of_rows()

    def test_cell_value(self):
        r = pe.Reader(self.testfile)
        for i in range(0, self.rows):
            row = i + 1
            assert str(row) == r.cell_value(i,1)
        for i in r.row_range():
            assert str(i+1) == r.cell_value(i,1)
        assert str(3) == r.cell_value(2, 3)
            
    def test_row_range(self):
        r = pe.Reader(self.testfile)
        assert self.rows == len(r.row_range())
            
    def test_number_of_columns(self):
        r = pe.Reader(self.testfile)
        assert 4 == r.number_of_columns()

    @raises(ValueError)
    def test_slice(self):
        r = pe.Reader(self.testfile)
        content1 = [['1', '1', '1', '1']]
        assert content1 == r.row[0:1]
        content2 = [["1", "1", "1", "1"], ["2", "2", "2", "2"]]
        assert content2 == r.row[0:2]
        assert content2 == r.row[:2]
        content3 = [["2", "2", "2", "2"], ["3","3","3","3"]]
        assert content3 == r.row[1:]
        content4 = [["1", "1", "1", "1"], ["2", "2", "2", "2"]]
        assert content4 == r.row[0:2:1]
        content5 = ["1", "1", "1", "1"]
        assert [content5] == r.row[0:0]
        r.row[2:1]  # bang


class PyexcelMultipleSheetBase:

    def _write_test_file(self, filename):
        w = pe.BookWriter(filename)
        w.write_book_from_dict(self.content)
        w.close()

    def _clean_up(self):
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

    def test_sheet_names(self):
        r = pe.BookReader( self.testfile)
        expected = [ "Sheet1", "Sheet2", "Sheet3"]
        sheet_names = r.sheet_names()
        assert sheet_names == expected

    def test_reading_through_sheets(self):
        b = pe.BookReader(self.testfile)
        data = pe.utils.to_array(b["Sheet1"].rows())
        expected = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
        assert data == expected
        data = pe.to_array(b["Sheet2"].rows())
        expected = [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]
        assert data == expected
        data = pe.to_array(b["Sheet3"].rows())
        expected = [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected
        sheet3 = b["Sheet3"]
        s3 = sheet3.become_series()
        data = pe.to_array(s3.rows())
        expected = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected

    def test_iterate_through_sheets(self):
        b = pe.BookReader(self.testfile)
        for s in b:
            data = pe.utils.to_array(s)
            assert self.content[s.name] == data
        si = pe.iterators.SheetIterator(b)
        for s in si:
            data = pe.utils.to_array(s)
            assert self.content[s.name] == data

    def test_write_a_book_reader(self):
        b = pe.BookReader(self.testfile)
        bw = pe.BookWriter(self.testfile2)
        for s in b:
            data = pe.utils.to_array(s)
            sheet = bw.create_sheet(s.name)
            sheet.write_array(data)
            sheet.close()
        bw.close()
        x = pe.BookReader(self.testfile2)
        for s in x:
            data = pe.utils.to_array(s)
            assert self.content[s.name] == data

    def test_random_access_operator(self):
        r = pe.BookReader(self.testfile)
        value = r["Sheet1"].row[0][1]
        assert value == 1
        value = r["Sheet3"].row[0][1]
        assert value == 'Y'
        value = r["Sheet3"].become_series().row[0][1]
        assert value == 4
        #value = r["Sheet3"].become_sheet().row[0][1]
        #assert value == 'Y'

        
class PyexcelIteratorBase:
    def test_random_access(self):
        assert self.iteratable.cell_value(100, 100) == None

    def test_set_value(self):
        self.iteratable.cell_value(0, 0, 1)
        assert self.iteratable.cell_value(0, 0) == 1

    def test_horizontal_iterator(self):
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(self.iteratable.enumerate())
        assert result == actual

    def test_row_iterator(self):
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_one_dimensional_array(self.iteratable.rows())
        assert result == actual

    def test_row_iterator_2_dimensions(self):
        result = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
        actual = pe.utils.to_array(self.iteratable.rows())
        assert result == actual

    def test_horizontal_reverse_iterator(self):
        result = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        actual = pe.utils.to_array(self.iteratable.reverse())
        assert result == actual

    def test_row_reverse_iterator(self):
        result = [9, 10, 11, 12, 5, 6, 7, 8, 1, 2, 3, 4]
        actual = pe.utils.to_one_dimensional_array(self.iteratable.rrows())
        assert result == actual

    def test_row_reverse_iterator_2_dimensions(self):
        result = [[9, 10, 11, 12], [5, 6, 7, 8], [1, 2, 3, 4]]
        actual = pe.utils.to_array(self.iteratable.rrows())
        assert result == actual

    def test_vertical_iterator(self):
        result = [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
        actual = pe.utils.to_array(self.iteratable.vertical())
        assert result == actual

    def test_column_iterator(self):
        result = [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
        actual = pe.utils.to_one_dimensional_array(self.iteratable.columns())
        assert result == actual

    def test_column_iterator_2_dimensions(self):
        result = [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
        actual = pe.utils.to_array(self.iteratable.columns())
        assert result == actual

    def test_vertical_reverse_iterator(self):
        result = [12, 8, 4, 11, 7, 3, 10, 6, 2, 9, 5, 1]
        actual = pe.utils.to_array(self.iteratable.rvertical())
        assert result == actual

    def test_column_reverse_iterator(self):
        result = [4, 8, 12, 3, 7, 11, 2, 6, 10, 1, 5, 9]
        actual = pe.utils.to_one_dimensional_array(self.iteratable.rcolumns())
        assert result == actual

    def test_column_reverse_iterator_2_dimensions(self):
        result = [[4, 8, 12], [3, 7, 11], [2, 6, 10], [1, 5, 9]]
        actual = pe.utils.to_array(self.iteratable.rcolumns())
        assert result == actual

    def test_horizontal_top_right_2_bottom_left_iterator(self):
        result = [4, 3, 2, 1, 8, 7, 6, 5, 12, 11, 10, 9]
        actual = pe.utils.to_array(pe.iterators.HTRBLIterator(self.iteratable))
        assert result == actual

    def test_horizontal_bottom_left_2_top_right_iterator(self):
        result = [9, 10, 11, 12, 5, 6, 7, 8, 1, 2, 3, 4]
        actual = pe.utils.to_array(pe.iterators.HBLTRIterator(self.iteratable))
        assert result == actual

    def test_vertical_bottom_left_2_top_right_iterator(self):
        result = [9, 5, 1, 10, 6, 2, 11, 7, 3, 12, 8, 4]
        actual = pe.utils.to_array(pe.iterators.VBLTRIterator(self.iteratable))
        assert result == actual

    def test_vertical_top_right_2_bottom_left_iterator(self):
        result = [4, 8, 12, 3, 7, 11, 2, 6, 10, 1, 5, 9]
        actual = pe.utils.to_array(pe.iterators.VTRBLIterator(self.iteratable))
        assert result == actual


class PyexcelSheetRWBase:
            
    @raises(TypeError)
    def test_extend_rows(self):
        r2 = self.testclass(self.testfile)
        content = [['r', 's', 't', 'o'],
                   [1, 2, 3, 4],
                   [True],
                   [1.1, 2.2, 3.3, 4.4, 5.5]]
        r2.row += content
        assert r2.row[3] == ['r', 's', 't', 'o', '']
        assert r2.row[4] == [1, 2, 3, 4, '']
        assert r2.row[5] == [True, "", "", "", '']
        assert r2.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]        
        r2.row += 12  # bang
