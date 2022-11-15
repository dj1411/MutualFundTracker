# Import google apis
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
ws = None

def read_kuvera():
    global df_kuvera
    file_kuvera = input("Enter file exported from Kuvera: ")
    myassert(os.path.exists(file_kuvera), f"file not found: {file_kuvera}")
    df_kuvera = pandas.read_csv(file_kuvera)
    pass


def gsheet_init():
    global ws
    gc = gspread.oauth()
    sheet = gc.open_by_key(config['DEFAULT']['GSHEET_ID'])
    for id, sh in enumerate(sheet.worksheets(), start=0):
        print(id, sh)
    sh_id = int(input("Select sheet to use: "))
    ws = sheet.get_worksheet(sh_id)


def gsheet_read_fundlist():
    return ws.col_values(1)


def create_value_list(fundlist):
    value_list = []
    col = df_kuvera.columns.get_loc('Current Value')
    for fund in fundlist:
        select = df_kuvera['Scheme Name'] == fund
        if df_kuvera[select].size > 0:
            arr = [int(df_kuvera[select].iat[0, col])]
        else:
            arr = ['']
        value_list.append(arr)
    return value_list


def gsheet_write_values(value_list):
    value_list.pop(0)
    value_list.pop(0)
    value_list.pop(0)
    ws.update('F4:F50', value_list)


def main():
    read_kuvera()
    start_time = datetime.datetime.now()
    gsheet_init()
    fundlist = gsheet_read_fundlist()
    value_list = create_value_list(fundlist)
    gsheet_write_values(value_list)
    end_time = datetime.datetime.now()
    td = end_time - start_time
    myprint("Script finished in %f seconds" % td.total_seconds())


if __name__ == "__main__":
    try:
        main()
    except (SystemExit, KeyboardInterrupt) as e :
        pass
    except:
        myassert(False, "An exception has occurred.", True)
