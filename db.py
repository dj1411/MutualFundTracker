# import standard packages
from select import select
import pandas as pd
import configparser
import os
from datetime import *
import threading

# Import local packages
from gsheet import GSheet

# globals
config = configparser.ConfigParser()
configfile = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(configfile)
list_month = ["Jan",	"Feb",	"Mar",	"Apr",	"May",
              "Jun",	"Jul",	"Aug",	"Sep",	"Oct",	"Nov",	"Dec"]


class Db:
    def __init__(self) -> None:
        # read from google
        _gsheet = GSheet(config['DEFAULT']['GSHEET_ID'])
        (self.df_investment, self.df_nav) = _gsheet.read()

        # reset index
        self.df_investment.set_index("owner_fund_principle", inplace=True)
        self.df_nav.set_index("owner_fund_principle", inplace=True)

    def calculate_principle(self):
        list_columns = ['owner_fund_principle']
        list_columns = list_columns.extend(list_month)
        df_principle = pd.DataFrame(columns=list_columns)
        for label, data in self.df_investment.iterrows():
            df_principle.at[len(df_principle), 'owner_fund_principle'] = label
            list_principle = [label]
            principle = int(label.split('_')[2])
            for month in list_month:
                inv = self.df_investment.loc[label][month]
                if not isinstance(inv, str):
                    principle += inv
                    list_principle.append(principle)
                    row, _ = df_principle.shape
                    df_principle.at[row - 1, month] = principle
                else:
                    break
            # df_principle.at[len(df_principle)] = list_principle

        print(df_principle)
