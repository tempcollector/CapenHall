#!/usr/bin/python
import reader
import database
import location
import credentials as c
from reader import TempSensorError

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

def main():
    databaseFile = 'temperature.db'
    tempFile = '/sys/bus/w1/devices/28-00044a3b10ff/w1_slave'
    interface = 'wlan0'

    try:
        place = location.PI[reader.getMACAddr(interface)]
        (time, celcius, farenheit) = reader.readTemperature(tempFile)
    except KeyError as error:
        print error.message, ': device not registered.'
    except TempSensorError as error:
        print place, ': ', error.message
    else:
        spreadsheet = {
            'ID' : '1PY-eVqQs-2LdJu3gZ2tdaBRBNFh0gpI1GdSWpL_yXd8',
            'rangeName' : 'A1:B1',
            'valueInputOption' : 'RAW',
            'ROWS' : [time, celcius, farenheit, place]
        }
        database.uploadToDB(databaseFile, (time, celcius, farenheit), place)
        credentials = c.get_credentials()
        http_auth = credentials.authorize(Http())
        service = build('sheets', 'v4', http = http_auth)
        values = [spreadsheet['ROWS']]
        body = {'values': values}
        print 'Uploading to Google Sheets...'
        result = service.spreadsheets().values().append(
            spreadsheetId = spreadsheet['ID'],
            range = spreadsheet['rangeName'],
            valueInputOption = spreadsheet['valueInputOption'],
            body = body).execute()

if __name__ == '__main__':
    main()
