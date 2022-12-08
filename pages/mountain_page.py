import streamlit as st
import pandas as pd
import tableManager as tm

import pages.park_page as pp

mountain_dataframe = None
park_dataframe = None

# Generate the mountain dataframe 
def gen_mountain_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Park ID':[],
        'Elevation':[]
    }
    df = pd.DataFrame(dict)

    # Fill in the dataframe, filter by the searchterm
    for mountain in tm.get_mountain(searchterm):
        row = pd.DataFrame({'ID':str(mountain[0]), 
                            'Name':mountain[1], 
                            'Park ID':str(mountain[2]), 
                            'Elevation':str(mountain[3])}, 
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    return df.set_axis(['ID', 'Name', 'Park', 'Elevation (m)'], axis = 'columns', copy = False)

# Draw the text box for the Mountain
def draw_textbox():
    name = st.text_input('Mountain', '', key = 'mountain_drawTextBox')
    st.write('Searching for ', name)
    global mountain_dataframe
    mountain_dataframe = gen_mountain_dataframe(name)

# Modify the Mountain
def modify():
    page = st.radio('Choose one', ['Update', 'Add', 'Delete'], key='mountain_selection')

    match page:
        case 'Update':
            update()
        case 'Add':
            add()
        case 'Delete':
            delete()
        case _:
            st.write('Error: Invalid page name')

    global mountain_dataframe
    mountain_dataframe = gen_mountain_dataframe('')

def update():
    # Select box for name of Mountain to modify
    name = st.selectbox('Select a Mountain to modify', 
                        mountain_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    # Radio selection for attribute to modify
    attr = st.radio('Select an attribute to modify', 
                    list(mountain_dataframe.columns.values)[1:], key='mountain_attr')
    
    # Match statement for different attributes to change
    match attr:
        case 'Name':
            newAttr = st.text_input('Enter the new name', key='mountain_new_name')
        case 'Park ID':
            new_park = st.selectbox('Select Park:', 
                                    list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:, 'Name']))
            tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
            newAttr = tm.mycursor.fetchone()[0] # Get the Park ID from the Park
        case 'Elevation':
            newAttr = st.number_input('Enter the new elevation', key='mountain_new_elevation')

    # Button to apply changes
    if (st.button('Update', key='mountain_update_button')):
        tm.update_mountain(name, attr, newAttr)

def add():
    # Textbox for Mountain name
    new_name = st.text_input('Enter Mountain name:', key='mountain_add_name')
    # Select box for Park
    new_park = st.selectbox('Select Park', 
                            list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:, 'Name']))
    tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
    new_park_id = tm.mycursor.fetchone()[0] # Get the Park ID from the Park
    # Number input box for Mountain elevation
    new_elevation = st.number_input('Enter Mountain elevation:', key='mountain_add_elevation')

    # Button to add Mountain
    if (st.button('Add', key='mountain_add_button')):
        tm.insert_mountain(new_name, new_park_id, new_elevation)

def delete():
    # Select box for Mountain to delete
    name = st.selectbox('Select a Mountain to delete', 
                        mountain_dataframe.sort_values(by=['Name']).loc()[:,'Name'])

    # Button to delete Mountain
    if (st.button('Delete', key='mountain_delete_button')):
        tm.delete_mountain(name)

# Main method
def main():
    # Initializing the local Mountain dataframe
    global mountain_dataframe
    mountain_dataframe = gen_mountain_dataframe('')

    modify()
    draw_textbox()
    st.table(mountain_dataframe)

main()