import mysql.connector
import csv
import tableManager as tm

import pandas as pd


def main():



    tm.dropAllTables()
    tm.init_country()
    tm.init_state_province()
    tm.init_park()


    # user add values
    tm.insert_country("Mexico", "North America")
    tm.print_country()

    tm.print_state_province()

    tm.insert_state_province("Sinaloa", 54)
    tm.print_state_province()

    # user update values
    tm.update_state_province("Sinaloa", "country_id", 32)
    tm.print_state_province()


    # user delete values
    tm.delete_state_province("Sinaloa")
    tm.print_state_province()

    # user can search for things
        # will have the kinds of things they can search for
    
    
    # for aggregate: how many national parks are in each country



def init():
    tm.init_park()

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

#init()
init_all()

# Test for Delete Country
# tm.delete_country('New Zealand')

# Test for Update Country
# tm.update_country('Greece', 'name', 'Mozambique')
# tm.update_country('Mozambique', 'region', 'Africa')

# Tests for Park INSERT/UPDATE/DELETE
# tm.insert_park("Some Really Cool National Park", 85000, 45, "NULL", 1923)
# tm.update_park("Some Really Cool National Park", "year_established", 2014)
# tm.delete_park("Some Really Cool National Park")

# Tests for Lake INSERT/UPDATE/DELETE
# tm.insert_lake('Lake Tahoe', 33, 'Freshwater', 501)
# tm.update_lake('Lake Tahoe', "name", 'Lake Smokin A Pack')
# tm.update_lake('Lake Smokin A Pack', "park_id", 100)
# tm.update_lake('Lake Smokin A Pack', 'park_id', 32)
# tm.update_lake('Lake Smokin A Pack', 'type', 'Crater')
# tm.update_lake('Lake Smokin A Pack', 'depth', 2)
# tm.delete_lake('Lake Smokin A Pack')

# Tests for Mountain INSERT/UPDATE/DELETE
# tm.insert_mountain('Pompeii', 1, 1433)
# tm.update_mountain('Pompeii', 'name', 'Mount Pauly')
# tm.update_mountain('Mount Pauly', 'park_id', 99)
# tm.update_mountain('Mount Pauly', 'park_id', 14)
# tm.update_mountain('Mount Pauly', 'elevation', 9999)
# tm.delete_mountain('Mount Pauly')

# Tests for Trail INSERT/UPDATE/DELETE
# tm.insert_trail('Happy Trail', 23, 56.4)
# tm.update_trail('Happy Trail', 'name', 'Sad Trail')
# tm.update_trail('Sad Trail', 'park_id', 152)
# tm.update_trail('Sad Trail', 'park_id', 22)
# tm.update_trail('Sad Trail', 'distance', 49.21)
# tm.delete_trail('Sad Trail')

tm.print_all()