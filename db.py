# import standard packages
from select import select
from tkinter.font import names
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
        self.gsheet = GSheet(config['DEFAULT']['GSHEET_ID'])
        (self.df_investment, self.df_nav) = self.gsheet.read()

        # treat data as numeric
        for col_label in list_month:
            if col_label in list_month:
                self.df_investment[col_label] = pd.to_numeric(
                    self.df_investment[col_label])
                self.df_nav[col_label] = pd.to_numeric(self.df_nav[col_label])

    def calculate_principle(self):
        list_columns = ['owner', 'fund']
        list_columns.extend(list_month)
        self.df_principle = pd.DataFrame(columns=list_columns)
        for row_label, data in self.df_investment.iterrows():
            list_principle = [data['owner'], data['fund']]
            principle = self.df_investment.loc[row_label]['principle']
            for month in list_month:
                principle += data[month]
                list_principle.append(principle)
            self.df_principle.loc[row_label] = list_principle


    def calculate_profit(self):
        self.df_profit = self.df_nav - self.df_principle
        _df_profit = self.df_profit.reset_index(
            names='owner_fund_principle').fillna(0)
        self.gsheet.write('profit', _df_profit)

    def calculate_percent(self):
        df_percent = self.df_profit / self.df_principle
        df_percent = df_percent.reset_index(
            names='owner_fund_principle').fillna(0)
        self.gsheet.write('percent', df_percent)
