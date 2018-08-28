Working with databases
=======================

How to import an excel sheet to a database using SQLAlchemy
-----------------------------------------------------------

.. NOTE::

   You can find the complete code of this example in examples folder on github

Before going ahead, let's import the needed components and initialize sql
engine and table base::

   >>> import os
   >>> import pyexcel as p
   >>> from sqlalchemy import create_engine
   >>> from sqlalchemy.ext.declarative import declarative_base
   >>> from sqlalchemy import Column , Integer, String, Float, Date
   >>> from sqlalchemy.orm import sessionmaker
   >>> engine = create_engine("sqlite:///birth.db")
   >>> Base = declarative_base()
   >>> Session = sessionmaker(bind=engine)

Let's suppose we have the following database model:

   >>> class BirthRegister(Base):
   ...     __tablename__='birth'
   ...     id=Column(Integer, primary_key=True)
   ...     name=Column(String)
   ...     weight=Column(Float)
   ...     birth=Column(Date)

Let's create the table::
  
   >>> Base.metadata.create_all(engine)

Now here is a sample excel file to be saved to the table:


.. pyexcel-table::
   
   ---pyexcel:data table---
   name,weight,birth     
   Adam,3.4,2015-02-03
   Smith,4.2,2014-11-12

.. testcode::
   :hide:

   >>> import datetime
   >>> data = [
   ...    ["name", "weight", "birth"],
   ...    ["Adam", 3.4, datetime.date(2015, 2, 3)],
   ...    ["Smith", 4.2, datetime.date(2014, 11, 12)]
   ... ]
   >>> p.save_as(array=data, dest_file_name="birth.xls")

Here is the code to import it:

   >>> session = Session() # obtain a sql session
   >>> p.save_as(file_name="birth.xls", name_columns_by_row=0, dest_session=session, dest_table=BirthRegister)

Done it. It is that simple. Let's verify what has been imported to make sure.

   >>> sheet = p.get_sheet(session=session, table=BirthRegister)
   >>> sheet
   birth:
   +------------+----+-------+--------+
   | birth      | id | name  | weight |
   +------------+----+-------+--------+
   | 2015-02-03 | 1  | Adam  | 3.4    |
   +------------+----+-------+--------+
   | 2014-11-12 | 2  | Smith | 4.2    |
   +------------+----+-------+--------+

.. testcode::
   :hide:

   >>> session.close()
   >>> os.unlink('birth.db')
