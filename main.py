# import standard packages
import os.path
import configparser
import datetime

# import custom packages
from db import Db

# globals
config = configparser.ConfigParser()
configfile = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(configfile)


def main():
    start_time = datetime.datetime.now()

    db = Db()
    db.calculate_principle()
    db.calculate_profit()
    db.calculate_percent()

    end_time = datetime.datetime.now()
    td = end_time - start_time
    print("Script finished in %f seconds" % td.total_seconds())


if __name__ == "__main__":
    try:
        main()
    except (SystemExit, KeyboardInterrupt) as e:
        pass
    except:
        assert False, "An exception has occurred."
