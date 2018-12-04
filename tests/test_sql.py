import datetime
from textwrap import dedent
from unittest import TestCase

from db import Base, Pyexcel, Session, engine

import pyexcel as pe
from nose.tools import eq_, raises


class TestSQL(TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        p1 = Pyexcel(
            id=0, name="Adam", weight=11.25, birth=datetime.date(2014, 11, 11)
        )
        session = Session()
        session.add(p1)
        p1 = Pyexcel(
            id=1, name="Smith", weight=12.25, birth=datetime.date(2014, 11, 12)
        )
        session.add(p1)
        session.commit()

    def test_sql(self):
        sheet = pe.get_sheet(session=Session(), table=Pyexcel)
        content = dedent(
            """
        pyexcel:
        +------------+----+-------+--------+
        | birth      | id | name  | weight |
        +------------+----+-------+--------+
        | 2014-11-11 | 0  | Adam  | 11.25  |
        +------------+----+-------+--------+
        | 2014-11-12 | 1  | Smith | 12.25  |
        +------------+----+-------+--------+"""
        ).strip("\n")
        self.assertEqual(str(sheet), content)

    def test_sql_sheet(self):
        sheet = pe.get_sheet(
            session=Session(),
            table=Pyexcel,
            sheet_name="custom sheet",
            export_columns=["weight", "birth"],
        )
        content = dedent(
            """
        custom sheet:
        +--------+------------+
        | weight | birth      |
        +--------+------------+
        | 11.25  | 2014-11-11 |
        +--------+------------+
        | 12.25  | 2014-11-12 |
        +--------+------------+"""
        ).strip("\n")
        self.assertEqual(str(sheet), content)


class TestEmptyTable:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def test_empty_table(self):
        sheet = pe.get_sheet(session=Session(), table=Pyexcel)
        assert sheet is not None

    @raises(Exception)
    def test_save_as(self):
        data = [
            ["birth", "name", "weight"],
            [datetime.date(2017, 1, 11), "Adam", 3.0],
        ]
        session = Session()
        pe.save_as(array=data, dest_session=session, dest_table=Pyexcel)
        sheet = pe.get_sheet(session=session, table=Pyexcel)
        eq_(str(sheet), "")

    def test_save_as_1(self):
        data = [
            ["birth", "name", "weight"],
            [datetime.date(2017, 1, 11), "Adam", 3.0],
        ]
        session = Session()
        pe.save_as(
            array=data,
            name_columns_by_row=0,
            dest_session=session,
            dest_table=Pyexcel,
        )
        sheet = pe.get_sheet(session=session, table=Pyexcel)
        print(sheet)
        content = dedent(
            """
        pyexcel:
        +------------+----+------+--------+
        | birth      | id | name | weight |
        +------------+----+------+--------+
        | 2017-01-11 | 1  | Adam | 3.0    |
        +------------+----+------+--------+"""
        ).strip("\n")
        eq_(str(sheet), content)
