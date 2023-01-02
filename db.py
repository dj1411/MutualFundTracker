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
        _gsheet = GSheet(config['DEFAULT']['GSHEET_ID'])
        (self.df_investment, self.df_nav) = _gsheet.read()

    def calculate_profit(self):
        # calculate principle
        for label, data in self.df_investment.iterrows():
            principle = self.df_investment.loc[label]['principle']
            list_principle = []
            for month in list_month:
                inv = self.df_investment.loc[label][month]
                if not isinstance(inv, str):
                    principle += inv
                    list_principle.append(principle)
                else:
                    break
            print(list_principle)
