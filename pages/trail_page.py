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

trail_dataframe = None


def gen_trail_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Park ID':[],
        'Distance':[]
    }

    df = pd.DataFrame(dict)

    for trail in tm.get_trail(mycursor, searchterm):
        row = pd.DataFrame({'ID':str(trail[0]), 'Name':trail[1], 'Park ID':str(trail[2]), 'Distance':str(trail[3])}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    df.set_axis(['ID', 'Name', 'Park ID', 'Distance (km)'], axis = 'columns', inplace = True)

    return df

def draw_textbox():
    name = st.text_input('Trail', '')
    st.write('Searching for ', name)
    global trail_dataframe
    trail_dataframe = gen_trail_dataframe(name)

def main():
    draw_textbox()
    st.table(trail_dataframe)

main()