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


class Db:
    def __init__(self) -> None:
        _gsheet = GSheet(config['DEFAULT']['GSHEET_ID'])
        (self.df_principle, self.df_nav) = _gsheet.read()
        print(self.df_principle)
