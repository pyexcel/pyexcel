"""
pyexcel_server.py
:copyright: (c) 2014 by C. W.
:license: GPL v3

This shows how to use pyexcel to handle excel file upload. In order
to evaluate it, please install Flask::

    pip install Flask
    python flaskserver.py

Then visit http://localhost:5000/upload

Flask is a micro framework for web development. For more infomation,
please visit: http://flask.pocoo.org
"""

from flask import Flask, request, render_template, jsonify
import pyexcel as pe
app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'excel' in request.files:
        # handle file upload
        filename = request.files['excel'].filename
        extension = filename.split(".")[1]
        # Obtain the file extension and content
        # pass a tuple instead of a file name
        sheet = pe.load_from_memory(extension, request.files['excel'].read())
        # then use it as usual
        data = sheet.to_dict()
        # respond with a json
        return jsonify({"result":data})
    return render_template('upload.html')
    
if __name__ == "__main__":
    # start web server
    app.run()
