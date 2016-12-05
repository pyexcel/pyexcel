from unittest import TestCase
import pyexcel as pe
import datetime
from textwrap import dedent
from db import Session, Base, Pyexcel, engine


class TestSQL(TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        p1 = Pyexcel(id=0,
                     name="Adam",
                     weight=11.25,
                     birth=datetime.date(2014, 11, 11))
        session = Session()
        session.add(p1)
        p1 = Pyexcel(id=1,
                     name="Smith",
                     weight=12.25,
                     birth=datetime.date(2014, 11, 12))
        session.add(p1)
        session.commit()

    def test_sql(self):
        sheet = pe.load_from_sql(Session(), Pyexcel)
        content = dedent("""
        pyexcel:
        +------------+----+-------+--------+
        | birth      | id | name  | weight |
        +------------+----+-------+--------+
        | 2014-11-11 | 0  | Adam  | 11.25  |
        +------------+----+-------+--------+
        | 2014-11-12 | 1  | Smith | 12.25  |
        +------------+----+-------+--------+""").strip('\n')
        self.assertEqual(str(sheet), content)

    def test_sql_sheet(self):
        sheet = pe.get_sheet(session=Session(), table=Pyexcel, export_columns=['weight', 'birth'])
        content = dedent("""
        pyexcel:
        +--------+------------+
        | weight | birth      |
        +--------+------------+
        | 11.25  | 2014-11-11 |
        +--------+------------+
        | 12.25  | 2014-11-12 |
        +--------+------------+""").strip('\n')
        self.assertEqual(str(sheet), content)


class TestEmptyTable:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def test_empty_table(self):
        sheet = pe.load_from_sql(Session(), Pyexcel)
        assert sheet is not None
