import mysql.connector
import csv

def isNull(str):
    if( str == "NULL" ):
        # print("here")
        return None
    return int(str)

def dropAllTables(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS trail")
    mycursor.execute("DROP TABLE IF EXISTS mountain")
    mycursor.execute("DROP TABLE IF EXISTS lake")
    mycursor.execute("DROP TABLE IF EXISTS park")
    mycursor.execute("DROP TABLE IF EXISTS state_province")
    mycursor.execute("DROP TABLE IF EXISTS country")

def init_country(mycursor):
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

def insert_country(mycursor, name, region):
    sql = "INSERT INTO country (name, region) VALUES (%s, %s)"
    mycursor.execute(sql, (name, region) )

def update_country(mycursor, name, attribute, new_value):
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
        case 'name':
            current_name = new_value
        case 'region':
            region = new_value

    try:
        mycursor.execute("""UPDATE country SET name = %s, region = %s WHERE id = %s""", (current_name, region, id))
    # Duplicate name will throw IntegrityError thanks to UNIQUE constraint
    except mysql.connector.IntegrityError as duplicate_error:
        print("An entry with the name: " + current_name+ " already exists. Please enter a different country name and try again")
    # CHECK for valid region will throw DatabaseError
    except mysql.connector.DatabaseError as invalid_region_error:
        print("An invalid region was entered as the updated region: " + region + "\nValid regions are: Africa, Asia, Europe, Ocenia, North America, South America")

def delete_country(mycursor, name):
    mycursor.execute("""SELECT id FROM country WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()

    if fetched_row == None:
        print("Unable to delete country: \
            No country exists with the name: " + name + ". Please enter a new country and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM country WHERE id = %s""", (id_to_delete, ))

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
    with open('CSVs/state_province.csv', newline='', encoding = 'utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            mycursor.execute(sql, (f'{row[1]}', f'{int(row[2])}') )


    mycursor.execute("SELECT * FROM state_province")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

def is_duplicate_state_province(mycursor, name, country_id):
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

def insert_state_province(mycursor, name, country_id,):
    dupe = is_duplicate_state_province(mycursor, name, country_id)

    statement = "INSERT INTO state_province (name, country_id) VALUES (%s, %s)"
    if(dupe):
        print("duplicate")
    else:
        mycursor.execute(statement, (name, country_id) )
        

def update_state_province(mycursor, old_name, attr, val):
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
        case "name":
            name = val;
        case "country_id":
            country_id = val;
    
    try:
        mycursor.execute("""UPDATE state_province SET name = %s, country_id = %s WHERE id = %s""", (name, country_id, id) )
    except mysql.connector.IntegrityError as country_id_error:
        print("Unable to update state/province: \
            The given country_id " + str(country_id) + " does not exist. Please enter a different country_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def delete_state_province(mycursor, name):
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

def insert_park(mycursor, name, visitors_per_year, state_province_id, area, year_established):
    sql = "INSERT INTO park (name, visitors_per_year, state_province_id, area, year_established) VALUES (%s, %s, %s, %s, %s)"
    
    try:
        mycursor.execute(sql, (name, isNull(visitors_per_year), isNull(state_province_id), isNull(area), isNull(year_established)))
    except mysql.connector.IntegrityError as sp_id_error:
        print("Unable to add park: \
            The given state/province id " + str(state_province_id) + " does not exist. Please enter a new state/province id and try agian")
    except mysql.connector.Error as error:
        print("Something went wrong. {}".format(error))

def update_park(mycursor, name, attribute, new_value):
    mycursor.execute("""SELECT * FROM park WHERE name = %s""", (name,))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update park: No park with the name " + name + " exists. Please enter a different park and try again.")
        return
    
    id, current_name, visitors_per_year, sp_id, area, year_established = \
        row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3], row_to_update[4], row_to_update[5]

    match attribute:
        case 'name':
            current_name = new_value
        case 'visitors_per_year':
            visitors_per_year = new_value
        case 'state_province_id':
            sp_id = new_value
        case 'area':
            area = new_value
        case 'year_established':
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

def delete_park(mycursor, name):
    mycursor.execute("""SELECT id FROM park WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()

    if fetched_row == None:
        print("Unable to delete park: No country exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM park WHERE id = %s""", (id_to_delete, ))

# Create and initialize the lake table
def init_lake(mycursor):
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

def insert_lake(mycursor, name, park_id, type, depth):
    sql = "INSERT INTO lake (name, park_id, type, depth) VALUES (%s, %s, %s, %s)"

    try:
        mycursor.execute(sql, (name, isNull(park_id), type, isNull(depth)))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert lake: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def update_lake(mycursor, name, attribute, new_value):
    mycursor.execute("""SELECT * FROM lake WHERE name = %s""", (name,))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update lake: No lake with the name " + name + " exists. Please enter a different lake and try again.")
        return

    id, current_name, park_id, type, depth = row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3], row_to_update[4]

    match attribute:
        case 'name':
            current_name = new_value
        case 'park_id':
            park_id = new_value
        case 'type':
            type = new_value
        case 'depth':
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

def delete_lake(mycursor, name):
    mycursor.execute("""SELECT id FROM lake where name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete lake: No lake exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM lake WHERE id = %s""", (id_to_delete, ))

# Create and initialize the mountain table
def init_mountain(mycursor):
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

def insert_mountain(mycursor, name, park_id, elevation):
    sql = "INSERT INTO mountain (name, park_id, elevation) VALUES (%s, %s, %s)"

    try:
        mycursor.execute(sql, (name, park_id, elevation))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert mountain: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def update_mountain(mycursor, name, attribute, new_value):
    mycursor.execute("""SELECT * FROM mountain WHERE name = %s""", (name, ))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update mountain: No mountian with the name " + name + " exists. Please enter a different mountain and try again.")
        return

    id, current_name, park_id, elevation = row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3]

    match attribute:
        case 'name':
            current_name = new_value
        case 'park_id':
            park_id = new_value
        case 'elevation':
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

