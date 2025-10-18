
One liners
================================================================================

This section shows you how to get data from your excel files and how to
export data to excel files in **one line**

Read from the excel files
--------------------------------------------------------------------------------

Get a list of dictionaries
********************************************************************************

.. testcode::
   :hide:

   >>> import os
   >>> import pyexcel as p
   >>> content="""
   ... Name,Period,Representative Composers
   ... Medieval,c.1150-c.1400,"Machaut, Landini"
   ... Renaissance,c.1400-c.1600,"Gibbons, Frescobaldi"
   ... Baroque,c.1600-c.1750,"JS Bach, Vivaldi"
   ... Classical,c.1750-c.1830,"Joseph Haydn, Wolfgan Amadeus Mozart"
   ... Early Romantic,c.1830-c.1860,"Chopin, Mendelssohn, Schumann, Liszt"
   ... Late Romantic,c.1860-c.1920,"Wagner,Verdi"
   ... Modernist,20th century,"Sergei Rachmaninoff,Calude Debussy"
   ... """.strip()
   >>> sheet = p.get_sheet(file_content=content, file_type='csv')
   >>> sheet.save_as("your_file.xls")


Suppose you want to process `History of Classical Music <https://www.naxos.com/education/brief_history.asp>`_:


.. pyexcel-table::

   ---pyexcel:History of Classical Music---
   Name,Period,Representative Composers
   Medieval,c.1150-c.1400,"Machaut, Landini"
   Renaissance,c.1400-c.1600,"Gibbons, Frescobaldi"
   Baroque,c.1600-c.1750,"JS Bach, Vivaldi"
   Classical,c.1750-c.1830,"Joseph Haydn, Wolfgan Amadeus Mozart"
   Early Romantic,c.1830-c.1860,"Chopin, Mendelssohn, Schumann, Liszt"
   Late Romantic,c.1860-c.1920,"Wagner,Verdi"
   Modernist,20th century,"Sergei Rachmaninoff,Calude Debussy"



Let's get a list of dictionary out from the xls file:

.. code-block:: python

   >>> records = p.get_records(file_name="your_file.xls")

And let's check what do we have:

.. code-block:: python

   >>> for row in records:
   ...     print(f"{row['Representative Composers']} are from {row['Name']} period ({row['Period']})")
   Machaut, Landini are from Medieval period (c.1150-c.1400)
   Gibbons, Frescobaldi are from Renaissance period (c.1400-c.1600)
   JS Bach, Vivaldi are from Baroque period (c.1600-c.1750)
   Joseph Haydn, Wolfgan Amadeus Mozart are from Classical period (c.1750-c.1830)
   Chopin, Mendelssohn, Schumann, Liszt are from Early Romantic period (c.1830-c.1860)
   Wagner,Verdi are from Late Romantic period (c.1860-c.1920)
   Sergei Rachmaninoff,Calude Debussy are from Modernist period (20th century)


Get two dimensional array
********************************************************************************

Instead, what if you have to use `pyexcel.get_array` to do the same:

.. code-block:: python

   >>> for row in p.get_array(file_name="your_file.xls", start_row=1):
   ...     print(f"{row[2]} are from {row[0]} period ({row[1]})")
   Machaut, Landini are from Medieval period (c.1150-c.1400)
   Gibbons, Frescobaldi are from Renaissance period (c.1400-c.1600)
   JS Bach, Vivaldi are from Baroque period (c.1600-c.1750)
   Joseph Haydn, Wolfgan Amadeus Mozart are from Classical period (c.1750-c.1830)
   Chopin, Mendelssohn, Schumann, Liszt are from Early Romantic period (c.1830-c.1860)
   Wagner,Verdi are from Late Romantic period (c.1860-c.1920)
   Sergei Rachmaninoff,Calude Debussy are from Modernist period (20th century)


where `start_row` skips the header row.


Get a dictionary
********************************************************************************

You can get a dictionary too:

.. code-block:: python

   >>> my_dict = p.get_dict(file_name="your_file.xls", name_columns_by_row=0)

And let's have a look inside:

.. code-block:: python

   >>> from pyexcel._compact import OrderedDict
   >>> isinstance(my_dict, OrderedDict)
   True
   >>> for key, values in my_dict.items():
   ...     print(key + " : " + ','.join([str(item) for item in values]))
   Name : Medieval,Renaissance,Baroque,Classical,Early Romantic,Late Romantic,Modernist
   Period : c.1150-c.1400,c.1400-c.1600,c.1600-c.1750,c.1750-c.1830,c.1830-c.1860,c.1860-c.1920,20th century
   Representative Composers : Machaut, Landini,Gibbons, Frescobaldi,JS Bach, Vivaldi,Joseph Haydn, Wolfgan Amadeus Mozart,Chopin, Mendelssohn, Schumann, Liszt,Wagner,Verdi,Sergei Rachmaninoff,Calude Debussy


