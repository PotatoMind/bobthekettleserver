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
import RPi.GPIO as GPIO
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import subprocess

# Server Variables
modes = {'boil': 100, 'hot':65, 'warm': 35}
# Raspberry Pi pin setup
tmp_sensor = 27
# Initialize the Flask application
application = Flask(__name__)
# Initialize the temperature sensor object
sensor = W1ThermSensor()
# Setup GPIO ports
GPIO.setmode(GPIO.BCM)

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D21)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
cmd = ['hostname', '-I']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
o, e = proc.communicate()
lcd.message = o.decode('ascii') + '\nPort: 5000'

# Main page of the website
@application.route("/")
def index():
    return 'Hello World!'

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

# Run the server
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=80)


def flip_switch(switch):
    if switch:
        try:
            GPIO.output(27, GPIO.HIGH)
            time.sleep(5)
        except:
            print("Some error")
    else:
        try:
            GPIO.output(27, GPIO.LOW)
            time.sleep(5)
        except:
            print("Some error")