import mysql.connector
import csv
import createTables

def main():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "NationalParks"
    )

    mycursor = mydb.cursor()

    # mycursor.execute("CREATE DATABASE NationalParks")

    mycursor.execute("DROP TABLE customers")

    mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = ("John", "Highway 21")
    mycursor.execute(sql, val)

    mycursor.execute("SELECT * FROM customers")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)


    mycursor.execute("DROP TABLE state_province")
    mycursor.execute("DROP TABLE country")
    
    createTables.country(mycursor)
    createTables.state_province(mycursor)

main()