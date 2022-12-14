import mysql.connector
import csv

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "NationalParks"
)

mycursor = mydb.cursor()

def begin_transaction():
    mycursor.execute("START TRANSACTION")

def rollback():
    mycursor.execute("ROLLBACK")

def commitData():
    mydb.commit()

def isNull(str):
    if( str == "NULL" ):
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

    mycursor.execute("CREATE INDEX country_index ON country (name)")

def insert_country(name, region):
    sql = "INSERT INTO country (name, region) VALUES (%s, %s)"

    begin_transaction()
    try:
        mycursor.execute(sql, (name, region) )
    except mysql.connector.IntegrityError as duplicate_error:
        print("An entry with the name: " + name + " already exists.")
        rollback()
    except mysql.connector.DatabaseError as invalid_region_error:
        print("An invalid region was entered: " + region)
        rollback()

    commitData()

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

    begin_transaction()
    try:
        mycursor.execute("""UPDATE country SET name = %s, region = %s WHERE id = %s""", (current_name, region, id))
    # Duplicate name will throw IntegrityError thanks to UNIQUE constraint
    except mysql.connector.IntegrityError as duplicate_error:
        print("An entry with the name: " + current_name+ " already exists. Please enter a different country name and try again")
        rollback()
    # CHECK for valid region will throw DatabaseError
    except mysql.connector.DatabaseError as invalid_region_error:
        print("An invalid region was entered as the updated region: " + region + "\nValid regions are: Africa, Asia, Europe, Ocenia, North America, South America")
        rollback()

    commitData()

