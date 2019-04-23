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
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import subprocess
from waitress import serve
import sqlite3

# Server Variables
modes = {'boil': 90, 'hot': 60, 'warm': 30}
# Raspberry Pi pin setup
tmp_sensor = 27
# Initialize the Flask application
application = Flask(__name__)
# Initialize the temperature sensor object
try:
    sensor = W1ThermSensor()
except:
    print("DEAD")
# Setup GPIO ports
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
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

# DB Helper Functions
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_db():
    # sqlite db
    conn = create_connection('server.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS log
                 (datetime, command, device, response)''')
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return 'Created DB'
    
def save_db(log):
    # sqlite db
    conn = create_connection('server.db')
    c = conn.cursor()

    # Create table
    sql = '''INSERT INTO log(datetime, command, device, response)
        VALUES(?, ?, ?, ?) '''
    c.execute(sql, log)
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return 'Added log'

def get_db():
    # sqlite db
    conn = create_connection('server.db')
    c = conn.cursor()

    # Create table
    sql = '''GET * FROM log'''
    res = c.execute(sql)
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return res
# Create the database
create_db()

# Main page of the website
@application.route("/")
def index():
    return 'Hello World!'

# Sets the temperature of the water heater
@application.route('/temperature/<mode>', methods=['GET', 'POST'])
def temperature(mode):
    if request.method == 'GET':
        json = {
            "c":  round(sensor.get_temperature(), 2),
            "f": round(sensor.get_temperature(W1ThermSensor.DEGREES_F), 2),
            "k": round(sensor.get_temperature(W1ThermSensor.KELVIN), 2)
        }
        return str(json)
    else:
        if mode in modes:
            return set_temperature(mode)
        else:
            json = {
                "c":  round(sensor.get_temperature(), 2),
                "f": round(sensor.get_temperature(W1ThermSensor.DEGREES_F), 2),
                "k": round(sensor.get_temperature(W1ThermSensor.KELVIN), 2)
            }
            save_db((datetime.datetime.now(), request.path, request.remote_addr, str(json)))
            return str(json)

# Sets the time to keep the water heater heated
@application.route('/heat/<mode>/<int:duration>', methods=['POST'])
def heat(mode, duration):
    if mode in modes:
        set_temperature(mode)
    else:
        return 'Temperature mode not found: ' + mode
    start_time = time.time()
    end_time = time.time()
    flip_switch(1)
    while (end_time - start_time < duration):
        set_temperature(mode)
        print(end_time - start_time)
        end_time = time.time()
        time.sleep(1)
    flip_switch(0)
    save_db((datetime.datetime.now(), request.path, request.remote_addr, 'Done'))
    return 'Done'

@application.route('/stats', methods=['GET'])
def stats():
    rows = get_db()
    return 'Some crazy stats about the kettle that we don\'t have yet.'

@application.route('/switch/<value>', methods=['GET'])
def switch(value):
    if value == 'on':
        flip_switch(True)
    elif value == 'off':
        flip_switch(False)
    return 'Done did the thing'

def set_temperature(mode):
    print('Setting temperature mode to ' + mode + ' at ' + str(modes[mode]))
    temp = modes[mode]
    if (round(sensor.get_temperature(), 2) < temp):
        flip_switch(1)
        while (round(sensor.get_temperature(), 2) < temp):
            print(round(sensor.get_temperature(), 2))
            time.sleep(1)
        flip_switch(0)
        return 'Done'
    else:
        return 'Already heated'

def flip_switch(switch):
    if switch:
        try:
            GPIO.output(27, GPIO.HIGH)
            time.sleep(5)
        except e:
            print(e)
    else:
        try:
            GPIO.output(27, GPIO.LOW)
            time.sleep(5)
        except:
            print("Some error")

if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=5000)