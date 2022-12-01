import mysql.connector
import csv
import tableManager

def main():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "NationalParks"
    )

    mycursor = mydb.cursor()

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


main()