#!/usr/bin/python
import sqlite3

CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS temperature
    (recordedTime TEXT,
    celcius INTEGER,
    farenheit INTEGER,
    location TEXT)'''
INSERT_VALUES = 'INSERT INTO temperature VALUES (?,?,?,?)'

def uploadToDB(database, (time, celcius, farenheit), location):
    """Uploads temperature information along its location of origin to a
    sqlite3 database."""
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    try:
        cursor.execute(CREATE_TABLE)
        data = (time, celcius, farenheit, location)
        cursor.execute(INSERT_VALUES, data)
        connection.commit()
    except sqlite3.Error as error:
        print error.message
