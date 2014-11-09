===============================
Work with excel files in memory
===============================

With pyexcel >=0.0.6, excel files in memory can be manipulated directly without saving it to physical disk and vice versa. This is useful in excel file handling at file upload or in excel file download. The way to enable it is to pass a tuple instead of file name to an excel reader or writer class. For example::

    import pyexcel

    content = "1,2,3\n3,4,5"
    sheet = pyexcel.load_from_memory(("csv", content))
    print pyexcel.to_array(sheet.rows())

As you can see, the tuple which is consisted of file type extension and the content to :class:`Reader`. 


Real example: read any supported excel and respond its content in json
----------------------------------------------------------------------

You can find a real world example in **examples/memoryfile/** directory: pyexcel_server.py. Here is the example snippet

.. code-block:: python
    :linenos:

    def upload():
        if request.method == 'POST' and 'excel' in request.files:
            # handle file upload
            filename = request.files['excel'].filename
            extension = filename.split(".")[1]
            # Obtain the file extension and content
            # pass a tuple instead of a file name
            sheet = pyexcel.load_from_memory(extension, request.files['excel'].read())
            # then use it as usual
            data = pyexcel.to_dict(sheet)
            # respond with a json
            return jsonify({"result":data})
        return render_template...

**request.files['excel']** in line 2 holds the file object. line 5 finds out the file extension. line 8 feeds in a tuple to **Book**. line 10 gives a dictionary represetation of the excel file and line 11 send the json represetation of the excel file back to client browser
