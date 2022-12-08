#importing streamlit library
import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm


import pages.country_page as cp

sp_dataframe = None
country_dataframe = None

def gen_sp_dataframe(searchterm):
    # create the empty dict (to be drawn in the table)
    dict = {
        'ID':[],
        'Name':[],
        'Country':[]
    }
    df = pd.DataFrame(dict)

    # loop through the state_province table and create rows, then enter them into the dataframe
    for x in tm.get_state_province(searchterm):
        row = pd.DataFrame({ 'ID':str(x[0]), 'Name':x[1], 'Country':str(x[2]) }, index=[0])
        df = pd.concat([df.loc[:], row]).reset_index(drop=True)


    df.set_axis(['ID', 'Name', 'Country'], axis = 'columns', copy = False)
    
    # return the dataframe
    return df

def draw_textbox():
    name = st.text_input('State/Province', '', key="sp_drawTextBox")
    st.write('Searching for ', name)
    global sp_dataframe
    sp_dataframe = gen_sp_dataframe(name)

def modify():
    global sp_dataframe
    page_names = ['Update', 'Add', 'Delete']
    page = st.radio('Choose one', page_names, key="sp_selection")
    st.write('You selected:', page)

    if page == 'Update':
        update()
    elif page == 'Add':
        add()
    elif page == 'Delete':
        delete()

    sp_dataframe = gen_sp_dataframe('')

def update():
    tempdf = sp_dataframe.sort_values(by=['Name'])
    # Get info about current state/province. Set the new name and country id to the old name and country id
    name = st.selectbox('Select a Province to Modify',
        tempdf['Name'])

    attr = st.radio('Select an attribute to modify',
        list(sp_dataframe.columns.values)[1:], key="sp_attr")
    if attr == 'Name':
        newAttr = st.text_input('Enter new Name', key="sp_new_name")
    elif attr == 'Country':
        new_country = st.selectbox('Select country:',
            list(cp.gen_country_dataframe('').loc()[:,'Name']))
        tm.mycursor.execute("""SELECT id FROM country WHERE name = %s""", (new_country, ))
        newAttr = tm.mycursor.fetchone()[0]
    
    if(st.button('Update', key="sp_update_button")):
        tm.update_state_province(name, attr, newAttr)

def add():
    new_name = st.text_input('Enter State/Province name:', key="sp_new_name2")
    new_country = st.selectbox('Select country:',
        list(cp.gen_country_dataframe('').loc()[:,'Name']))
    tm.mycursor.execute("""SELECT id FROM country WHERE name = %s""", (new_country, ))
    new_country_id = tm.mycursor.fetchone()[0]
    if(st.button('Add', key="sp_add_button")):
        tm.insert_state_province(new_name, new_country_id)

def delete():
    tempdf = sp_dataframe.sort_values(by=['Name'])
    name = st.selectbox('Select a Province to Delete',
        tempdf['Name'])
    if(st.button('Delete', key="sp_delete_button")):
        tm.delete_state_province(name)

def main():
    print("reset")
    # writing simple text
    # st.text("Hello")

    global sp_dataframe
    sp_dataframe = gen_sp_dataframe('')    

    global country_dataframe
    country_dataframe = cp.gen_country_dataframe('')
    


    modify()
    draw_textbox()
    st.table(sp_dataframe)

    # st.table(cp.gen_country_dataframe(""))

main()