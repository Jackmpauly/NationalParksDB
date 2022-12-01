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


    # tableManager.dropAllTables(mycursor)
    # mycursor.execute("DROP TABLE country CASCADE")
    # tableManager.init_country(mycursor)
    # tableManager.init_state_province(mycursor)
    tableManager.init_park(mycursor)

    # mycursor.execute("DELETE FROM country WHERE (id = 37)")


    
    tableManager.printAllTables(mycursor)

main()