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

lake_dataframe = None

def gen_lake_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Park ID':[],
        'Type':[],
        'Depth':[]
    }

    df = pd.DataFrame(dict)

    for lake in tm.get_lake(mycursor, searchterm):
        row = pd.DataFrame({'ID':str(lake[0]), 'Name':lake[1], 'Park ID':str(lake[2]), 'Type':lake[3], \
             'Depth':str(lake[4])}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    df.set_axis(['ID', 'Name', 'Park ID', 'Type', 'Depth (m)'], axis = 'columns', copy = False)

    return df

def draw_textbox():
    name = st.text_input('Lake', '')
    st.write('Searching for ', name)
    global lake_dataframe
    lake_dataframe = gen_lake_dataframe(name)

def main():
    draw_textbox()
    st.table(lake_dataframe)

main()