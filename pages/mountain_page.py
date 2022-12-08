import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm

import pages.park_page as pp

mountain_dataframe = None
park_dataframe = None

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
    
    df.set_axis(['ID', 'Name', 'Park', 'Elevation (m)'], axis = 'columns', copy = False)

    return df

def draw_textbox():
    name = st.text_input('Mountain', '', key = 'mountain_drawTextBox')
    st.write('Searching for ', name)
    global mountain_dataframe
    mountain_dataframe = gen_mountain_dataframe(name)

def modify():
    global mountain_dataframe
    page_names = ['Update', 'Add', 'Delete']
    page = st.radio('Choose one', page_names, key = 'mountain_selection')

    match page:
        case 'Update':
            update()
        case 'Add':
            add()
        case 'Delete':
            delete()
        case _:
            st.write('Error: Invalid page name')

    mountain_dataframe = gen_mountain_dataframe('')

def update():
    tempdf = mountain_dataframe.sort_values(by = ['Name'])

    name = st.selectbox('Select a Mountain to modify', tempdf['Name'], key = 'mountain_update_selectbox')
    attr = st.radio('Select an attribute to modify', 
        list(mountain_dataframe.columns.values)[1:], key = 'mountain_attr')

    match attr:
        case 'Name':
            newAttr = st.text_input('Enter the new name', key = 'mountain_new_name')
        case 'Park ID':
            new_park = st.selectbox('Select Park:', list(pp.gen_park_dataframe('').sort_values(by = ['Name']).loc()[:, 'Name']), key = 'mountain_new_park')
            tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
            newAttr = tm.mycursor.fetchone()[0]
        case 'Elevation':
            newAttr = st.text_input('Enter the new elevation', key = 'mountain_new_elevation')

    if (st.button('Update', key = 'mountain_update_button')):
        tm.update_mountain(name, attr, newAttr)

def add():
    new_name = st.text_input('Enter Mountain name:', key = 'mountain_add_name')
    new_park = st.selectbox('Select Park', list(pp.gen_park_dataframe('').sort_values(by = ['Name']).loc()[:, 'Name']))
    tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
    new_park_id = tm.mycursor.fetchone()[0]
    new_elevation = st.text_input('Enter Mountain elevation:', key = 'mountain_add_elevation')

    if (st.button('Add', key = 'mountain_add_button')):
        tm.insert_mountain(new_name, new_park_id, new_elevation)

def delete():
    tempdf = mountain_dataframe.sort_values(by = ['Name'])
    name = st.selectbox('Select a Mountain to delete', tempdf['Name'], key = 'mountain_delete_selectbox')

    if (st.button('Delete', key = 'mountain_delete_button')):
        tm.delete_mountain(name)

def main():
    global mountain_dataframe
    global park_dataframe
    mountain_dataframe = gen_mountain_dataframe('')
    park_dataframe = pp.gen_park_dataframe('')

    modify()
    draw_textbox()
    st.table(mountain_dataframe)

main()