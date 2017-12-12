#!/usr/bin/python

import MySQLdb, serial, sys, datetime, time
db = MySQLdb.connect("localhost","root", "root","dbName")

def sqlPush(temperature, humidity, timeAndDate):

      cursor = db.cursor()

      sql = "INSERT INTO DATA (Lampo, Aika_paiva, Kosteus) \
             VALUES ('%s','%s', '%s')" % \
             (temperature, timeAndDate, humidity)
      try:
         cursor.execute(sql)
         db.commit()
         print(timeAndDate)
      except:
         print("Error: unable to push data")
         db.rollback()

      return

with serial.Serial(port='/dev/ttyACM0', baudrate=9600) as ser:

    if ser.isOpen():

      ser.readline()

    while ser.isOpen():

      serialData = (ser.readline()).decode("utf-8")
      serialData = serialData[:-2]
      timeAndDate = datetime.datetime.now()
      timeAndDate = str(timeAndDate)
      timeAndDate = timeAndDate[:-7]
      temperatureDetector = "C" in serialData
      humidityDetector = "H" in serialData

      if(temperatureDetector == 1):
        serialData = serialData[:-1]
        temperature = serialData

      if(humidityDetector == 1):
        serialData = serialData[:-1]
        humidity = serialData
        sqlPush(temperature, humidity, timeAndDate)
