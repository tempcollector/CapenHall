#!/usr/bin/python
import database
import credentials as c
from httplib2 import Http
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

def main():
    updatedToSheets = False
    data = database.getFromDB(updatedToSheets)
    richardSheetID = '1PY-eVqQs-2LdJu3gZ2tdaBRBNFh0gpI1GdSWpL_yXd8'
    sheetID = '1XATRUyPfMIqiLKrpYixMT2E6hT1uwkknSBgW8v3x1ME'
    if data != None:
        ROWS = list()
        for row in data:
            ROWS.append(list(row))
        spreadsheet = {
                    'ID' : sheetID,
                    'rangeName' : 'A1:F1',
                    'valueInputOption' : 'RAW',
                    'ROWS' : ROWS
        }
        credentials = c.get_credentials()
        http_auth = credentials.authorize(Http())
        service = build('sheets', 'v4', http = http_auth)
        values = spreadsheet['ROWS']
        body = {'values': values}
        print 'Uploading to Google Sheets...'
        result = service.spreadsheets().values().append(
            spreadsheetId = spreadsheet['ID'],
            range = spreadsheet['rangeName'],
            valueInputOption = spreadsheet['valueInputOption'],
            body = body).execute()
        database.setUpdatedToSheets()
    else:
        print 'Everything is up to date...'
if __name__ == '__main__':
    main()
