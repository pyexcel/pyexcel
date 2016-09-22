===============================
Work with excel files in memory
===============================

Excel files in memory can be manipulated directly without saving it to physical disk and vice versa. This is useful in excel file handling at file upload or in excel file download. For example:

.. code-block:: python

    >>> import pyexcel
    >>> content = "1,2,3\n3,4,5"
    >>> sheet = pyexcel.get_sheet(file_type="csv", file_content=content)
    >>> sheet.csv
    '1,2,3\r\n3,4,5\r\n'


file type as its attributes
--------------------------------------------------------------------------------

Since version 0.3.0, each supported file types became an attribute of the Sheet and
Book class. What it means is that:

#. Read the content in memory
#. Set the content in memory 

For example, after you have your Sheet and Book instance, you could access its content in a support file type by using its dot notation. The code in previous section could be rewritten as:

.. code-block:: python

    >>> import pyexcel
    >>> content = "1,2,3\n3,4,5"
    >>> sheet = pyexcel.Sheet()
    >>> sheet.csv = content
    >>> sheet.array
    [[1, 2, 3], [3, 4, 5]]

	
Read any supported excel and respond its content in json
----------------------------------------------------------------------

You can find a real world example in **examples/memoryfile/** directory: pyexcel_server.py. Here is the example snippet

.. code-block:: python
    :linenos:
    :emphasize-lines: 4,5,8,10

    def upload():
        if request.method == 'POST' and 'excel' in request.files:
            # handle file upload
            filename = request.files['excel'].filename
            extension = filename.split(".")[-1]
            # Obtain the file extension and content
            # pass a tuple instead of a file name
            content = request.files['excel'].read()
            if sys.version_info[0] > 2:
                # in order to support python 3
                # have to decode bytes to str
                content = content.decode('utf-8')
            sheet = pe.get_sheet(file_type=extension, file_content=content)
            # then use it as usual
            sheet.name_columns_by_row(0)
            # respond with a json
            return jsonify({"result": sheet.dict})
        return render_template('upload.html')

**request.files['excel']** in line 4 holds the file object. line 5 finds out the file extension. line 13 obtains a sheet instance. line 15 uses the first row as data header. line 17 sends the json representation of the excel file back to client browser.

Write to memory and respond to download
-------------------------------------------

.. code-block:: python
    :linenos:

    data = [
        [...],
        ...
    ]
    
    @app.route('/download')
    def download():
        sheet = pe.Sheet(data)
        output = make_response(sheet.csv)
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output

**make_response** is a Flask utility to make a memory content as http response.

.. note:: 
   You can find the corresponding source code at `examples/memoryfile <https://github.com/chfw/pyexcel/tree/master/examples/memoryfile>`_

Relevant packages
=================

Readily made plugins have been made on top of this example. Here is a list of them:

============== ============================
framework      plugin/middleware/extension
============== ============================
Flask          `Flask-Excel`_
Django         `django-excel`_
Pyramid        `pyramid-excel`_
============== ============================

.. _Flask-Excel: https://github.com/chfw/Flask-Excel
.. _django-excel: https://github.com/chfw/django-excel
.. _pyramid-excel: https://github.com/chfw/pyramid-excel

And you may make your own by using `pyexcel-webio <https://github.com/chfw/pyexcel-webio>`_