Please note that my_dict is an OrderedDict.

Get a dictionary of two dimensional array
********************************************************************************

.. testcode::
   :hide:

   >>> a_dictionary_of_two_dimensional_arrays = {
   ...      'Top Violinist':
   ...          [
   ...              ["Name", "Period", "Nationality"],
   ...              ["Antonio Vivaldi", "1678-1741", "Italian"],
   ...              ["Niccolo Paganini","1782-1840", "Italian"],
   ...              ["Pablo de Sarasate","1852-1904", "Spainish"],
   ...              ["Eugene Ysaye", "1858-1931", "Belgian"],
   ...              ["Fritz Kreisler", "1875-1962", "Astria-American"],
   ...              ["Jascha Heifetz", "1901-1987", "Russian-American"],
   ...              ["David Oistrakh", "1908-1974", "Russian"],
   ...              ["Yehundi Menuhin","1916-1999", "American"],
   ...              ["Itzhak Perlman","1945-", "Israeli-American"],
   ...              ["Hilary Hahn","1979-","American"]
   ...          ],
   ...      'Noteable Violin Makers':
   ...          [
   ...              ['Maker', 'Period', 'Country'],
   ...              ['Antonio Stradivari', '1644-1737', 'Cremona, Italy'],
   ...              ['Giovanni Paolo Maggini', '1580-1630', 'Botticino, Italy'],
   ...              ['Amati Family', '1500-1740', 'Cremona, Italy'],
   ...              ['Guarneri Family', '1626-1744', 'Cremona, Italy'],
   ...              ['Rugeri Family', '1628-1719', 'Cremona, Italy'],
   ...              ['Carlo Bergonzi', '1683-1747', 'Cremona, Italy'],
   ...              ['Jacob Stainer', '1617-1683', 'Austria'],
   ...          ],
   ...      'Most Expensive Violins':
   ...          [
   ...              ['Name', 'Estimated Value', 'Location'],
   ...              ['Messiah Stradivarious', '$ 20,000,000', 'Ashmolean Museum in Oxford, England'],
   ...              ['Vieuxtemps Guarneri', '$ 16,000,000', 'On loan to Anne Akiko Meyers'],
   ...              ['Lady Blunt', '$ 15,900,000', 'Anonymous bidder'],
   ...          ]
   ...  }
   >>> p.save_book_as(bookdict=a_dictionary_of_two_dimensional_arrays, dest_file_name="book.xls")


Suppose you have a multiple sheet book as the following:


.. pyexcel-table::

   ---pyexcel:Top Violinist---
   Name,Period,Nationality
   Antonio Vivaldi,1678-1741,Italian
   Niccolo Paganini,1782-1840,Italian
   Pablo de Sarasate,1852-1904,Spainish
   Eugene Ysaye,1858-1931,Belgian
   Fritz Kreisler,1875-1962,Astria-American
   Jascha Heifetz,1901-1987,Russian-American
   David Oistrakh,1908-1974,Russian
   Yehundi Menuhin,1916-1999,American
   Itzhak Perlman,1945-,Israeli-American
   Hilary Hahn,1979-,American
   ---pyexcel---
   ---pyexcel:Noteable Violin Makers---
   Maker,Period,Country
   Antonio Stradivari,1644-1737,"Cremona, Italy"
   Giovanni Paolo Maggini,1580-1630,"Botticino, Italy"
   Amati Family,1500-1740,"Cremona, Italy"
   Guarneri Family,1626-1744,"Cremona, Italy"
   Rugeri Family,1628-1719,"Cremona, Italy"
   Carlo Bergonzi,1683-1747,"Cremona, Italy"
   Jacob Stainer,1617-1683,Austria
   ---pyexcel---
   ---pyexcel:Most Expensive Violins---
   Name,Estimated Value,Location
   Messiah Stradivarious,"$ 20,000,000","Ashmolean Museum in Oxford, England"
   Vieuxtemps Guarneri,"$ 16,000,000",On loan to Anne Akiko Meyers
   Lady Blunt,"$ 15,900,000",Anonymous bidder



Here is the code to obtain those sheets as a single dictionary:

.. code-block:: python

   >>> book_dict = p.get_book_dict(file_name="book.xls")

And check:

