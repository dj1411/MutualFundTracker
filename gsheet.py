# import standard packages
import pandas as pd
import configparser
import os
import threading

# Import google apis
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# globals
config = configparser.ConfigParser()
configfile = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(configfile)
lock = threading.Lock()


class GSheet:
    def __init__(self) -> None:
        gc = gspread.oauth(credentials_filename='credentials.json',
                           authorized_user_filename='token.json')
        self.sheet = gc.open_by_key(config['DEFAULT']['GSHEET_ID'])

    def gspread_read(self):
        ws = self.sheet.worksheet('principle')
        df_principle = pd.DataFrame(ws.get_all_records())

        ws = self.sheet.worksheet('nav')
        df_nav = pd.DataFrame(ws.get_all_records())

        return (df_principle, df_nav)

    def gspread_write(self, tab, df):
        global lock
        lock.acquire()
        ws = self.sheet.worksheet(tab)
        ws.update([df.columns.values.tolist()] + df.values.tolist())
        lock.release()
