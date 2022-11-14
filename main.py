# Import google apis
from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# import standard packages
import pandas
import os.path
import configparser
import datetime

# import custom packages
from Utils import myprint
from Utils import myassert

# globals
df_kuvera = None
config = configparser.ConfigParser()
configfile = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(configfile)
MAXROWS = 50
MAXCOLS = 100


def read_kuvera():
    global df_kuvera
    file_kuvera = input("Enter file exported from Kuvera: ")
    myassert(os.path.exists(file_kuvera), f"file not found: {file_kuvera}")
    df_kuvera = pandas.read_csv(file_kuvera)
    pass


def gsheet_init():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def gsheet_read_fundnames(creds):
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=config['DEFAULT']['GSHEET_ID'],
                                range="self!A4:A31").execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    print(values)


def main():
    read_kuvera()
    start_time = datetime.datetime.now()
    creds = gsheet_init()
    gsheet_read_fundnames(creds)
    end_time = datetime.datetime.now()
    td = end_time - start_time
    myprint("Script finished in %f seconds" % td.total_seconds())


if __name__ == "__main__":
    try:
        main()
    except:
        myassert(False, "An exception has occurred.", True)
