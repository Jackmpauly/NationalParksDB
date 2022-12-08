import streamlit as st
import pandas as pd
import tableManager as tm

country_dataframe = None

# Generate the Country dataframe
def gen_country_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Region':[]
    }
    df = pd.DataFrame(dict)

    # Fill in the dataframe, filter by the searchterm
    for country in tm.get_country(searchterm):
        row = pd.DataFrame({'ID':str(country[0]), 
                            'Name':country[1], 
                            'Region':country[2]}, 
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)

    return df.set_axis(['ID', 'Name', 'Region'], axis = 'columns', copy = False)

# Draw the text box for the Country
def draw_textbox():
    name = st.text_input('Country', '', key='country_drawTextBox')
    st.write('Searching for ', name)
    global country_dataframe
    country_dataframe = gen_country_dataframe(name)

# Modify the Country
def modify():
    page = st.radio('Choose one', ['Update', 'Add', 'Delete'], key='country_selection')
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

    global country_dataframe
    country_dataframe = gen_country_dataframe('')

def update():
    # Select box for Country to modify
    name = st.selectbox('Select a Country to Modify', 
                        country_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    # Radio selection for attribute to modify
    attr = st.radio('Select an attribute to modify',
                    list(country_dataframe.columns.values)[1:], key='country_attr')
    
    # Match statement for different attributes to change
    match attr:
        case 'Name':
            newAttr = st.text_input('Enter new Name', key='country_new_name')
        case 'Region':
            newAttr = st.selectbox('Select Region:', 
                                    ['Africa', 'Asia', 'North America', 'South America', 'Oceania', 'Europe'])
    
    # Button to apply changes
    if(st.button('Apply', key='country_update_button')):
        tm.update_country(name, attr, newAttr)

def add():
    # Text box for new Country name
    new_name = st.text_input('Enter Country name:', key='country_add_name')
    # Select box for Region
    new_region = st.selectbox('Select Region:',
                                ['Africa', 'Asia', 'North America', 'South America', 'Oceania', 'Europe'])
    
    # Button to add Country
    if(st.button('Add', key='country_add_button')):
        tm.insert_country(new_name, new_region)

def delete():
    # Select box for Country to delete
    name = st.selectbox('Select a Country to Delete',
                        country_dataframe.sort_values(by=['Name']).loc()[:,'Name'])
    # Button to delete Country
    if(st.button('Delete', key='country_delete_button')):
        tm.delete_country(name)

# Main method
def main():
    # Initializing the local Country dataframe 
    global country_dataframe
    country_dataframe = gen_country_dataframe('')  
    
    modify()
    draw_textbox()
    st.table(country_dataframe)

main()