import pyexcel as pe
import datetime
from textwrap import dedent
from db import Session, Base, Pyexcel, engine

class TestSQL:
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
Sheet Name: pyexcel
+------------+----+-------+--------+
| birth      | id | name  | weight |
+------------+----+-------+--------+
| 2014-11-11 | 0  | Adam  | 11.25  |
+------------+----+-------+--------+
| 2014-11-12 | 1  | Smith | 12.25  |
+------------+----+-------+--------+""").strip('\n')
        assert str(sheet) == content

class TestEmptyTable:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def test_empty_table(self):
        sheet = pe.load_from_sql(Session(), Pyexcel)
        assert sheet is not None
