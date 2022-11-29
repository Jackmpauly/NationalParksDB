import mysql.connector
import csv

def country(mycursor):
    # mycursor.execute("DROP TABLE country")
    mycursor.execute("CREATE TABLE country (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(100), Continent VARCHAR(100))")
    sql = "INSERT INTO country (Name, Continent) VALUES (%s, %s)"
    with open('CSVs/countries.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            mycursor.execute(sql, (f'{row[1]}', f'{row[2]}'))


    mycursor.execute("SELECT * FROM country")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def state_province(mycursor):
    # mycursor.execute("DROP TABLE state_province")
    mycursor.execute("CREATE TABLE state_province (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(100), Country_ID INT, FOREIGN KEY (Country_ID) REFERENCES country(ID))")
    sql = "INSERT INTO state_province (Name, Country_ID) VALUES (%s, %s)"
    with open('CSVs/state_province.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            mycursor.execute(sql, (f'{row[1]}', f'{int(row[2])}') )


    mycursor.execute("SELECT * FROM state_province")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)