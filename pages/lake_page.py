import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm

import pages.park_page as pp

lake_dataframe = None
park_dataframe = None

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

    for lake in tm.get_lake(searchterm):
        row = pd.DataFrame({'ID':str(lake[0]), 'Name':lake[1], 'Park ID':str(lake[2]), 'Type':lake[3], \
             'Depth':str(lake[4])}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    df.set_axis(['ID', 'Name', 'Park', 'Type', 'Depth (m)'], axis = 'columns', copy = False)

    return df

def draw_textbox():
    name = st.text_input('Lake', '', key = 'lake_drawTextBox')
    st.write('Searching for ', name)
    global lake_dataframe
    lake_dataframe = gen_lake_dataframe(name)

def modify():
    global lake_dataframe
    page_names = ['Update', 'Add', 'Delete']
    page = st.radio('Choose one', page_names, key = 'lake_selection')
    st.write('You selected', page)

    match page:
        case 'Update':
            update()
        case 'Add':
            add()
        case 'Delete':
            delete()
        case _:
            st.write('Error: Invalid page name')

    lake_dataframe = gen_lake_dataframe('')

def update():
    tempdf = lake_dataframe.sort_values(by = ['Name'])

    name = st.selectbox('Select a Lake to Modify', tempdf['Name'], key = 'lake_update_selectbox')
    attr = st.radio('Select an attribute to modify', 
        list(lake_dataframe.columns.values)[1:], key = 'lake_attr')

    if attr == 'Name':
        newAttr = st.text_input('Enter the new Name', key = 'lake_new_name')
    elif attr == 'Park ID':
        new_park = st.selectbox('Select Park:', list(pp.gen_park_dataframe('').sort_values(by = ['Name']).loc()[:, 'Name']), key = 'lake_new_park')
        tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
        newAttr = tm.mycursor.fetchone()[0]
    elif attr == 'Type':
        newAttr = st.text_input('Enter the new Type', key = 'lake_new_type')
    elif attr == 'Depth':
        newAttr = st.text_input('Enter the new Depth', key = 'lake_new_depth')
    
    if (st.button('Update', key = 'lake_update_button')):
        tm.update_lake(name, attr, newAttr)

def add():
    new_name = st.text_input('Enter Lake name:', key = 'lake_add_name')
    new_park = st.selectbox('Select Park', list(pp.gen_park_dataframe('').sort_values(by = ['Name']).loc()[:, 'Name']))
    tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
    new_park_id = tm.mycursor.fetchone()[0]
    new_type = st.text_input('Enter Lake type:', key = 'lake_add_type')
    new_depth = st.text_input('Enter Lake depth:', key = 'lake_add_depth')

    if (st.button('Add', key = 'sp_add_button')):
        tm.insert_lake(new_name, new_park_id, new_type, new_depth)

def delete():
    tempdf = lake_dataframe.sort_values(by = ['Name'])
    name = st.selectbox('Select a Lake to Delete', tempdf['Name'], key = 'lake_delete_selectbox')

    if (st.button('Delete', key = 'lake_delete_button')):
        tm.delete_lake(name)

def main():
    global lake_dataframe
    global park_dataframe
    lake_dataframe = gen_lake_dataframe('')
    park_dataframe = pp.gen_park_dataframe('')

    modify()
    draw_textbox()
    st.table(lake_dataframe)

main()