.. code-block:: python

   >>> isinstance(book_dict, OrderedDict)
   True
   >>> import json
   >>> for key, item in book_dict.items():
   ...     print(json.dumps({key: item}))
   {"Most Expensive Violins": [["Name", "Estimated Value", "Location"], ["Messiah Stradivarious", "$ 20,000,000", "Ashmolean Museum in Oxford, England"], ["Vieuxtemps Guarneri", "$ 16,000,000", "On loan to Anne Akiko Meyers"], ["Lady Blunt", "$ 15,900,000", "Anonymous bidder"]]}
   {"Noteable Violin Makers": [["Maker", "Period", "Country"], ["Antonio Stradivari", "1644-1737", "Cremona, Italy"], ["Giovanni Paolo Maggini", "1580-1630", "Botticino, Italy"], ["Amati Family", "1500-1740", "Cremona, Italy"], ["Guarneri Family", "1626-1744", "Cremona, Italy"], ["Rugeri Family", "1628-1719", "Cremona, Italy"], ["Carlo Bergonzi", "1683-1747", "Cremona, Italy"], ["Jacob Stainer", "1617-1683", "Austria"]]}
   {"Top Violinist": [["Name", "Period", "Nationality"], ["Antonio Vivaldi", "1678-1741", "Italian"], ["Niccolo Paganini", "1782-1840", "Italian"], ["Pablo de Sarasate", "1852-1904", "Spainish"], ["Eugene Ysaye", "1858-1931", "Belgian"], ["Fritz Kreisler", "1875-1962", "Astria-American"], ["Jascha Heifetz", "1901-1987", "Russian-American"], ["David Oistrakh", "1908-1974", "Russian"], ["Yehundi Menuhin", "1916-1999", "American"], ["Itzhak Perlman", "1945-", "Israeli-American"], ["Hilary Hahn", "1979-", "American"]]}


.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("book.xls")


Write data
---------------------------------------------

Export an array
**********************

Suppose you have the following array:

.. code-block:: python

   >>> data = [['G', 'D', 'A', 'E'], ['Thomastik-Infield Domaints', 'Thomastik-Infield Domaints', 'Thomastik-Infield Domaints', 'Pirastro'], ['Silver wound', '', 'Aluminum wound', 'Gold Label Steel']]

And here is the code to save it as an excel file :

.. code-block:: python

   >>> p.save_as(array=data, dest_file_name="example.xls")

Let's verify it:

.. code-block:: python

    >>> p.get_sheet(file_name="example.xls")
    pyexcel_sheet1:
    +----------------------------+----------------------------+----------------------------+------------------+
    | G                          | D                          | A                          | E                |
    +----------------------------+----------------------------+----------------------------+------------------+
    | Thomastik-Infield Domaints | Thomastik-Infield Domaints | Thomastik-Infield Domaints | Pirastro         |
    +----------------------------+----------------------------+----------------------------+------------------+
    | Silver wound               |                            | Aluminum wound             | Gold Label Steel |
    +----------------------------+----------------------------+----------------------------+------------------+

.. testcode::
   :hide:

   >>> import os
   >>> os.unlink("example.xls")

And here is the code to save it as a csv file :

.. code-block:: python

   >>> p.save_as(array=data,
   ...           dest_file_name="example.csv",
   ...           dest_delimiter=':')

Let's verify it:

.. code-block:: python

    >>> with open("example.csv") as f:
    ...     for line in f.readlines():
    ...         print(line.rstrip())
    ...
    G:D:A:E
    Thomastik-Infield Domaints:Thomastik-Infield Domaints:Thomastik-Infield Domaints:Pirastro
    Silver wound::Aluminum wound:Gold Label Steel

Export a list of dictionaries
**********************************

.. code-block:: python

    >>> records = [
    ...     {"year": 1903, "country": "Germany", "speed": "206.7km/h"},
    ...     {"year": 1964, "country": "Japan", "speed": "210km/h"},
    ...     {"year": 2008, "country": "China", "speed": "350km/h"}
    ... ]
    >>> p.save_as(records=records, dest_file_name='high_speed_rail.xls')


Export a dictionary of single key value pair
********************************************************************************

.. code-block:: python

    >>> henley_on_thames_facts = {
    ...     "area": "5.58 square meters",
    ...     "population": "11,619",
    ...     "civial parish": "Henley-on-Thames",
    ...     "latitude": "51.536",
    ...     "longitude": "-0.898"
    ... }
    >>> p.save_as(adict=henley_on_thames_facts, dest_file_name='henley.xlsx')


Export a dictionary of single dimensonal array
********************************************************************************

