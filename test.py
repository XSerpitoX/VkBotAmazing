from pprint import pprint

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1ZKXMC1RKChvp_kzgZwIyfC6tnFD_j2mjiJJi-J-949o'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A1:E47',
            majorDimension='ROWS'
        ).execute()

pprint(values['values'][1])