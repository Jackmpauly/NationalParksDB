import mysql.connector
import csv
import tableManager as tm

import pandas as pd

def main():
    init_all()

def init_all():
    tm.dropAllTables()

    tm.init_country()
    tm.init_state_province()
    tm.init_park()
    tm.init_lake()
    tm.init_mountain()
    tm.init_trail()

    # Commit changes to database
    tm.commitData()

    print("Successfully initialized all tables.")

main()