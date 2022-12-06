#importing streamlit library
import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm

import pages.country_page as cp
import pages.state_province_page as sp
import pages.park_page as pp
import pages.mountain_page as mp
import pages.lake_page as lp
import pages.trail_page as tp


mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "NationalParks"
    )

mycursor = mydb.cursor()

# tm.dropAllTables(mycursor)
# mycursor.execute("DROP TABLE country CASCADE")
# tm.init_country(mycursor)
# tm.init_state_province(mycursor)
# tm.init_park(mycursor)

# global variables:
c_dataframe = None
sp_dataframe = None
p_dataframe = None
m_dataframe = None
l_dataframe = None
t_dataframe = None



def gen_sp_dataframe(searchterm):
    # create the empty dict (to be drawn in the table)
    dict = {
        'ID':[],
        'Name':[],
        'Country ID':[]
    }
    df = pd.DataFrame(dict)

    # loop through the state_province table and create rows, then enter them into the dataframe
    for x in tm.get_state_province(mycursor, searchterm):
        row = pd.DataFrame({ 'ID':str(x[0]), 'Name':x[1], 'Country ID':str(x[2]) }, index=[0])
        df = pd.concat([df.loc[:], row]).reset_index(drop=True)


    # return the dataframe
    return df


def draw_textbox():
    name = st.text_input('State/Province', '')
    st.write('Searching for ', name)
    global sp_dataframe
    sp_dataframe = gen_sp_dataframe(name)

def modify():
    global sp_dataframe

    tempdf = sp_dataframe.sort_values('Name')
    option = st.selectbox('Select a Province to Modify',
        tempdf['Name'])

    st.write('You selected:', option)

    if st.button('Update'):
        attr_option = st.selectbox('Select an attribute to modify',
            list(sp_dataframe.columns.values)[1:])
        new_name = st.text_input('Enter new ' + attr_option)
        
    else:
        st.write('Goodbye')

def getAllDataframes():
    print("getting all dataframes")
    global c_dataframe
    c_dataframe = cp.gen_country_dataframe('')
    global sp_dataframe
    sp_dataframe = sp.gen_sp_dataframe('')
    global p_dataframe
    p_dataframe = pp.gen_park_dataframe('')
    global m_dataframe
    m_dataframe = mp.gen_mountain_dataframe('')
    global l_dataframe
    l_dataframe = lp.gen_lake_dataframe('')
    global t_dataframe
    t_dataframe = tp.gen_trail_dataframe('')


def main():
    print("reset")
    # writing simple text
    # st.text("Hello")


st.text('Hello')