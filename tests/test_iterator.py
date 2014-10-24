import os
import pyexcel
import datetime
import copy
from base import PyexcelIteratorBase, create_sample_file2


class TestMatrix:

    def test1(self):
        """Test empty array as input to Matrix"""
        m = pyexcel.iterators.Matrix([])
        assert m.number_of_columns() == 0
        assert m.number_of_rows() == 0

    def test_update_a_cell(self):
        data = [
            ['a', 'b', 'c', 'd'],
            ['e', 'f', 'g', 'h'],
            ['i', 'j', 1.1, 1]
        ]
        r = pyexcel.iterators.Matrix(data)
        r[0,0] = 'k'
        assert r[0,0] == 'k'
        d = datetime.date(2014, 10, 1)
        r.cell_value(0, 1, d)
        assert isinstance(r[0,1], datetime.date) is True
        assert r[0,1].strftime("%d/%m/%y") == "01/10/14"

    def test_transpose(self):
        """Test transpose"""
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        result = [
            [1, 4],
            [2, 5],
            [3, 6]
        ]
        m = pyexcel.iterators.Matrix(data)
        m.transpose()
        actual = pyexcel.utils.to_array(m)
        assert result == actual

    def test_extend_columns(self):
        """Test extend columns"""
        data1 = [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4],
            [1]
        ]
        m = pyexcel.iterators.Matrix(data1)
        data2 = [[1, 2], [1, 2]]
        m.extend_columns(data2)
        result = [
            [1, 2, 3, 4, 5, 6, 1, 2],
            [1, 2, 3, 4, '', '', 1, 2],
            [1, '', '', '', '', '', '', '']
        ]
        actual = pyexcel.utils.to_array(m)
        assert result == actual
        # += 
        data11 = [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4],
            [1]
        ]
        m2 = pyexcel.iterators.Matrix(data11)
        m2.column += data2
        actual2 = pyexcel.utils.to_array(m2)
        assert result == actual2
        # +
        data111 = [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4],
            [1]
        ]
        m3 = pyexcel.iterators.Matrix(data111)
        m4 = m3.column + data2
        actual3 = pyexcel.utils.to_array(m4)
        assert result == actual3
        
    def test_extend_rows(self):
        data = [
            ['a', 'b', 'c', 'd'],
            ['e', 'f', 'g', 'h'],
            ['i', 'j', 1.1, 1]
        ]
        r = pyexcel.iterators.Matrix(copy.deepcopy(data))
        content = [['r', 's', 't', 'o'],
                   [1, 2, 3, 4],
                   [True],
                   [1.1, 2.2, 3.3, 4.4, 5.5]]
        r.extend_rows(content)
        assert r.row[3] == ['r', 's', 't', 'o', '']
        assert r.row[4] == [1, 2, 3, 4, '']
        assert r.row[5] == [True, "", "", "", '']
        assert r.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]
        r2 = pyexcel.iterators.Matrix(copy.deepcopy(data))
        r2.row += content
        assert r2.row[3] == ['r', 's', 't', 'o', '']
        assert r2.row[4] == [1, 2, 3, 4, '']
        assert r2.row[5] == [True, "", "", "", '']
        assert r2.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]        
        r3 = pyexcel.iterators.Matrix(copy.deepcopy(data))
        r3 = r3.row + content
        assert r3.row[3] == ['r', 's', 't', 'o', '']
        assert r3.row[4] == [1, 2, 3, 4, '']
        assert r3.row[5] == [True, "", "", "", '']
        assert r3.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]
        try:
            r3 += 12
            assert 1==2
        except TypeError:
            assert 1==1
            
    def test_delete_columns(self):
        data = [
            ['a', 'b', 'c', 'd'],
            ['e', 'f', 'g', 'h'],
            ['i', 'j', 1.1, 1]
        ]
        r = pyexcel.iterators.Matrix(copy.deepcopy(data))
        r.delete_columns([0,2])
        assert r.row[0] == ['b', 'd']
        r2 = pyexcel.iterators.Matrix(copy.deepcopy(data))
        del r2.column[0]
        assert r2.row[0] == ['b', 'c', 'd']
        try:
            r.delete_columns("hi")
            assert 1==2
        except ValueError:
            assert 1==1

    def test_set_column_at(self):
        data = [
            ['a', 'b', 'c', 'd'],
            ['e', 'f', 'g', 'h'],
            ['i', 'j', 1.1, 1]
        ]
        r = pyexcel.iterators.Matrix(data)
        try:
            r.set_column_at(1, [11, 1], 1000)
            assert 1 == 2
        except IndexError:
            assert 1 == 1

    def test_set_rows(self):
        data = [
            ['a', 'b', 'c', 'd'],
            ['e', 'f', 'g', 'h'],
            ['i', 'j', 1.1, 1]
        ]
        r = pyexcel.iterators.Matrix(data)
        content = ['r', 's', 't', 'o']
        r.row[1] = content
        assert r.row[1] == content
        content2 = [1, 2, 3, 4]
        r.row[1:] = content2
        assert r.row[2] == [1, 2, 3, 4]
        content3 = [True, False, True, False]
        r.row[0:0] = content3
        assert r.row[0] == [True, False, True, False]
        r.row[0:2:1] = [1, 1, 1, 1]
        assert r.row[0] == [1, 1, 1, 1]
        assert r.row[1] == [1, 1, 1, 1]
        assert r.row[2] == [1, 2, 3, 4]
        try:
            r.row[2:1] = ['e', 'r', 'r', 'o']
            assert 1 == 2
        except ValueError:
            assert 1 == 1

    def test_set_columns(self):
        data = [
            ['a', 'b', 'c', 'd'],
            ['e', 'f', 'g', 'h'],
            ['i', 'j', 1.1, 1]
        ]
        r = pyexcel.iterators.Matrix(data)
        content = ['r', 's', 't', 'o']
        r.column[1] = content
        assert r.column[1] == content[:3]
        assert r.column[0] == ['a', 'e', 'i']
        content2 = [1, 2, 3, 4]
        r.column[1:] = content2
        assert r.column[2] == content2[:3]
        content3 = [True, False, True, False]
        r.column[0:0] = content3
        assert r.column[0] == content3[:3]
        r.column[0:2:1] = [1, 1, 1, 1]
        assert r.column[0] == [1, 1, 1]
        assert r.column[1] == [1, 1, 1]
        assert r.column[2] == content2[:3]
        try:
            r.column[2:1] = ['e', 'r', 'r', 'o']
            assert 1 == 2
        except ValueError:
            assert 1 == 1

    def test_delete_rows(self):
        data = [
            ['a', 'b', 'c', 'd'],
            ['e', 'f', 'g', 'h'],
            ['i', 'j', 1.1, 1]
        ]
        r = pyexcel.iterators.Matrix(copy.deepcopy(data))
        content = ['i', 'j', 1.1, 1]
        assert r.row[2] == content
        del r.row[0]
        assert r.row[1] == content
        r2 = pyexcel.iterators.Matrix(copy.deepcopy(data))
        del r2.row[1:]
        assert r2.number_of_rows() == 1
        r3 = pyexcel.iterators.Matrix(copy.deepcopy(data))
        del r3.row[0:0]
        assert r3.row[1] == content
        assert r3.number_of_rows() == 2
        try:
            del r.row[2:1]
            assert 1 == 2
        except ValueError:
            assert 1 == 1


class TestIteratableArray(PyexcelIteratorBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.array = []
        for i in [0, 4, 8]:
            array = [i+1, i+2, i+3, i+4]
            self.array.append(array)
        self.iteratable = pyexcel.iterators.Matrix(self.array)


class TestIteratorWithPlainReader(PyexcelIteratorBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.csv"
        create_sample_file2(self.testfile)
        self.iteratable = pyexcel.PlainReader(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestIterator(PyexcelIteratorBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.csv"
        create_sample_file2(self.testfile)
        self.iteratable = pyexcel.Reader(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestHatIterators:
    def setUp(self):
        self.testfile = "test.csv"
        self.content = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3]
        ]
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()

    def test_hat_column_iterator(self):
        r = pyexcel.SeriesReader(self.testfile)
        result = pyexcel.utils.to_dict(r)
        actual = {
            "X": [1, 1, 1, 1, 1],
            "Y": [2, 2, 2, 2, 2],
            "Z": [3, 3, 3, 3, 3],
        }
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
