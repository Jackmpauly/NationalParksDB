import streamlit as st
import pandas as pd
import tableManager as tm

import pages.country_page as cp

sp_dataframe = None

# Generate the State/Province dataframe
def gen_sp_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Country':[]
    }
    df = pd.DataFrame(dict)
    
    # Fill in the dataframe, filter by the searchterm
    for x in tm.get_state_province(searchterm):
        row = pd.DataFrame({'ID':str(x[0]), 
                            'Name':x[1], 
                            'Country':str(x[2]) }, 
                            index=[0])
        df = pd.concat([df.loc[:], row]).reset_index(drop=True)

    return df.set_axis(['ID', 'Name', 'Country'], axis = 'columns', copy = False)

# Draw the text box for the State/Province
def draw_textbox():
    name = st.text_input('State/Province', '', key='sp_drawTextBox')
    st.write('Searching for ', name)
    global sp_dataframe
    sp_dataframe = gen_sp_dataframe(name)

# Modify the State/Province
def modify():
    page = st.radio('Choose one', ['Update', 'Add', 'Delete'], key='sp_selection')
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

    global sp_dataframe
    sp_dataframe = gen_sp_dataframe('')

def update():
    # Select box for Province to modify
    name = st.selectbox('Select a Province to Modify',
                        sp_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    # Radio selection for attribute to modify
    attr = st.radio('Select an attribute to modify',
                    list(sp_dataframe.columns.values)[1:], key='sp_attr')
    
    # Match statement for different attributes to change
    match attr:
        case 'Name':
            newAttr = st.text_input('Enter new Name', key='sp_new_name')
        case 'Country':
            new_country = st.selectbox('Select country:',
                                        list(cp.gen_country_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
            tm.mycursor.execute("""SELECT id FROM country WHERE name = %s""", (new_country, ))
            newAttr = tm.mycursor.fetchone()[0] # Get the Country ID from the Country
    
    # Button to apply changes
    if(st.button('Apply', key='sp_update_button')):
        tm.update_state_province(name, attr, newAttr)

def add():
    # Text box for new State/Province name
    new_name = st.text_input('Enter State/Province name:', key='sp_add_name')
    # Select box for Country
    new_country = st.selectbox('Select country:',
                                list(cp.gen_country_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
    tm.mycursor.execute("""SELECT id FROM country WHERE name = %s""", (new_country, ))
    new_country_id = tm.mycursor.fetchone()[0] # Get the Country ID from the Country

    # Button to add State/Province
    if(st.button('Add', key='sp_add_button')):
        tm.insert_state_province(new_name, new_country_id)

def delete():
    # Select box for Province to delete
    name = st.selectbox('Select a State/Province to Delete',
                        sp_dataframe.sort_values(by=['Name']).loc()['Name'])
    
    # Button to delete Country
    if(st.button('Delete', key='sp_delete_button')):
        tm.delete_state_province(name)

# Main method
def main():
    # Initializing the local State/Province dataframe
    global sp_dataframe
    sp_dataframe = gen_sp_dataframe('')

    modify()
    draw_textbox()
    st.table(sp_dataframe)

main()