import streamlit as st
import pandas as pd
import tableManager as tm
import datetime

import pages.state_province_page as spp

park_dataframe = None

# Generate the park dataframe
def gen_park_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Visitors Per Year':[],
        'State/Province':[],
        'Area (km sqd)':[],
        'Year Established':[]
    }
    df = pd.DataFrame(dict)

    # Fill in the dataframe, filter by the searchterm
    for park in tm.get_park(searchterm):
        row = pd.DataFrame({'ID':str(park[0]), 
                            'Name':park[1], 
                            'Visitors Per Year':park[2], 
                            'State/Province':str(park[3]), 
                            'Area (km sqd)':str(park[4]), 
                            'Year Established':str(park[5])}, 
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    return df.set_axis(['ID', 'Name', 'Visitors Per Year', 'State/Province', 'Area', 'Year Established'], axis = 'columns', copy = False)

# Draw the text box for the Park
def draw_textbox():
    name = st.text_input('Park', '', key='park_drawTextBox')
    st.write('Searching for ', name)
    global park_dataframe
    park_dataframe = gen_park_dataframe(name)

# Modify the Park
def modify():
    page = st.radio('Choose one', ['Update', 'Add', 'Delete'], key='park_selection')
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

    global park_dataframe
    park_dataframe = gen_park_dataframe('')

def update():
    # Select box for name of Park to modify
    name = st.selectbox('Select a Park to Modify',
                        park_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    # Radio selection for attribute to modify
    attr = st.radio('Select an attribute to modify',
                    list(park_dataframe.columns.values)[1:], key="park_attr")
    
    # Match statement for different attributes to change
    match attr:
        case 'Name':
            newAttr = st.text_input('Enter new Name', key="park_new_name")
        case 'Visitors Per Year':
            newAttr = st.number_input('Visitors Per Year', step=1, key='park_new_visitors_per_year')
        case 'State/Province':
            new_state_prov = st.selectbox('Select State/Province:',
                                            list(spp.gen_sp_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
            tm.mycursor.execute("""SELECT id FROM state_province WHERE name = %s""", (new_state_prov, ))
            newAttr = tm.mycursor.fetchone()[0] # Get the State/Province ID from the State/Province
        case 'Area (km sqd)':
            newAttr = st.number_input('Area:', key='park_new_area')
        case 'Year Established':
            year = datetime.datetime.today().year
            newAttr = st.selectbox('Select Year:',
                                    range(year, year-200, -1))
            
    # Button to apply changes
    if(st.button('Apply', key="park_update_button")):
        tm.update_state_province(name, attr, newAttr)

def add():
    # Text box for new Park name
    new_name = st.text_input('Enter Park name:', key="park_add_name")
    # Number input box for Visitors Per Year
    new_visitors_per_year = st.number_input('Visitors Per Year', step=1)
    # Select box for State/Province
    new_state_prov = st.selectbox('Select State/Province:',
                                    list(spp.gen_sp_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
    tm.mycursor.execute("""SELECT id FROM state_province WHERE name = %s""", (new_state_prov, ))
    new_sp_id = tm.mycursor.fetchone()[0] # Get the State/Province ID from the State/Province
    # Number input box for Area
    new_area = st.number_input('Area:')
    # Select box for Year
    year = datetime.datetime.today().year
    new_year_established = st.selectbox('Select Year:',
    range(year, year-200, -1))

    # Button to add Park
    if(st.button('Add', key="park_add_button")):
        tm.insert_park(new_name, new_visitors_per_year, new_sp_id, new_area, new_year_established)

def delete():
    # Select box for Park to delete
    name = st.selectbox('Select a Park to Delete',
                        park_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    
    # Button to delete Park
    if(st.button('Delete', key="park_delete_button")):
        tm.delete_park(name)

# Main method
def main():
    # Initializing the local Park dataframe
    global park_dataframe
    park_dataframe = gen_park_dataframe('')

    modify()
    draw_textbox()
    st.table(park_dataframe)

main()