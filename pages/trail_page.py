import streamlit as st
import pandas as pd
import tableManager as tm

import pages.park_page as pp

trail_dataframe = None

def gen_trail_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Park ID':[],
        'Distance':[]
    }

    df = pd.DataFrame(dict)

    # Fill in the dataframe, filter by searchterm
    for trail in tm.get_trail(searchterm):
        row = pd.DataFrame({'ID':str(trail[0]), 
                            'Name':trail[1], 
                            'Park ID':str(trail[2]), 
                            'Distance':str(trail[3])}, 
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    return df.set_axis(['ID', 'Name', 'Park', 'Distance (km)'], axis = 'columns', copy = False)

# Draw the text box for the Trail
def draw_textbox():
    name = st.text_input('Trail', '', key='trail_drawTextBox')
    st.write('Searching for ', name)
    global trail_dataframe
    trail_dataframe = gen_trail_dataframe(name)

# Modify the Trail
def modify():
    page = st.radio('Choose one', ['Update', 'Add', 'Delete'], key="trail_selection")
    st.write('You selected:', page)

    match page:
        case 'Update':
            update()
        case 'Add':
            add()
        case 'Delete':
            delete()
        case _:
            st.write('Error: Invalid page name')

    global trail_dataframe
    trail_dataframe = gen_trail_dataframe('')

def update():
    # Select box for name of Trail to modify
    name = st.selectbox('Select a Trail to Modify',
                        trail_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    
    # Radio selection for attribute to modify
    attr = st.radio('Select an attribute to modify',
                    list(trail_dataframe.columns.values)[1:], key="trail_attr")
    
    # Match statement for different attributes to change
    match attr:
        case 'Name':
            newAttr = st.text_input('Enter new Name', key="trail_new_name")
        case 'Park':
            new_park = st.selectbox('Select Park:',
                list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
            tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
            newAttr = tm.mycursor.fetchone()[0]
        case 'Distance (km)':
            newAttr = st.number_input('Distance (km):', key='trail_new_distance')
    
    # Button to apply changes
    if(st.button('Update', key="trail_update_button")):
        tm.update_trail(name, attr, newAttr)

def add():
    # Text box for new Trail name
    new_name = st.text_input('Enter Trail name:', key="trail_add_name")
    # Select box for Park
    new_park = st.selectbox('Select Park:', 
                            list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
    tm.mycursor.execute("""SELECT id FROM park WHERE name = %s""", (new_park, ))
    new_park_id = tm.mycursor.fetchone()[0] # Get the Park ID from the Park
    # Number input box for Distance
    new_distance = st.number_input('Enter Distance (km):')

    # Button to add Trail
    if(st.button('Add', key="trail_add_button")):
        tm.insert_trail(new_name, new_park_id, new_distance)

def delete():
    # Select box for Trail to delete
    name = st.selectbox('Select a Trail to Delete',
        gen_trail_dataframe('').sort_values(by=['Name']).loc()[:,'Name'])
    
    # Button to delete Trail
    if(st.button('Delete', key="trail_delete_button")):
        tm.delete_trail(name)

# Main method
def main():
    # Initializing the local Trail dataframe
    global trail_dataframe
    trail_dataframe = gen_trail_dataframe('')

    modify()
    draw_textbox()
    st.table(trail_dataframe)

main()