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

# Server Variables
modes = {'boil': 100, 'hot':65, 'warm': 35}

# Initialize the Flask application
application = Flask(__name__)

# Main page of the website
@application.route("/")
def index():
    return 'Hello World!'

# Sets the temperature of the water heater
@application.route('/temperature/<mode>', methods=['GET, POST'])
def temperature(mode):
    if request.method == 'GET':
        temp = 10000
        return 'The temperature is ' + temp
    else:
        if mode in modes:
                # Do something
                return 'Setting temperature mode to ' + mode + ' at ' + modes[mode]
        else:
                return 'Temperature mode not found: ' + mode

# Sets the time to keep the water heater heated
@application.route('/heat/<time>', methods=['POST'])
def heat(time):
    return 'Keeping heated for ' + time + ' seconds.'

@application.route('/stats', methods=['GET'])
def stats():
    return 'Some crazy stats about the kettle that we don\'t have yet.'

# A function to generate 7 random characters
if __name__ == '__main__':
    application.run(host='0.0.0.0')
