import streamlit as st
import pandas as pd
import tableManager as tm

import pages.park_page as pp

lake_dataframe = None

# Generate the Lake Dataframe
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

    # Fill in the dataframe, filter by the searchterm
    for lake in tm.get_lake(searchterm):
        row = pd.DataFrame({'ID':str(lake[0]), 
                            'Name':lake[1], 
                            'Park ID':str(lake[2]), 
                            'Type':lake[3], 
                            'Depth':str(lake[4])}, 
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    return df.set_axis(['ID', 'Name', 'Park', 'Type', 'Depth (m)'], axis = 'columns', copy = False)

# Draw the text box for the Lake
def draw_textbox():
    name = st.text_input('Lake', '', key='lake_drawTextBox')
    st.write('Searching for ', name)
    global lake_dataframe
    lake_dataframe = gen_lake_dataframe(name)

# Modify the Lake
def modify():
    page = st.radio('Choose one', ['Update', 'Add', 'Delete'], key='lake_selection')
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

    global lake_dataframe
    lake_dataframe = gen_lake_dataframe('')

def update():
    # Select box for name of Lake to modify
    name = st.selectbox('Select a Lake to Modify', 
                        lake_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    # Radio selection for attribute to modify
    attr = st.radio('Select an attribute to modify', 
                    list(lake_dataframe.columns.values)[1:], key='lake_attr')

    # Match statement for different attributes to change
    match attr:
        case 'Name':
            newAttr = st.text_input('Enter the new Name', key='lake_new_name')
        case 'Park':
            new_park = st.selectbox('Select Park:', 
                                    list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:, 'Name']))
            tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
            newAttr = tm.mycursor.fetchone()[0] # Get the Park ID from the Park
        case 'Type':
            newAttr = st.text_input('Enter the new Type', key='lake_new_type')
        case 'Depth (m)':
            newAttr = st.number_input('Enter the new Depth', key='lake_new_depth')
    
    # Button to apply changes
    if (st.button('Update', key='lake_update_button')):
        tm.update_lake(name, attr, newAttr)

def add():
    # Text box for new Lake name
    new_name = st.text_input('Enter Lake name:', key='lake_add_name')
    # Select box for Park
    new_park = st.selectbox('Select Park', 
                            list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:, 'Name']))
    tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
    new_park_id = tm.mycursor.fetchone()[0] # Get the Park ID from the Park
    # Text box for the Lake types
    new_type = st.text_input('Enter Lake type:', key='lake_add_type')
    # Number input box for Lake depth
    new_depth = st.number_input('Enter Lake depth:', key='lake_add_depth')

    # Button to add Lake
    if (st.button('Add', key='sp_add_button')):
        tm.insert_lake(new_name, new_park_id, new_type, new_depth)

def delete():
    # Select box for Lake to delete
    name = st.selectbox('Select a Lake to Delete', 
                        lake_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    
    # Button to delete Lake
    if (st.button('Delete', key='lake_delete_button')):
        tm.delete_lake(name)

# Main method
def main():
    # Initializing the local Lake dataframe
    global lake_dataframe
    lake_dataframe = gen_lake_dataframe('')

    modify()
    draw_textbox()
    st.table(lake_dataframe)

main()