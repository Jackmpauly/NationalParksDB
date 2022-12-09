import streamlit as st
import pandas as pd
import tableManager as tm

joined_dataframe = None
lake_dataframe = None
mountain_dataframe = None
trail_dataframe = None

def gen_joined_dataframe():
    dict = {
        'Park':[],
        'Park Area':[],
        'Visitors Per Year':[],
        'Year Established':[],
        'State/Province':[],
        'Country':[],
        'Region':[],
        'Number of Lakes':[],
        'Number of Mountains':[],
        'Number of Trails':[]
    }

    df = pd.DataFrame(dict)

    for row in tm.get_joined_table():
        row = pd.DataFrame({'Park':row[0], 'Park Area':str(row[1]), 'Visitors Per Year':row[2], 'Year Established':str(row[3]), 'State/Province':row[4], 'Country':row[5], 'Region':row[6], 'Number of Lakes':str(row[7]), 'Number of Mountains':str(row[8]), 'Number of Trails':str(row[9])}, index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)

    return df.set_axis(['Park', 'Park Area (m)', 'Visitors Per Year', 'Year Established', 'State/Province', 'Country', 'Region', 'Number of Lakes', 'Number of Mountains', 'Number of Trails'], axis = 'columns', copy = False)

def main():
    filter_container = st.container()
    with filter_container:
        st.header('Filters')
        left_column, middle_column, right_column = st.columns(3)

        with left_column:
            st.subheader('Country')
            
        with middle_column:    
            st.subheader('State/Province')

        with right_column:
            st.subheader('Park')

    
    global joined_dataframe
    joined_dataframe = gen_joined_dataframe()
    st.table(joined_dataframe)

main()