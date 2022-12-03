import mysql.connector
import csv
import tableManager

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "NationalParks"
)

mycursor = mydb.cursor()

def main():

    # mycursor.execute("CREATE DATABASE NationalParks"))


    tableManager.dropAllTables(mycursor)
    # mycursor.execute("DROP TABLE country CASCADE")
    tableManager.init_country(mycursor)
    tableManager.init_state_province(mycursor)
    tableManager.init_park(mycursor)

    # mycursor.execute("DELETE FROM country WHERE (id = 37)")

    # user add values
    tableManager.insert_country(mycursor, "Mexico", "North America")
    tableManager.print_country(mycursor)

    tableManager.print_state_province(mycursor)

    tableManager.insert_state_province(mycursor, "Sinaloa", 54)
    tableManager.print_state_province(mycursor)

    # user update values
    tableManager.update_state_province(mycursor, "Sinaloa", "country_id", 32)
    tableManager.print_state_province(mycursor)


    # user delete values
    tableManager.delete_state_province(mycursor, "Sinaloa")
    tableManager.print_state_province(mycursor)

    # user can search for things
        # will have the kinds of things they can search for
    
    
    # for aggregate: how many national parks are in each country



def init():
    tableManager.init_park(mycursor)

def init_all():
    tableManager.dropAllTables(mycursor)

    tableManager.init_country(mycursor)
    tableManager.init_state_province(mycursor)
    tableManager.init_park(mycursor)
    tableManager.init_lake(mycursor)
    tableManager.init_mountain(mycursor)
    tableManager.init_trail(mycursor)

#init()
init_all()

# Test for Delete Country
# tableManager.delete_country(mycursor, 'New Zealand')
# tableManager.print_all(mycursor)

# Test for Update Country
tableManager.update_country(mycursor, 'Greece', 'name', 'Mozambique')
tableManager.update_country(mycursor, 'Mozambique', 'region', 'Africa')
tableManager.print_all(mycursor)