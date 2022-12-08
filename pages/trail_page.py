import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm

import pages.park_page as pp

trail_dataframe = None
park_dataframe = None

def gen_trail_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Park':[],
        'Distance (km)':[]
    }

    df = pd.DataFrame(dict)

    for trail in tm.get_trail(searchterm):
        row = pd.DataFrame({'ID':str(trail[0]), 'Name':trail[1], 'Park':str(trail[2]), 'Distance (km)':str(trail[3])}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    return df.set_axis(['ID', 'Name', 'Park', 'Distance (km)'], axis = 'columns', copy = False)

def modify():
    global trail_dataframe
    page_names = ['Update', 'Add', 'Delete']
    page = st.radio('Choose one', page_names, key="trail_selection")
    st.write('You selected:', page)

    if page == 'Update':
        update()
    elif page == 'Add':
        add()
    elif page == 'Delete':
        delete()

    trail_dataframe = gen_trail_dataframe('')

def update():
    tempdf = trail_dataframe.sort_values(by=['Name'])
    name = st.selectbox('Select a Trail to Modify',
        tempdf['Name'])

    attr = st.radio('Select an attribute to modify',
        list(trail_dataframe.columns.values)[1:], key="trail_attr")
    if attr == 'Name':
        newAttr = st.text_input('Enter new Name', key="trail_new_name")
    elif attr == 'Park':
        new_park = st.selectbox('Select Park:',
            list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
        tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
        newAttr = tm.mycursor.fetchone()[0]
    elif attr == 'Distance (km)':
        newAttr = st.number_input('Distance (km):')
    
    if(st.button('Update', key="trail_update_button")):
        tm.update_trail(name, attr, newAttr)
        tm.commitData()

def add():
    new_name = st.text_input('Enter Trail name:', key="trail_new_name2")
    new_park = st.selectbox('Select Park:', list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
    tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
    new_park_id = tm.mycursor.fetchone()[0]
    new_distance = st.number_input('Enter Distance (km):')

    if(st.button('Add', key="trail_add_button")):
        tm.insert_trail(new_name, new_park_id, new_distance)
        tm.commitData()

def delete():
    tempdf = gen_trail_dataframe('').sort_values(by=['Name']).loc()
    name = st.selectbox('Select a Trail to Delete',
        tempdf[:,'Name'])
    if(st.button('Delete', key="trail_delete_button")):
        tm.delete_trail(name)
        tm.commitData()

def draw_textbox():
    name = st.text_input('Trail', '')
    st.write('Searching for ', name)
    global trail_dataframe
    trail_dataframe = gen_trail_dataframe(name)

def main():
    global trail_dataframe
    global park_dataframe
    trail_dataframe = gen_trail_dataframe('')
    park_dataframe = pp.gen_park_dataframe('')

    modify()
    draw_textbox()
    st.table(trail_dataframe)

main()