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
        self.df_profit = pd.DataFrame()
        self.df_profit['owner'] = self.df_investment['owner']
        self.df_profit['fund'] = self.df_investment['fund']
        _df_profit = self.df_nav.drop(
            ['owner', 'fund'], axis=1) - self.df_principle.drop(['owner', 'fund'], axis=1)
        self.df_profit = pd.concat(
            [self.df_profit, _df_profit], axis=1).fillna(0)
        self.gsheet.write('profit', self.df_profit)

    def calculate_percent(self):
        self.df_percent = pd.DataFrame()
        self.df_percent['owner'] = self.df_investment['owner']
        self.df_percent['fund'] = self.df_investment['fund']
        _df_percent = self.df_profit.drop(
            ['owner', 'fund'], axis=1) / self.df_principle.drop(['owner', 'fund'], axis=1)
        self.df_percent = pd.concat(
            [self.df_percent, _df_percent], axis=1).fillna(0)
        self.gsheet.write('percent', self.df_percent)

    def calculate_overall(self):
        df_overall = pd.DataFrame()
        df_overall = pd.concat(
            [self.df_investment['owner'], self.df_investment['fund']], axis=1)

        # principle column
        _, ncols = self.df_principle.shape
        df_overall = pd.concat(
            [df_overall, self.df_principle.iloc[:, ncols-1].rename('principle')], axis=1)

        # profit column
        list_profit = []
        for label, data in self.df_profit.iterrows():
            list_profit.append(data.drop(['owner', 'fund']).sum())
        df_overall['profit'] = list_profit

        print(df_overall)
