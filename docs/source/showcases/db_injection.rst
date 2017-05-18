How to inject csv data to database
==========================================

Here is `real case <http://stackoverflow.com/questions/43837878/csv-to-mysql-in-matlab-code>`_ 
in the stack-overflow. Due to the author's ignorance, the user would like
to have the code in matlab than Python. Hence, I am sharing my pyexcel solution
here.

Problem definition
-------------------------
Here is my CSV file::

    PDB_Id	123442	234335	234336	3549867
    a001	6	0	0	8
    b001	4	2	0	0
    c003	0	0	0	5

I want to put this data in a MYSQL table in the form::

    PROTEIN_ID	PROTEIN_KEY	VALUE_OF_KEY
    a001	    123442	    6
    a001	    234335	    0
    a001	    234336	    0
    a001	    3549867	    8
    b001	    123442	    4
    b001	    234335	    2
    b001	    234336	    0
    b001	    234336	    0
    c003	    123442	    0
    c003	    234335	    0
    c003	    234336	    0
    c003	    3549867	    5

I have created table with the following code:

    sql = """CREATE TABLE ALLPROTEINS (
             Protein_ID CHAR(20),
             PROTEIN_KEY INT ,
             VALUE_OF_KEY INT
             )"""

I need the code for insert.

Pyexcel solution
--------------------

.. testcode::
   :hide:

   >>> data = [
   ...     [u'PDB_Id', 123442, 234335, 234336, 3549867],
   ...     [u'a001', 6, 0, 0, 8],
   ...     [u'b001', 4, 2, 0, 0],
   ...     [u'c003', 0, 0, 0, 5]]
   >>> import pyexcel as p
   >>> p.save_as(array=data, dest_file_name='csv-to-mysql-in-matlab-code.csv',
   ...     dest_delimiter='\t')

If you could insert an id field to act as the primary key, it can be mapped using sqlalchemy's ORM::

    $ sqlite3 /tmp/stack2.db
    sqlite> CREATE TABLE ALLPROTEINS (
       ...>          ID INT,
       ...>          Protein_ID CHAR(20),
       ...>          PROTEIN_KEY INT,
       ...>          VALUE_OF_KEY INT
       ...>          );

Here is the data mapping script vis sqlalchemy:

    >>> # mapping your database via sqlalchemy
    >>> from sqlalchemy import create_engine
    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> from sqlalchemy import Column, Integer, String
    >>> from sqlalchemy.orm import sessionmaker
    
    >>> # checkout http://docs.sqlalchemy.org/en/latest/dialects/index.html
    >>> # for a different database server
    >>> engine = create_engine("sqlite:////tmp/stack2.db")
    >>> Base = declarative_base()
    >>> class Proteins(Base):
    ...     __tablename__ = 'ALLPROTEINS'
    ...     id = Column(Integer, primary_key=True, autoincrement=True) # <-- appended field
    ...     protein_id = Column(String(20))
    ...     protein_key = Column(Integer)
    ...     value_of_key = Column(Integer)
    >>> Session = sessionmaker(bind=engine)
    >>>

Here is the short script to get data inserted into the database:

    >>> import pyexcel as p
    >>> from itertools import product
    
    >>> # data insertion code starts here
    >>> sheet = p.get_sheet(file_name="csv-to-mysql-in-matlab-code.csv", delimiter='\t')
    >>> sheet.name_columns_by_row(0)
    >>> sheet.name_rows_by_column(0)
    >>> print(sheet)
    csv-to-mysql-in-matlab-code.csv:
    +------+--------+--------+--------+---------+
    |      | 123442 | 234335 | 234336 | 3549867 |
    +======+========+========+========+=========+
    | a001 | 6      | 0      | 0      | 8       |
    +------+--------+--------+--------+---------+
    | b001 | 4      | 2      | 0      | 0       |
    +------+--------+--------+--------+---------+
    | c003 | 0      | 0      | 0      | 5       |
    +------+--------+--------+--------+---------+
    >>> results = []
    >>> for protein_id, protein_key in product(sheet.rownames, sheet.colnames):
    ...     results.append([protein_id, protein_key, sheet[str(protein_id), protein_key]])
    >>> 
    >>> sheet2 = p.get_sheet(array=results)
    >>> sheet2.colnames = ['protein_id', 'protein_key', 'value_of_key']
    >>> print(sheet2)
    pyexcel_sheet1:
    +------------+-------------+--------------+
    | protein_id | protein_key | value_of_key |
    +============+=============+==============+
    | a001       | 123442      | 6            |
    +------------+-------------+--------------+
    | a001       | 234335      | 0            |
    +------------+-------------+--------------+
    | a001       | 234336      | 0            |
    +------------+-------------+--------------+
    | a001       | 3549867     | 8            |
    +------------+-------------+--------------+
    | b001       | 123442      | 4            |
    +------------+-------------+--------------+
    | b001       | 234335      | 2            |
    +------------+-------------+--------------+
    | b001       | 234336      | 0            |
    +------------+-------------+--------------+
    | b001       | 3549867     | 0            |
    +------------+-------------+--------------+
    | c003       | 123442      | 0            |
    +------------+-------------+--------------+
    | c003       | 234335      | 0            |
    +------------+-------------+--------------+
    | c003       | 234336      | 0            |
    +------------+-------------+--------------+
    | c003       | 3549867     | 5            |
    +------------+-------------+--------------+
    >>> sheet2.save_to_database(session=Session(), table=Proteins)

Here is the data inserted:

    $ sqlite3 /tmp/stack2.db
    sqlite> select * from allproteins
       ...> ;
    |a001|123442|6
    |a001|234335|0
    |a001|234336|0
    |a001|3549867|8
    |b001|123442|4
    |b001|234335|2
    |b001|234336|0
    |b001|234336|0
    |c003|123442|0
    |c003|234335|0
    |c003|234336|0
    |c003|3549867|5
