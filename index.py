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
from w1thermsensor import W1ThermSensor

# Server Variables
modes = {'boil': 100, 'hot':65, 'warm': 35}
# Initialize the Flask application
application = Flask(__name__)
# Initialize the temperature sensor object
sensor = W1ThermSensor()

# Main page of the website
@application.route("/")
def index():
    return "Hello World!"

# Sets the temperature of the water heater
@application.route('/temperature/<mode>', methods=['GET', 'POST'])
def temperature(mode):
    if request.method == 'GET':
        temperature_in_celsius = sensor.get_temperature()
        temperature_in_fahrenheit = sensor.get_temperature(W1ThermSensor.DEGREES_F)
        return 'The temperature is ' + str(temperature_in_fahrenheit)
    else:
        if mode in modes:
                # Do something
                return 'Setting temperature mode to ' + mode + ' at ' + str(modes[mode])
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