.. code-block:: python

    >>> ccs_insights = {
    ...     "year": ["2017", "2018", "2019", "2020", "2021"],
    ...     "smart phones": [1.53, 1.64, 1.74, 1.82, 1.90],
    ...     "feature phones": [0.46, 0.38, 0.30, 0.23, 0.17]
    ... }
    >>> p.save_as(adict=ccs_insights, dest_file_name='ccs.csv')


Export a dictionary of two dimensional array as a book
********************************************************************************

Suppose you want to save the below dictionary to an excel file :

.. code-block:: python

   >>> a_dictionary_of_two_dimensional_arrays = {
   ...      'Top 3 Aircraft Manufacturers':
   ...          [
   ...              ['Name', 'Revenue'],
   ...              ['Lockheed Martin', '65.4 billion USD'],
   ...              ['Airbus', '78.9 billion USD'],
   ...              ['Boeing', '58.16 billion USD']
   ...          ],
   ...      'Top 3 Airlines':
   ...          [
   ...              ['Name', 'Country', 'Revenue'],
   ...              ['Delta Air Lines', 'US', 61.6],
   ...              ['American Airlines Holdings', 'US', 57.1],
   ...              ['American Airlines Group', 'US', 54.2]
   ...          ],
   ...      'Biggest 3 Airoplanes':
   ...          [
   ...              ['Model', 'Passenger limt'],
   ...              ['Airbus A380-800', 853],
   ...              ['Boeing 747-400', 660],
   ...              ['Boeing 747-8', 605]
   ...          ]
   ...  }

Here is the code:

.. code-block:: python

   >>> p.save_book_as(
   ...    bookdict=a_dictionary_of_two_dimensional_arrays,
   ...    dest_file_name="book.xls"
   ... )

If you want to preserve the order of sheets in your dictionary, you have to
pass on an ordered dictionary to the function itself. For example:

.. code-block:: python

   >>> data = OrderedDict()
   >>> data.update({"Sheet 2": a_dictionary_of_two_dimensional_arrays['Top 3 Airlines']})
   >>> data.update({"Sheet 1": a_dictionary_of_two_dimensional_arrays['Top 3 Aircraft Manufacturers']})
   >>> data.update({"Sheet 3": a_dictionary_of_two_dimensional_arrays['Biggest 3 Airoplanes']})
   >>> p.save_book_as(bookdict=data, dest_file_name="book.xls")

Let's verify its order:

.. code-block:: python

   >>> book_dict = p.get_book_dict(file_name="book.xls")
   >>> for key, item in book_dict.items():
   ...     print(json.dumps({key: item}))
   {"Sheet 2": [["Name", "Country", "Revenue"], ["Delta Air Lines", "US", 61.6], ["American Airlines Holdings", "US", 57.1], ["American Airlines Group", "US", 54.2]]}
   {"Sheet 1": [["Name", "Revenue"], ["Lockheed Martin", "65.4 billion USD"], ["Airbus", "78.9 billion USD"], ["Boeing", "58.16 billion USD"]]}
   {"Sheet 3": [["Model", "Passenger limt"], ["Airbus A380-800", 853], ["Boeing 747-400", 660], ["Boeing 747-8", 605]]}

Please notice that "Sheet 2" is the first item in the *book_dict*, meaning the order of sheets are preserved.


Transcoding
-------------------------------------------

.. note::

   Please note that `pyexcel-cli` can perform file transcoding at command line.
   No need to open your editor, save the code, then python run.

.. testcode::
   :hide:

   >>> import datetime
   >>> data = [
   ...    ["Country", "New US tariffs, %", "Tariffs charged to the USA"],
   ...    ["China", 34, 67],
   ...    ["EU", 20, 39],
   ...    ["United Kingdom", 10, 10]
   ... ]
   >>> p.save_as(array=data, dest_file_name="trump_tariffs.xls")


The following code does a simple file format transcoding from xls to csv:

.. code-block:: python

   >>> p.save_as(file_name="trump_tariffs.xls", dest_file_name="trump_tariffs.csv")

Again it is really simple. Let's verify what we have gotten:

.. code-block:: python

   >>> sheet = p.get_sheet(file_name="trump_tariffs.csv")
   >>> sheet
   trump_tariffs.csv:
   +----------------+-------------------+----------------------------+
   | Country        | New US tariffs, % | Tariffs charged to the USA |
   +----------------+-------------------+----------------------------+
   | China          | 34                | 67                         |
   +----------------+-------------------+----------------------------+
   | EU             | 20                | 39                         |
   +----------------+-------------------+----------------------------+
   | United Kingdom | 10                | 10                         |
   +----------------+-------------------+----------------------------+


