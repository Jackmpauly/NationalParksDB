import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm

mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "NationalParks"
    )

mycursor = mydb.cursor()

park_dataframe = None

def gen_park_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Visitors Per Year':[],
        'State_Province ID':[],
        'Area':[],
        'Year Established':[]
    }

    df = pd.DataFrame(dict)

    for park in tm.get_park(mycursor, searchterm):
        row = pd.DataFrame({'ID':str(park[0]), 'Name':park[1], 'Visitors Per Year':park[2], 'State_Province ID':str(park[3]),
             'Area':str(park[4]), 'Year Established':str(park[5])}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    df.set_axis(['ID', 'Name', 'Visitors Per Year', 'State_Province ID', 'Area (km sqd)', 'Year Established'], axis = 'columns', copy = False)

    return df

def draw_textbox():
    name = st.text_input('Park', '')
    st.write('Searching for ', name)
    global park_dataframe
    park_dataframe = gen_park_dataframe(name)

def main():
    draw_textbox()
    st.table(park_dataframe)

main()