def delete_mountain(mycursor, name):
    mycursor.execute("""SELECT id FROM mountain WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete mountain: No mountain exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM mountain WHERE id = %s""", (id_to_delete, ))

# Create and initialize the trail table
def init_trail(mycursor):
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

def insert_trail(mycursor, name, park_id, distance):
    sql = "INSERT INTO trail (name, park_id, distance) VALUES (%s, %s, %s)"

    try:
        mycursor.execute(sql, (name, park_id, distance))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert trail: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

def update_trail(mycursor, name, attribute, new_value):
    mycursor.execute("""SELECT * FROM trail WHERE name = %s""", (name, ))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update trail: No trail with the name " + name + " exists. Please enter a different trail and try again.")
        return

    id, current_name, park_id, distance = row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3]

    match attribute:
        case 'name':
            current_name = new_value
        case 'park_id':
            park_id = new_value
        case 'distance':
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

def delete_trail(mycursor, name):
    mycursor.execute("""SELECT id FROM trail WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete trail: No trail exists with the name: " + name + ". Please tner a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    mycursor.execute("""DELETE FROM trail WHERE id = %s""", (id_to_delete, ))

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


def get_country(mycursor):
    # print("COUNTRY")
    mycursor.execute("SELECT * FROM country")
    return mycursor.fetchall()

def get_state_province(mycursor, param):
    # print("STATE_PROVINCE")
    print(param)
    statement = "SELECT * FROM state_province WHERE name LIKE '%%%s%%'" % param
    print(statement)
    mycursor.execute(statement)
    return mycursor.fetchall()

def get_park(mycursor):
    # print("PARK")
    mycursor.execute("SELECT * FROM park")
    return mycursor.fetchall()

def get_lake(mycursor):
    mycursor.execute("SELECT * FROM lake")
    return mycursor.fetchall()

def get_mountain(mycursor):
    mycursor.execute("SELECT * FROM mountain")
    return mycursor.fetchall()

def get_trail(mycursor):
    mycursor.execute("SELECT * FROM trail")
    return mycursor.fetchall()

def print_all(mycursor):
    for x in get_country(mycursor):
        print(x)
    for x in get_state_province(mycursor, ""):
        print(x)
    for x in get_park(mycursor):
        print(x)
    for x in get_lake(mycursor):
        print(x)
    for x in get_mountain(mycursor):
        print(x)
    for x in get_trail(mycursor):
        print(x)