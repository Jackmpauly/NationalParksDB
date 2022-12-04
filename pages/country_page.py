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

country_dataframe = None

def gen_country_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Region':[]
    }

    df = pd.DataFrame(dict)

    for country in tm.get_country(mycursor, searchterm):
        row = pd.DataFrame({'ID':str(country[0]), 'Name':country[1], 'Region':country[2]}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    return df

def draw_textbox():
    name = st.text_input('Country', '')
    st.write('Searching for ', name)
    global country_dataframe
    country_dataframe = gen_country_dataframe(name)

def main():
    draw_textbox()
    st.table(country_dataframe)

main()