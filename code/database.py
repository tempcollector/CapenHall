#!/usr/bin/python
import sqlite3
import os

CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS temperature(
    recordedTime TEXT,
    recordedDate TEXT,
    location TEXT,
    recordedZone TEXT,
    celcius INTEGER,
    farenheit INTEGER,
    updatedToSheets INTEGER
)'''
def __getProjectDir():
    """Gets the project directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def getDBFile():
    projectDir = __getProjectDir()
    databaseFile = os.path.join(projectDir, 'files/temperature.db')
    return databaseFile
def setUpdatedToSheets():
    database = getDBFile()
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        try:
            SELECT_VALUES = '''UPDATE temperature
                SET updatedToSheets = ?
                WHERE  updatedToSheets = ?'''
            data = (True, False)
            print 'Updating updated files to sheets...'
            cursor.execute(SELECT_VALUES, data)
            connection.commit()
        except sqlite3.Error as error:
            print error.message
def uploadToDB((timeDateZone, celcius, farenheit), location):
    """Uploads temperature information along its location of origin to a
    sqlite3 database."""
    database = getDBFile()
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        try:
            INSERT_VALUES = 'INSERT INTO temperature VALUES (?,?,?,?,?,?,?)'
            time = timeDateZone[0]; date = timeDateZone[1]; zone = timeDateZone[2]
            updatedToSheets = False
            data = (time, date, location, zone, celcius, farenheit, updatedToSheets)
            print 'Uploading to database...'
            cursor.execute(CREATE_TABLE)
            cursor.execute(INSERT_VALUES, data)
            connection.commit()
        except sqlite3.Error as error:
            print error.message
def getFromDB(updatedToSheets):
    """Retrieves records from the temperature table that have not yet been
    updated to Google Sheets."""
    database = getDBFile()
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        try:
            SELECT_VALUES = '''SELECT
                recordedTime,
                recordedDate,
                location,
                recordedZone,
                celcius,
                farenheit
                FROM temperature WHERE updatedToSheets = ?'''
            data = (updatedToSheets, )
            print 'Retrieving from database...'
            cursor.execute(SELECT_VALUES, data)
            ROWS = cursor.fetchall()
            if not ROWS:
                ROWS = None
            return ROWS
        except sqlite3.Error as error:
            print error.message
