import mysql.connector
import csv

def dropAllTables(mycursor):
    # mycursor.execute("DROP TABLE park")
    mycursor.execute("DROP TABLE state_province")
    mycursor.execute("DROP TABLE country")

def init_country(mycursor):
    mycursor.execute(
        """CREATE TABLE country (
            id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(50) NOT NULL DEFAULT 'Missing Name', 
            region VARCHAR(15) NOT NULL,
            CHECK(region IN ('Africa', 'Asia', 'Europe', 'Oceania', 'North America', 'South America'))
        )
        """
    )
    sql = "INSERT INTO country (name, region) VALUES (%s, %s)"
    with open('CSVs/country.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            mycursor.execute(sql, (f'{row[1]}', f'{row[2]}'))


    mycursor.execute("SELECT * FROM country")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def insert_country(mycursor):
    sql = "INSERT INTO country (name, region) VALUES (%s, %s)"
    

def init_state_province(mycursor):
    mycursor.execute(
        """CREATE TABLE state_province (
            id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(100) NOT NULL DEFAULT 'Missing State/Province', 
            country_id INTEGER NOT NULL, 
            FOREIGN KEY (country_id) REFERENCES country(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
    )
    sql = "INSERT INTO state_province (name, country_id) VALUES (%s, %s)"
    with open('CSVs/state_province.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            mycursor.execute(sql, (f'{row[1]}', f'{int(row[2])}') )


    mycursor.execute("SELECT * FROM state_province")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def init_park(mycursor):
    mycursor.execute(
        """CREATE TABLE park (
            id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(100) NOT NULL DEFAULT 'Missing National Park Name', 
            visitors_per_year INTEGER, 
            state_province_id INTEGER NOT NULL, 
            area INTEGER, 
            year_established INTEGER NOT NULL, 
            FOREIGN KEY (state_province_id) REFERENCES state_province(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
    )
    sql = "INSERT INTO park (name, visitors_per_year, state_province_id, area, year_established) VALUES (%s, %s, %s, %s, %s)"
    with open('CSVs/park.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            input = ( row[1], isNull(row[2]), isNull(row[3]), isNull(row[4]), isNull(row[5]) )
            # print(input)
            mycursor.execute(sql, input)


    mycursor.execute("SELECT * FROM park")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def isNull(str):
    if( str == "NULL" ):
        # print("here")
        return None
    return int(str)


def test(mycursor):
    mycursor.execute(
        """CREATE TABLE park (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            Name VARCHAR(100), 
            Visitors_Per_Year INT, 
            SP_ID INT, 
            Area INT, 
            Year_Established YEAR, 
            FOREIGN KEY (SP_ID) REFERENCES state_province(ID)
        )
        """
    )
    sql = "INSERT INTO park (Name, Visitors_Per_Year, SP_ID, Area, Year_Established) VALUES (%s, %s, %s, %s, %s)"
    string = "NULL"
    number = "1"
    input = ("Djebel Aissa National Park",isNull(string),isNull(number),94,2003)
    mycursor.execute(sql, input)

    mycursor.execute("SELECT * FROM park")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


def printAllTables(mycursor):
    print("COUNTRY")
    mycursor.execute("SELECT * FROM country")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    
    print("STATE_PROVINCE")
    mycursor.execute("SELECT * FROM state_province")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

    print("PARK")
    mycursor.execute("SELECT * FROM park")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)