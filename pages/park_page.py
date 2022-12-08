import streamlit as st
import pandas as pd
import tableManager as tm
import datetime


import pages.state_province_page as spp

park_dataframe = None

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

    for park in tm.get_park(searchterm):
        row = pd.DataFrame({'ID':str(park[0]), 'Name':park[1], 'Visitors Per Year':park[2], 'State/Province':str(park[3]),
             'Area (km sqd)':str(park[4]), 'Year Established':str(park[5])}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)
    
    return df.set_axis(['ID', 'Name', 'Visitors Per Year', 'State/Province', 'Area', 'Year Established'], axis = 'columns', copy = False)

def draw_textbox():
    name = st.text_input('Park', '')
    st.write('Searching for ', name)
    global park_dataframe
    park_dataframe = gen_park_dataframe(name)

def modify():
    global park_dataframe
    page_names = ['Update', 'Add', 'Delete']
    page = st.radio('Choose one', page_names, key="park_selection")
    st.write('You selected:', page)

    if page == 'Update':
        update()
    elif page == 'Add':
        add()
    elif page == 'Delete':
        delete()

    park_dataframe = gen_park_dataframe('')

def update():
    tempdf = park_dataframe.sort_values(by=['Name'])
    name = st.selectbox('Select a Park to Modify',
        tempdf['Name'])

    attr = st.radio('Select an attribute to modify',
        list(park_dataframe.columns.values)[1:], key="park_attr")
    if attr == 'Name':
        newAttr = st.text_input('Enter new Name', key="park_new_name")
    elif attr == 'Visitors Per Year':
        newAttr = st.number_input('Visitors Per Year', step=1)
    elif attr == 'State/Province':
        new_state_prov = st.selectbox('Select State/Province:',
            list(spp.gen_sp_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
        tm.mycursor.execute("""SELECT id FROM state_province WHERE name = %s""", (new_state_prov, ))
        newAttr = tm.mycursor.fetchone()[0]
    elif attr == 'Area (km sqd)':
        newAttr = st.number_input('Area:')
    elif attr == 'Year Established':
        year = datetime.datetime.today().year
        newAttr = st.selectbox('Select Year:',
        range(year, year-200, -1))
    
    if(st.button('Update', key="sp_update_button")):
        tm.update_state_province(name, attr, newAttr)
        tm.commitData()

def add():
    new_name = st.text_input('Enter Park name:', key="park_new_name2")
    new_visitors_per_year = st.number_input('Visitors Per Year', step=1)
    new_state_prov = st.selectbox('Select State/Province:',
        list(spp.gen_sp_dataframe('').sort_values(by=['Name']).loc()[:,'Name']))
    tm.mycursor.execute("""SELECT id FROM state_province WHERE name = %s""", (new_state_prov, ))
    new_sp_id = tm.mycursor.fetchone()[0]
    new_area = st.number_input('Area:')
    year = datetime.datetime.today().year
    new_year_established = st.selectbox('Select Year:',
    range(year, year-200, -1))

    if(st.button('Add', key="sp_add_button")):
        tm.insert_park(new_name, new_visitors_per_year, new_sp_id, new_area, new_year_established)
        tm.commitData()

def delete():
    tempdf = park_dataframe.sort_values(by=['Name'])
    name = st.selectbox('Select a Park to Delete',
        tempdf['Name'])
    if(st.button('Delete', key="park_delete_button")):
        tm.delete_park(name)
        tm.commitData()


def main():
    global park_dataframe
    park_dataframe = gen_park_dataframe('')

    modify()
    draw_textbox()
    st.table(park_dataframe)

main()