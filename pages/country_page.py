import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm

country_dataframe = None

def gen_country_dataframe(searchterm):
    # Empty dictionary to be drawn in the table
    dict = {
        'ID':[],
        'Name':[],
        'Region':[]
    }

    df = pd.DataFrame(dict)

    for country in tm.get_country(searchterm):
        row = pd.DataFrame({'ID':str(country[0]), 'Name':country[1], 'Region':country[2]}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)

    return df.set_axis(['ID', 'Name', 'Region'], axis = 'columns', copy = False)

def draw_textbox():
    name = st.text_input('Country', '', key = 'country_drawTextBox')
    st.write('Searching for ', name)
    global country_dataframe
    country_dataframe = gen_country_dataframe(name)

def modify():
    global country_dataframe
    page_names = ['Update', 'Add', 'Delete']
    page = st.radio('Choose one', page_names, key="country_selection")
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

    country_dataframe = gen_country_dataframe('')

def update():
    tempdf = country_dataframe.sort_values(by=['Name'])
    name = st.selectbox('Select a Country to Modify',
        tempdf['Name'])
    attr = st.radio('Select an attribute to modify',
        list(country_dataframe.columns.values)[1:], key="country_attr")
    if attr == 'Name':
        newAttr = st.text_input('Enter new Name')
    elif attr == 'Region':
        newAttr = st.selectbox('Select Region:',
            ['Africa', 'Asia', 'North America', 'South America', 'Oceania', 'Europe'])
    if(st.button('Update', key="country_update_button")):
        tm.update_country(name, attr, newAttr)

def add():
    new_name = st.text_input('Enter Country name:')
    new_region = st.selectbox('Select Region:',
            ['Africa', 'Asia', 'North America', 'South America', 'Oceania', 'Europe'])
    if(st.button('Add', key="country_add_button")):
        tm.insert_country(new_name, new_region)

def delete():
    tempdf = country_dataframe.sort_values(by=['Name'])
    name = st.selectbox('Select a Country to Delete',
        tempdf['Name'])
    if(st.button('Delete', key="country_delete_button")):
        tm.delete_country(name)

def main():

    global country_dataframe
    country_dataframe = gen_country_dataframe('')  

    modify()
    draw_textbox()
    st.table(country_dataframe)

main()