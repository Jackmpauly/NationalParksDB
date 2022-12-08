import mysql.connector
import csv

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "NationalParks"
)

mycursor = mydb.cursor()

def commitData():
    mydb.commit()

def isNull(str):
    if( str == "NULL" ):
        # print("here")
        return None
    return int(str)

def dropAllTables():
    mycursor.execute("DROP TABLE IF EXISTS trail")
    mycursor.execute("DROP TABLE IF EXISTS mountain")
    mycursor.execute("DROP TABLE IF EXISTS lake")
    mycursor.execute("DROP TABLE IF EXISTS park")
    mycursor.execute("DROP TABLE IF EXISTS state_province")
    mycursor.execute("DROP TABLE IF EXISTS country")

def init_country():
    mycursor.execute(
        """CREATE TABLE country (
            id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(50) NOT NULL UNIQUE DEFAULT 'Missing Name', 
            region VARCHAR(15) NOT NULL,
            CHECK(region IN ('Africa', 'Asia', 'Europe', 'Oceania', 'North America', 'South America'))
        )
        """
    )
    sql = "INSERT INTO country (name, region) VALUES (%s, %s)"
    with open('CSVs/country.csv', newline='', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            mycursor.execute(sql, (f'{row[1]}', f'{row[2]}'))


    mycursor.execute("SELECT * FROM country")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def insert_country(name, region):
    sql = "INSERT INTO country (name, region) VALUES (%s, %s)"

    try:
        mycursor.execute(sql, (name, region) )
    except mysql.connector.IntegrityError as duplicate_error:
        print("An entry with the name: " + name + " already exists.")
    except mysql.connector.DatabaseError as invalid_region_error:
        print("An invalid region was entered: " + region)

def update_country(name, attribute, new_value):
    mycursor.execute("""SELECT * FROM country WHERE name = %s""", (name, ))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update country: \
            No country exists with the name: " + name + ". Please enter a new country and try again")
        return

    id = row_to_update[0]
    current_name = row_to_update[1]
    region = row_to_update[2]

    match attribute:
        case 'Name':
            current_name = new_value
        case 'Region':
            region = new_value

    try:
        mycursor.execute("""UPDATE country SET name = %s, region = %s WHERE id = %s""", (current_name, region, id))
    # Duplicate name will throw IntegrityError thanks to UNIQUE constraint
    except mysql.connector.IntegrityError as duplicate_error:
        print("An entry with the name: " + current_name+ " already exists. Please enter a different country name and try again")
    # CHECK for valid region will throw DatabaseError
    except mysql.connector.DatabaseError as invalid_region_error:
        print("An invalid region was entered as the updated region: " + region + "\nValid regions are: Africa, Asia, Europe, Ocenia, North America, South America")

def delete_country(name):
    mycursor.execute("""SELECT id FROM country WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()

    if fetched_row == None:
        print("Unable to delete country: \
            No country exists with the name: " + name + ". Please enter a new country and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM country WHERE id = %s""", (id_to_delete, ))

def init_state_province():
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
    with open('CSVs/state_province.csv', newline='', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            mycursor.execute(sql, (f'{row[1]}', f'{int(row[2])}') )


    mycursor.execute("SELECT * FROM state_province")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def is_duplicate_state_province(name, country_id):
    getcount = (
        """SELECT COUNT(*) AS c FROM state_province
            WHERE (name = %s) AND (country_id = %s)
        """
    )
    mycursor.execute(getcount, (name, country_id) )

    myresult = mycursor.fetchone()
    if(myresult[0] == 1):
        return True
    else:
        return False

def insert_state_province(name, country_id):
    dupe = is_duplicate_state_province(mycursor, name, country_id)

    statement = "INSERT INTO state_province (name, country_id) VALUES (%s, %s)"
    if(dupe):
        print("duplicate")
    else:
        mycursor.execute(statement, (name, country_id) )
        

def update_state_province(old_name, attr, val):
    mycursor.execute(
        """SELECT * FROM state_province
            WHERE name = %s
        """, (old_name,)
    )
    update_id = mycursor.fetchone()
    if update_id == None:
        print("Unable to update state/province: \
            There is no state/province with the name: " + old_name + ". Please enter a different name and try again.")
        return

    id = update_id[0]
    name = update_id[1]
    country_id = update_id[2]

    match attr:
        case "Name":
            name = val;
        case "Country":
            country_id = val;
    
    try:
        mycursor.execute("""UPDATE state_province SET name = %s, country_id = %s WHERE id = %s""", (name, country_id, id) )
    except mysql.connector.IntegrityError as country_id_error:
        print("Unable to update state/province: \
            The given country_id " + str(country_id) + " does not exist. Please enter a different country_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def delete_state_province(name):
    mycursor.execute(
        """SELECT id FROM state_province
            WHERE name = %s
        """, (name,)
    )
    update_id = mycursor.fetchone()
    if update_id == None:
        print("Unable to delete state/province: \
            There is no state/province with the name: " + name + ". Please enter a different name and try again.")
        return

    id = update_id[0]

    mycursor.execute("""DELETE FROM state_province WHERE id = %s""", (id,))

def init_park():
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
    with open('CSVs/park.csv', newline='', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            input = ( row[1], isNull(row[2]), isNull(row[3]), isNull(row[4]), isNull(row[5]) )
            # print(input)
            mycursor.execute(sql, input)


    mycursor.execute("SELECT * FROM park")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def insert_park(name, visitors_per_year, state_province_id, area, year_established):
    sql = "INSERT INTO park (name, visitors_per_year, state_province_id, area, year_established) VALUES (%s, %s, %s, %s, %s)"
    
    try:
        mycursor.execute(sql, (name, isNull(visitors_per_year), isNull(state_province_id), isNull(area), isNull(year_established)))
    except mysql.connector.IntegrityError as sp_id_error:
        print("Unable to add park: \
            The given state/province id " + str(state_province_id) + " does not exist. Please enter a new state/province id and try agian")
    except mysql.connector.Error as error:
        print("Something went wrong. {}".format(error))

def update_park(name, attribute, new_value):
    mycursor.execute("""SELECT * FROM park WHERE name = %s""", (name,))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update park: No park with the name " + name + " exists. Please enter a different park and try again.")
        return
    
    id, current_name, visitors_per_year, sp_id, area, year_established = \
        row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3], row_to_update[4], row_to_update[5]

    match attribute:
        case 'Name':
            current_name = new_value
        case 'Visitors Per Year':
            visitors_per_year = new_value
        case 'State/Province':
            sp_id = new_value
        case 'Area (km sqd)':
            area = new_value
        case 'Year Established':
            year_established = new_value

    try:
        mycursor.execute(
            """
            UPDATE park
            SET name = %s, visitors_per_year = %s, state_province_id = %s, area = %s, year_established = %s
            WHERE id = %s
            """,
            (current_name, visitors_per_year, sp_id, area, year_established, id)
        )
    # Thrown when attempting to update SP_ID to an invalid SP_ID
    except mysql.connector.IntegrityError as sp_id_error:
        print("Unable to update park: The given state_province_id: " + str(sp_id) + " does not exist. Enter a different state_province_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def delete_park(name):
    mycursor.execute("""SELECT id FROM park WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()

    if fetched_row == None:
        print("Unable to delete park: No country exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM park WHERE id = %s""", (id_to_delete, ))

# Create and initialize the lake table
def init_lake():
    mycursor.execute(
        """
        CREATE TABLE lake (
            id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL DEFAULT 'Missing Lake Name',
            park_id INTEGER NOT NULL,
            type VARCHAR(25),
            depth INTEGER,
            FOREIGN KEY (park_id) REFERENCES park(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
    )

    sql = "INSERT INTO lake (name, park_id, type, depth) VALUES (%s, %s, %s, %s)"
    with open('CSVs/lake.csv', newline='', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for row in csv_reader:
            input = ( row[1], isNull(row[2]), row[3], isNull(row[4]) )
            mycursor.execute(sql, input)
    
    # TODO: Verification Step - Delete Later
    mycursor.execute("SELECT * FROM lake")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def insert_lake(name, park_id, type, depth):
    sql = "INSERT INTO lake (name, park_id, type, depth) VALUES (%s, %s, %s, %s)"

    try:
        mycursor.execute(sql, (name, isNull(park_id), type, isNull(depth)))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert lake: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def update_lake(name, attribute, new_value):
    mycursor.execute("""SELECT * FROM lake WHERE name = %s""", (name,))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update lake: No lake with the name " + name + " exists. Please enter a different lake and try again.")
        return

    id, current_name, park_id, type, depth = row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3], row_to_update[4]

    match attribute:
        case 'Name':
            current_name = new_value
        case 'Park ID':
            park_id = new_value
        case 'Type':
            type = new_value
        case 'Depth':
            depth = new_value

    try:
        mycursor.execute(
            """
            UPDATE lake
            SET name = %s, park_id = %s, type = %s, depth = %s
            WHERE id = %s
            """,
            (current_name, park_id, type, depth, id)
        )
    # Thrown when attempting to update park_id to an invalid park_id
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to update lake: The given park_id: " + str(park_id) + " does not exist. Enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def delete_lake(name):
    mycursor.execute("""SELECT id FROM lake where name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete lake: No lake exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM lake WHERE id = %s""", (id_to_delete, ))

# Create and initialize the mountain table
def init_mountain():
    mycursor.execute(
        """
        CREATE TABLE mountain (
            id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL DEFAULT 'Missing Mountain Name',
            park_id INTEGER NOT NULL,
            elevation INTEGER NOT NULL,
            FOREIGN KEY (park_id) REFERENCES park(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
    )

    sql = "INSERT INTO mountain (name, park_id, elevation) VALUES (%s, %s, %s)"
    with open('CSVs/mountain.csv', newline = '', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for row in csv_reader:
            input = ( row[1], isNull(row[2]), isNull(row[3]) )
            mycursor.execute(sql, input)

    # TODO: Verification Step - Delete Later
    mycursor.execute("SELECT * FROM mountain")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def insert_mountain(name, park_id, elevation):
    sql = "INSERT INTO mountain (name, park_id, elevation) VALUES (%s, %s, %s)"

    try:
        mycursor.execute(sql, (name, park_id, elevation))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert mountain: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def update_mountain(name, attribute, new_value):
    mycursor.execute("""SELECT * FROM mountain WHERE name = %s""", (name, ))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update mountain: No mountian with the name " + name + " exists. Please enter a different mountain and try again.")
        return

    id, current_name, park_id, elevation = row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3]

    match attribute:
        case 'Name':
            current_name = new_value
        case 'Park ID':
            park_id = new_value
        case 'Elevation':
            elevation = new_value

    try:
        mycursor.execute(
            """
            UPDATE mountain
            SET name = %s, park_id = %s, elevation = %s
            WHERE id = %s
            """,
            (current_name, park_id, elevation, id)
        )
    # Thrown when attemtping to update park_id to an invalid park_id
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to update mountain: The given park_id: " + str(park_id) + " does not exist. Enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def delete_mountain(name):
    mycursor.execute("""SELECT id FROM mountain WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete mountain: No mountain exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM mountain WHERE id = %s""", (id_to_delete, ))

# Create and initialize the trail table
def init_trail():
    mycursor.execute(
        """
        CREATE TABLE trail (
            id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL DEFAULT 'Missing Trail Name',
            park_id INTEGER NOT NULL,
            distance DECIMAL(6, 2),
            FOREIGN KEY (park_id) REFERENCES park(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
    )

    sql = "INSERT INTO trail (name, park_id, distance) VALUES (%s, %s, %s)"
    with open('CSVs/trail.csv', newline = '', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for row in csv_reader:
            input = ( row[1], isNull(row[2]), row[3] )
            mycursor.execute(sql, input)

    # TODO: Verification Step - Delete Later
    mycursor.execute("SELECT * FROM trail")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def insert_trail(name, park_id, distance):
    sql = "INSERT INTO trail (name, park_id, distance) VALUES (%s, %s, %s)"

    try:
        mycursor.execute(sql, (name, park_id, distance))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert trail: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def update_trail(name, attribute, new_value):
    mycursor.execute("""SELECT * FROM trail WHERE name = %s""", (name, ))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update trail: No trail with the name " + name + " exists. Please enter a different trail and try again.")
        return

    id, current_name, park_id, distance = row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3]

    match attribute:
        case 'name':
            current_name = new_value
        case 'Park ID':
            park_id = new_value
        case 'Distance (km)':
            distance = new_value

    try:
        mycursor.execute(
            """
            UPDATE trail
            SET name = %s, park_id = %s, distance = %s
            WHERE id = %s
            """,
            (current_name, park_id, distance, id)
        )
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to update trail: The given park_id: " + str(park_id) + " does not exist. Enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def delete_trail(name):
    mycursor.execute("""SELECT id FROM trail WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete trail: No trail exists with the name: " + name + ". Please tner a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM trail WHERE id = %s""", (id_to_delete, ))

def test():
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


def get_country(param):
    # print("COUNTRY")
    sql = "SELECT * FROM country WHERE name LIKE %s"
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def get_state_province(param):
    # print("STATE_PROVINCE")
    sql = """SELECT state_province.id, state_province.name, country.name FROM state_province 
            INNER JOIN country ON (country.id=country_id) WHERE state_province.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def get_park(param):
    # print("PARK")
    sql = """SELECT park.id, park.name, park.visitors_per_year, sp.name, park.area, park.year_established FROM park
            INNER JOIN state_province sp on (park.state_province_id = sp.id) WHERE park.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def get_lake(param):
    sql = """SELECT lake.id, lake.name, p.name, lake.type, lake.depth FROM lake
            INNER JOIN park p on (lake.park_id = p.id) WHERE lake.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def get_mountain(param):
    sql = """SELECT mountain.id, mountain.name, p.name, mountain.elevation FROM mountain
            INNER JOIN park p on (mountain.park_id = p.id) WHERE mountain.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

# TODO: FOR SOME REASON THIS AIN'T WORKING
def get_trail(param):
    sql = """SELECT trail.id, trail.name, p.name, trail.distance FROM trail
            INNER JOIN park p on (trail.park_id = p.id) WHERE trail.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def print_all():
    for x in get_country(""):
        print(x)
    for x in get_state_province(""):
        print(x)
    for x in get_park(""):
        print(x)
    for x in get_lake(""):
        print(x)
    for x in get_mountain(""):
        print(x)
    for x in get_trail(""):
        print(x)