from flask import Flask
from flask import request
from flask import send_file
import random
import string
from werkzeug.utils import secure_filename
import zipfile
from io import BytesIO
import time
import datetime
from os.path import basename
import os
import numpy as np
import json
import PIL
from PIL import Image

# Initialize the Flask application
application = Flask(__name__)

# Main page of the website
@application.route("/")
def index():
    return "Hello World!"

# Upload GET and POST request for images
@application.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # If it's a POST request, then we are putting something in the DB
    if request.method == 'POST':
        # This gets the file from the POST request
        #f = request.files['the_file']
        # Sends file to DB and saves in images/ folder
        #results = fileToDB(f)
	#return results
        return
    if request.method == 'GET':
        ### Gets (currently all) paths from DB
        ### Needs to return actual images!
	#minRow = request.args.get('minRow')
	#maxRow = request.args.get('maxRow')
	#images = None
	#if minRow is not None and maxRow is not None:
        #	return filesFromDB(minRow, maxRow)
	#else:
	#	return filesFromDB()
        return

# A function to generate 7 random characters
if __name__ == '__main__':
    application.run(host='0.0.0.0')
