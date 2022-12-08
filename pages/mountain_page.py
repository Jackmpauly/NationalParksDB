import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm

mountain_dataframe = None

def gen_mountain_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Park ID':[],
        'Elevation':[]
    }

    df = pd.DataFrame(dict)

    for mountain in tm.get_mountain(searchterm):
        row = pd.DataFrame({'ID':str(mountain[0]), 'Name':mountain[1], 'Park ID':str(mountain[2]), 'Elevation':str(mountain[3])}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    df.set_axis(['ID', 'Name', 'Park ID', 'Elevation (m)'], axis = 'columns', copy = False)

    return df

def draw_textbox():
    name = st.text_input('Mountain', '')
    st.write('Searching for ', name)
    global mountain_dataframe
    mountain_dataframe = gen_mountain_dataframe(name)

def main():
    draw_textbox()
    st.table(mountain_dataframe)

main()