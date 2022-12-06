#importing streamlit library
import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm
import streamlit_app as sta

import pages.country_page as cp

mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "NationalParks"
    )

mycursor = mydb.cursor()

sp_dataframe = None

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


    df.set_axis(['ID', 'Name', 'Country ID'], axis = 'columns', copy = False)
    
    # return the dataframe
    return df

def draw_textbox():
    st.write('SEARCH')
    name = st.text_input('State/Province', '')
    st.write('Searching for ', name)
    global sp_dataframe
    sp_dataframe = gen_sp_dataframe(name)

def modify():

    page_names = ['Update', 'Add', 'Delete']
    page = st.radio('Choose one', page_names)
    st.write('You selected:', page)

    if page == 'Update':
        global sp_dataframe
        tempdf = sp_dataframe.sort_values(by=['Name'])
        spName = st.selectbox('Select a Province to Modify',
            tempdf['Name'])
        # Get info about current state/province. Set the new name and country id to the old name and country id
        new_name = spName
        mycursor.execute("""SELECT country_id FROM state_province WHERE name = %s""", (spName, ))
        new_country_id = mycursor.fetchone()


        attr = st.radio('Select an attribute to modify',
            list(sp_dataframe.columns.values)[1:])
        if attr == 'Name':
            new_name = st.text_input('Enter new Name')
        elif attr == 'Country ID':
            new_country = st.selectbox('Select country:',
                list(cp.gen_country_dataframe("").loc()[:,'Name']))
            mycursor.execute("""SELECT id FROM country WHERE name = %s""", (new_country, ))
            new_country_id = mycursor.fetchone()[0]
        
        if(st.button('Update')):
            tm.update_state_province(mycursor, new_name, attr, new_country_id)
            mydb.commit()


    elif page == 'Add':
        new_name = st.text_input('Enter State/Province name:')
        new_country = st.selectbox('Select country:',
            list(cp.gen_country_dataframe("").loc()[:,'Name']))
        mycursor.execute("""SELECT id FROM country WHERE name = %s""", (new_country, ))
        new_country_id = mycursor.fetchone()[0]
        if(st.button('Add')):
            tm.insert_state_province(mycursor, new_name, new_country_id)
            mydb.commit()
    elif page == 'Delete':
        tempdf = sp_dataframe.sort_values(by=['Name'])
        spName = st.selectbox('Select a Province to Delete',
            tempdf['Name'])
        if(st.button('Delete')):
            tm.delete_state_province(mycursor, spName)
            mydb.commit()

    sp_dataframe = gen_sp_dataframe('')


def main():
    print("reset")
    # writing simple text
    # st.text("Hello")

    global sp_dataframe
    sp_dataframe = gen_sp_dataframe('')    
    
    modify()
    draw_textbox()
    st.table(sp_dataframe)

    # st.table(cp.gen_country_dataframe(""))

main()