.. NOTE::

   Please note that csv(comma separate value) file is pure text file. Formula, charts, images and formatting in xls file will disappear no matter which transcoding tool you use. Hence, pyexcel is a quick alternative for this transcoding job.


Let use previous example and save it as xlsx instead

.. code-block:: python

   >>> p.save_as(file_name="trump_tariffs.xls",
   ...           dest_file_name="trump_tariffs.xlsx") # change the file extension

Again let's verify what we have gotten:

.. code-block:: python

   >>> sheet = p.get_sheet(file_name="trump_tariffs.xlsx")
   >>> sheet
   pyexcel_sheet1:
   +----------------+-------------------+----------------------------+
   | Country        | New US tariffs, % | Tariffs charged to the USA |
   +----------------+-------------------+----------------------------+
   | China          | 34                | 67                         |
   +----------------+-------------------+----------------------------+
   | EU             | 20                | 39                         |
   +----------------+-------------------+----------------------------+
   | United Kingdom | 10                | 10                         |
   +----------------+-------------------+----------------------------+


Excel book merge and split operation in one line
--------------------------------------------------------------------------------

Merge all excel files in directory into  a book where each file become a sheet
********************************************************************************

The following code will merge every excel files into one file, say "output.xls":

.. code-block:: python

    from pyexcel.cookbook import merge_all_to_a_book
    import glob


    merge_all_to_a_book(glob.glob("your_csv_directory\*.csv"), "output.xls")

You can mix and match with other excel formats: xls, xlsm and ods. For example, if you are sure you have only xls, xlsm, xlsx, ods and csv files in `your_excel_file_directory`, you can do the following:

.. code-block:: python

    from pyexcel.cookbook import merge_all_to_a_book
    import glob


    merge_all_to_a_book(glob.glob("your_excel_file_directory\*.*"), "output.xls")

Split a book into single sheet files
****************************************

.. testcode::
   :hide:

    >>> content = {
    ...     'Sheet 1':
    ...         [
    ...             [1.0, 2.0, 3.0],
    ...             [4.0, 5.0, 6.0],
    ...             [7.0, 8.0, 9.0]
    ...         ],
    ...     'Sheet 2':
    ...         [
    ...             ['X', 'Y', 'Z'],
    ...             [1.0, 2.0, 3.0],
    ...             [4.0, 5.0, 6.0]
    ...         ],
    ...     'Sheet 3':
    ...         [
    ...             ['O', 'P', 'Q'],
    ...             [3.0, 2.0, 1.0],
    ...             [4.0, 3.0, 2.0]
    ...         ]
    ... }
    >>> book = p.Book(content)
    >>> book.save_as("megabook.xls")


Suppose you have many sheets in a work book and you would like to separate each into a single sheet excel file. You can easily do this:

.. code-block:: python

   >>> from pyexcel.cookbook import split_a_book
   >>> split_a_book("megabook.xls", "output.xls")
   >>> import glob
   >>> outputfiles = glob.glob("*_output.xls")
   >>> for file in sorted(outputfiles):
   ...     print(file)
   ...
   Sheet 1_output.xls
   Sheet 2_output.xls
   Sheet 3_output.xls

for the output file, you can specify any of the supported formats

.. testcode::
   :hide:

   >>> os.unlink("Sheet 1_output.xls")
   >>> os.unlink("Sheet 2_output.xls")
   >>> os.unlink("Sheet 3_output.xls")

Extract just one sheet from a book
*************************************


Suppose you just want to extract one sheet from many sheets that exists in a work book and you would like to separate it into a single sheet excel file. You can easily do this:

.. code-block:: python

    >>> from pyexcel.cookbook import extract_a_sheet_from_a_book
    >>> extract_a_sheet_from_a_book("megabook.xls", "Sheet 1", "output.xls")
    >>> if os.path.exists("Sheet 1_output.xls"):
    ...     print("Sheet 1_output.xls exists")
    ...
    Sheet 1_output.xls exists

for the output file, you can specify any of the supported formats

.. testcode::
   :hide:

   >>> os.unlink("high_speed_rail.xls")
   >>> os.unlink("Sheet 1_output.xls")
   >>> os.unlink("megabook.xls")
   >>> os.unlink('trump_tariffs.xls')
   >>> os.unlink('trump_tariffs.csv')
   >>> os.unlink('trump_tariffs.xlsx')
   >>> os.unlink('henley.xlsx')
   >>> os.unlink('ccs.csv')
   >>> os.unlink("book.xls")
   >>> os.unlink("your_file.xls")
   >>> os.unlink("example.csv")
