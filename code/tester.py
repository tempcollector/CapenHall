#!/usr/bin/python
import reader
import credentials as c

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

def main():
    databaseFile = '../files/temperature.db'
    filename = '/sys/bus/w1/devices/28-00044a3b10ff/w1_slave'
    interface = 'eth0'
    place = 'Kitchen'

    macAddr = reader.getMACAddr(interface)
    (time, celcius, farenheit) = reader.readTemperature(filename)

    spreadsheet = {
        'ID' : '1PY-eVqQs-2LdJu3gZ2tdaBRBNFh0gpI1GdSWpL_yXd8',
        'rangeName' : 'A1:B1',
        'valueInputOption' : 'RAW',
        'ROWS' : [time, celcius, farenheit, place]
    }

    #location = {macAddr: place}
    database.uploadToDB(databaseFile, (t, c, f), location[hwAddr])
    credentials = c.get_credentials()
    http_auth = credentials.authorize(Http())
    service = build('sheets', 'v4', http = http_auth)

    values = [spreadsheet['ROWS']]
    body = {'values': values}
    result = service.spreadsheets().values().append(
        spreadsheetId = spreadsheet['ID'],
        range = spreadsheet['rangeName'],
        valueInputOption = spreadsheet['valueInputOption'],
        body = body).execute()
    print 'Uploading to Google Sheets...'

if __name__ == '__main__':
    main()