def delete_country(name):
    mycursor.execute("""SELECT id FROM country WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()

    if fetched_row == None:
        print("Unable to delete country: \
            No country exists with the name: " + name + ". Please enter a new country and try again.")
        return

    id_to_delete = fetched_row[0]
    begin_transaction()
    try:
        mycursor.execute("""DELETE FROM country WHERE id = %s""", (id_to_delete, ))
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

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

    mycursor.execute("CREATE INDEX state_province_index ON state_province (name)")

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
    dupe = is_duplicate_state_province(name, country_id)

    statement = "INSERT INTO state_province (name, country_id) VALUES (%s, %s)"
    if(dupe):
        print("duplicate")
    else:
        begin_transaction()
        try:
            mycursor.execute(statement, (name, country_id) )
        except mysql.connector.DatabaseError as error:
            print("Something went wrong. {}".format(error))
            rollback()

        commitData()
        
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
    
    begin_transaction()
    try:
        mycursor.execute("""UPDATE state_province SET name = %s, country_id = %s WHERE id = %s""", (name, country_id, id) )
    except mysql.connector.IntegrityError as country_id_error:
        print("Unable to update state/province: \
            The given country_id " + str(country_id) + " does not exist. Please enter a different country_id and try again.")
        rollback()
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()
    
    commitData()

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

    begin_transaction()
    try:
        mycursor.execute("""DELETE FROM state_province WHERE id = %s""", (id,))
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

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
            mycursor.execute(sql, input)

    mycursor.execute("CREATE INDEX park_index ON park (name)")

def insert_park(name, visitors_per_year, state_province_id, area, year_established):
    sql = "INSERT INTO park (name, visitors_per_year, state_province_id, area, year_established) VALUES (%s, %s, %s, %s, %s)"
    
    begin_transaction()
    try:
        mycursor.execute(sql, (name, isNull(visitors_per_year), isNull(state_province_id), isNull(area), isNull(year_established)))
    except mysql.connector.IntegrityError as sp_id_error:
        print("Unable to add park: \
            The given state/province id " + str(state_province_id) + " does not exist. Please enter a new state/province id and try agian")
        rollback()
    except mysql.connector.Error as error:
        print("Something went wrong. {}".format(error))
        rollback()
    
    commitData()

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

    begin_transaction()
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
        rollback()
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()
    
    commitData()

def delete_park(name):
    mycursor.execute("""SELECT id FROM park WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()

    if fetched_row == None:
        print("Unable to delete park: No country exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    begin_transaction()
    try:
        mycursor.execute("""DELETE FROM park WHERE id = %s""", (id_to_delete, ))
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

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
    
    mycursor.execute("CREATE INDEX lake_index ON lake (name)")

def insert_lake(name, park_id, type, depth):
    sql = "INSERT INTO lake (name, park_id, type, depth) VALUES (%s, %s, %s, %s)"

    begin_transaction()
    try:
        mycursor.execute(sql, (name, isNull(park_id), type, isNull(depth)))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert lake: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
        rollback()
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

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
        case 'Park':
            park_id = new_value
        case 'Type':
            type = new_value
        case 'Depth (m)':
            depth = new_value

    begin_transaction()
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
        rollback()
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()
    
    commitData()

def delete_lake(name):
    mycursor.execute("""SELECT id FROM lake where name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete lake: No lake exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    begin_transaction()
    try:
        mycursor.execute("""DELETE FROM lake WHERE id = %s""", (id_to_delete, ))
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

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

    mycursor.execute("CREATE INDEX mountain_index ON mountain (name)")

def insert_mountain(name, park_id, elevation):
    sql = "INSERT INTO mountain (name, park_id, elevation) VALUES (%s, %s, %s)"

    begin_transaction()
    try:
        mycursor.execute(sql, (name, park_id, elevation))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert mountain: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
        rollback()
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

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
        case 'Park':
            park_id = new_value
        case 'Elevation (m)':
            elevation = new_value

    begin_transaction()
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
        rollback()
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

def delete_mountain(name):
    mycursor.execute("""SELECT id FROM mountain WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete mountain: No mountain exists with the name: " + name + ". Please enter a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    begin_transaction()
    try:
        mycursor.execute("""DELETE FROM mountain WHERE id = %s""", (id_to_delete, ))
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

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

    mycursor.execute("CREATE INDEX trail_index ON trail (name)")

def insert_trail(name, park_id, distance):
    sql = "INSERT INTO trail (name, park_id, distance) VALUES (%s, %s, %s)"

    begin_transaction()
    try:
        mycursor.execute(sql, (name, park_id, distance))
    # Invalid park_id throws IntegrityError
    except mysql.connector.IntegrityError as park_id_error:
        print("Unable to insert trail: No park exists with id: " + str(park_id) + ". Please enter a different park_id and try again.")
        rollback()
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

def update_trail(name, attribute, new_value):
    mycursor.execute("""SELECT * FROM trail WHERE name = %s""", (name, ))

    row_to_update = mycursor.fetchone()
    if row_to_update == None:
        print("Unable to update trail: No trail with the name " + name + " exists. Please enter a different trail and try again.")
        return

    id, current_name, park_id, distance = row_to_update[0], row_to_update[1], row_to_update[2], row_to_update[3]

    match attribute:
        case 'Name':
            current_name = new_value
        case 'Park':
            park_id = new_value
        case 'Distance (km)':
            distance = new_value

    begin_transaction()
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
        rollback()
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

def delete_trail(name):
    mycursor.execute("""SELECT id FROM trail WHERE name = %s""", (name, ))

    fetched_row = mycursor.fetchone()
    if fetched_row == None:
        print("Unable to delete trail: No trail exists with the name: " + name + ". Please tner a different name and try again.")
        return

    id_to_delete = fetched_row[0]
    begin_transaction()
    try:
        mycursor.execute("""DELETE FROM trail WHERE id = %s""", (id_to_delete, ))
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))
        rollback()

    commitData()

def get_country(param):
    sql = "SELECT * FROM country USE INDEX(country_index) WHERE name LIKE %s OR region LIKE %s"
    mycursor.execute(sql, ('%' + param + '%', '%' + param + '%', ))
    return mycursor.fetchall()

def get_region_from_country_name(param):
    sql = """SELECT region
            FROM country USE INDEX(country_index)
            WHERE name = %s"""
    mycursor.execute(sql, (param, ))
    return mycursor.fetchall()

def get_state_province(param):
    sql = """SELECT state_province.id, state_province.name, country.name FROM state_province USE INDEX(state_province_index)
            INNER JOIN country ON (country.id=country_id) WHERE state_province.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def get_state_province_name_from_country_name(param):
    sql = """SELECT state_province.name
            FROM state_province USE INDEX(state_province_index)
            INNER JOIN country c on state_province.country_id = c.id
            WHERE c.name = %s"""
    mycursor.execute(sql, (param, ))
    return mycursor.fetchall()

def get_park(param):
    sql = """SELECT park.id, park.name, 
            CASE
                WHEN park.visitors_per_year IS NULL THEN 'No Data'
                ELSE park.visitors_per_year
            END AS visitors_per_year, 
            sp.name, park.area, park.year_established FROM park USE INDEX(park_index)
            INNER JOIN state_province sp on (park.state_province_id = sp.id) WHERE park.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def get_all_areas():
    sql = """SELECT DISTINCT area FROM park
            ORDER BY area ASC"""
    mycursor.execute(sql)
    return mycursor.fetchall()

def get_max_area():
    sql = """SELECT MAX(area) AS maxArea
            FROM park"""
    mycursor.execute(sql)
    return mycursor.fetchone()

def get_min_area():
    sql = """SELECT MIN(area) AS minArea
            FROM park"""
    mycursor.execute(sql)
    return mycursor.fetchone()

def get_all_visitors_per_year():
    sql = """SELECT DISTINCT 
            CASE
                WHEN visitors_per_year IS NULL THEN 0
                ELSE visitors_per_year
            END AS visitors_per_year 
            FROM park
            ORDER BY visitors_per_year ASC"""
    mycursor.execute(sql)
    return mycursor.fetchall()

def get_max_visitors_per_year():
    sql = """SELECT MAX(visitors_per_year) AS maxVisitors
            FROM park"""
    mycursor.execute(sql)
    return mycursor.fetchone()

def get_min_year_established():
    sql = """SELECT MIN(year_established) AS minYear
            FROM park"""
    mycursor.execute(sql)
    return mycursor.fetchone()

def get_max_year_established():
    sql = """SELECT MAX(year_established) AS maxYear
            FROM park"""
    mycursor.execute(sql)
    return mycursor.fetchone()

def get_lake(param):
    sql = """SELECT lake.id, lake.name, p.name, lake.type, lake.depth FROM lake USE INDEX(lake_index)
            INNER JOIN park p on (lake.park_id = p.id) WHERE lake.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def get_mountain(param):
    sql = """SELECT mountain.id, mountain.name, p.name, mountain.elevation FROM mountain USE INDEX(mountain_index)
            INNER JOIN park p on (mountain.park_id = p.id) WHERE mountain.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

def get_trail(param):
    sql = """SELECT trail.id, trail.name, p.name, trail.distance FROM trail USE INDEX(trail_index)
            INNER JOIN park p on (trail.park_id = p.id) WHERE trail.name LIKE %s"""
    mycursor.execute(sql, ('%' + param + '%', ))
    return mycursor.fetchall()

# Table that is viewed on the main page
def create_search_table_view():
    mycursor.execute("""DROP VIEW IF EXISTS search_joined_view""")
    sql = """
        CREATE VIEW search_joined_view AS
        SELECT park.id, park.name AS park_name, park.area, 
            CASE
                WHEN park.visitors_per_year IS NULL THEN 'No Data'
                ELSE park.visitors_per_year
            END AS park_visitors_per_year, 
            park.year_established, state_provinces.name AS state_province_name, countries.name AS country_name, countries.region,
        (SELECT COUNT(id)
            FROM lake
            WHERE lake.park_id = park.id) AS numLakes,
        (SELECT COUNT(id)
            FROM mountain
            WHERE mountain.park_id = park.id) AS numMountains,
        (SELECT COUNT(id)
            FROM trail
            WHERE trail.park_id = park.id) AS numTrails
        FROM park
        INNER JOIN state_province state_provinces ON park.state_province_id = state_provinces.id
        INNER JOIN country countries ON state_provinces.country_id = countries.id
        """

    try:
        mycursor.execute(sql)
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

# Will apply the selected filters to the view object above
def get_filtered_joined_table(params):
    sql = """SELECT * FROM search_joined_view"""

    # If there are parameters, add them to the query
    if len(params) > 0:
        sql += " WHERE "
        for param in params:
            # For numeric value ranges, need to make sure the second value is a list and that they are digits
            if len(param[1]) == 2 and str(param[1][0]).isdigit() and str(param[1][1]).isdigit():
                sql += param[0] + " >= " + str(param[1][0]) + " AND " + param[0] + " <= " + str(param[1][1]) + " AND "
            # For non-numeric values, just add the LIKE clause and single quotes
            else:
                sql += param[0] + " LIKE " + "'" + param[1] + "'" + " AND "
        # Remove the last AND
        sql = sql[:-4]

    # Create the filtered view for the sub-tables
    create_filtered_joined_table_view(sql)

    mycursor.execute(sql)
    return mycursor.fetchall()

# Creates a view of the filtered table to be used for filtering the sub-tables
def create_filtered_joined_table_view(sql):
    mycursor.execute("""DROP VIEW IF EXISTS filtered_joined_view""")
    sql = """
        CREATE VIEW filtered_joined_view AS
        """ + sql

    try:
        mycursor.execute(sql)
    except mysql.connector.DatabaseError as error:
        print("Something went wrong. {}".format(error))

# Gets the lakes from the parks that are listed in the filtered table
def get_lakes_from_filtered_joined_table():
    sql = """SELECT lake.id, lake.name, filtered_joined_view.park_name, lake.type, lake.depth
            FROM lake
            INNER JOIN filtered_joined_view ON lake.park_id = filtered_joined_view.id"""
    mycursor.execute(sql)
    return mycursor.fetchall()

# Gets the mountains from the parks that are listed in the filtered table
def get_mountains_from_filtered_joined_table():
    sql = """SELECT mountain.id, mountain.name, filtered_joined_view.park_name, mountain.elevation
            FROM mountain
            INNER JOIN filtered_joined_view ON mountain.park_id = filtered_joined_view.id"""
    mycursor.execute(sql)
    return mycursor.fetchall()

# Gets the trails from the parks that are listed in the filtered table
def get_trails_from_filtered_joined_table():
    sql = """SELECT trail.id, trail.name, filtered_joined_view.park_name, trail.distance
            FROM trail
            INNER JOIN filtered_joined_view ON trail.park_id = filtered_joined_view.id"""
    mycursor.execute(sql)
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