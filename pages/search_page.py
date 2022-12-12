import streamlit as st
import pandas as pd
import tableManager as tm

import pages.country_page as cp
import pages.state_province_page as spp
import pages.park_page as pp
import pages.lake_page as lp
import pages.mountain_page as mp
import pages.trail_page as tp

joined_dataframe = None

lake_dataframe = None
mountain_dataframe = None
trail_dataframe = None

country, region = ['country_name', ''], ['region', '']
sp = ['state_province_name', '']
park = ['park_name', '']
area = ['area', [None, None]]
visitors = ['park_visitors_per_year', [None, None]]
year = ['year_established', [None, None]]
num_lakes = ['numLakes', [None, None]]
num_mountains = ['numMountains', [None, None]]
num_trails = ['numTrails', [None, None]]

def gen_joined_dataframe(params):
    dict = {
        'ID':[],
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

    for row in tm.get_filtered_joined_table(params):
        row = pd.DataFrame({'ID':str(row[0]), 
                            'Park':row[1], 
                            'Park Area':str(row[2]), 
                            'Visitors Per Year':row[3], 
                            'Year Established':str(row[4]), 
                            'State/Province':row[5], 
                            'Country':row[6], 
                            'Region':row[7], 
                            'Number of Lakes':str(row[8]), 
                            'Number of Mountains':str(row[9]), 
                            'Number of Trails':str(row[10])}, 
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)

    return df.set_axis(['Park ID', 'Park', 'Park Area (m)', 'Visitors Per Year', 'Year Established', 'State/Province', 'Country', 'Region', 'Number of Lakes', 'Number of Mountains', 'Number of Trails'], axis = 'columns', copy = False)

def gen_filtered_lake_dataframe():
    dict = {
        'ID':[],
        'Name':[],
        'Park':[],
        'Type':[],
        'Depth':[]
    }
    df = pd.DataFrame(dict)

    for lake in tm.get_lakes_from_filtered_joined_table():
        row = pd.DataFrame({'ID':str(lake[0]),
                            'Name':lake[1],
                            'Park':lake[2],
                            'Type':lake[3],
                            'Depth':str(lake[4])},
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)

    return df.set_axis(['ID', 'Name', 'Park', 'Type', 'Depth (m)'], axis = 'columns', copy = False)

def gen_filtered_mountain_dataframe():
    dict = {
        'ID':[],
        'Name':[],
        'Park':[],
        'Elevation':[]
    }
    df = pd.DataFrame(dict)

    for mountain in tm.get_mountains_from_filtered_joined_table():
        row = pd.DataFrame({'ID':str(mountain[0]),
                            'Name':mountain[1],
                            'Park':mountain[2],
                            'Elevation':str(mountain[3])},
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)

    return df.set_axis(['ID', 'Name', 'Park', 'Elevation (m)'], axis = 'columns', copy = False)

def gen_filtered_trail_dataframe():
    dict = {
        'ID':[],
        'Name':[],
        'Park':[],
        'Length':[]
    }
    df = pd.DataFrame(dict)

    for trail in tm.get_trails_from_filtered_joined_table():
        row = pd.DataFrame({'ID':str(trail[0]),
                            'Name':trail[1],
                            'Park':trail[2],
                            'Length':str(trail[3])},
                            index = [0])
        df = pd.concat([df.loc[:], row]).reset_index(drop = True)

    return df.set_axis(['ID', 'Name', 'Park', 'Length (m)'], axis = 'columns', copy = False)

# Sets up the filter section of the page
def set_up_filter_section():
    # Variable set up for filters
    global joined_dataframe
    

    # Container that holds the filters
    filter_container = st.container()
    with filter_container:
        st.subheader('Filters')

        # Split up filters along three columns
        left_column, middle_column, right_column = st.columns(3)

        # Variables used to store default filter values
        min_area = tm.get_min_area()[0]
        max_area = tm.get_max_area()[0]
        max_vpy = tm.get_max_visitors_per_year()[0]
        min_year = tm.get_min_year_established()[0]
        max_year = tm.get_max_year_established()[0]

        # THe following are converted from a set to a list to get rid of duplicates in the options
        num_lake_options = list(set(gen_joined_dataframe([]).sort_values(by=['Number of Lakes']).loc[:,'Number of Lakes']))
        num_lake_options.sort()
        num_mountain_options = list(set(gen_joined_dataframe([]).sort_values(by=['Number of Mountains']).loc[:,'Number of Mountains']))
        num_mountain_options.sort()
        num_trail_options = list(set(gen_joined_dataframe([]).sort_values(by=['Number of Trails']).loc[:,'Number of Trails']))
        num_trail_options.sort()

        if st.button('Reset Filters', key='reset_filters'):
                st.session_state.country_filter_selectbox = ''
                st.session_state.region_filter_selectbox = ''
                st.session_state.sp_filter_selectbox = ''
                st.session_state.park_filter_selectbox = ''
                st.session_state.park_area_filter_slider = [min_area, max_area]
                st.session_state.park_visitors_filter_slider = [0, max_vpy]
                st.session_state.park_year_established_filter_slider = [str(min_year), str(max_year)]
                st.session_state.park_num_lakes_filter_slider = [num_lake_options[0], num_lake_options[-1]]
                st.session_state.park_num_mountains_filter_slider = [num_mountain_options[0], num_mountain_options[-1]]
                st.session_state.park_num_trails_filter_slider = [num_trail_options[0], num_trail_options[-1]]

        with left_column:
            # Country filter setup
            country[1] = st.selectbox('Select a Country to filter by', [''] +
                list(cp.gen_country_dataframe('').sort_values(by=['Name']).loc()[:,'Name']), key='country_filter_selectbox')

            # Region filter setup
            regions = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

            # If the list of countries is not empty:
            if country[1] != '':
                # Extract the region names from selected country
                regions = tm.get_region_from_country_name(country[1])

                # Remove the tuple from the list
                for i in range(len(regions)):
                    regions[i] = regions[i][0]
                
                regions.sort()
            
            region[1] = st.selectbox('Select a Region to filter by', [''] + regions, key='region_filter_selectbox')
            
            # Setup Year Established slider
            year[1][0], year[1][1] = st.select_slider('Select the range of Year Established to filter by', list(pp.gen_park_dataframe('').sort_values(by=['Year Established']).loc()[:,'Year Established']), 
                value=[str(min_year), str(max_year)], key='park_year_established_filter_slider')

        with middle_column:             
            # State/Province filter setup
            sps = list(spp.gen_sp_dataframe('').sort_values(by=['Name']).loc()[:,'Name'])

            if country[1] != '':
                
                # Extract the state/province names from selected country
                sps = tm.get_state_province_name_from_country_name(country[1])
                
                # Remove the tuple from the list
                for i in range(len(sps)):
                    sps[i] = sps[i][0]

                sps.sort()

            sp[1] = st.selectbox('Select a State/Province to filter by', [''] + sps, key='sp_filter_selectbox')

            # Setup park area slider
            area_options = tm.get_all_areas()
            
            for i in range(len(area_options)):
                area_options[i] = area_options[i][0]

            area[1][0], area[1][1] = st.select_slider('Select the range of Park Area to filter by', area_options, 
                value=[min_area, max_area], key='park_area_filter_slider')

            # Setup Visitors per Year slider
            visitor_options = tm.get_all_visitors_per_year()

            for i in range(len(visitor_options)):
                visitor_options[i] = visitor_options[i][0]

            visitors[1][0], visitors[1][1] = st.select_slider('Select the range of Visitors per Year to filter by', visitor_options, 
                value=[0, max_vpy], key='park_visitors_filter_slider')

        with right_column:               
            # Setup park selectbox
            park[1] = st.selectbox('Select a Park to filter by', [''] +
                list(pp.gen_park_dataframe('').sort_values(by=['Name']).loc()[:,'Name']), key='park_filter_selectbox')

            # Setup Number of Lakes slider           
            num_lakes[1][0], num_lakes[1][1] = st.select_slider('Select the range of Number of Lakes', num_lake_options,
                value=[num_lake_options[0], num_lake_options[-1]], key='park_num_lakes_filter_slider')

            # Setup Number of Mountains slider
            num_mountains[1][0], num_mountains[1][1] = st.select_slider('Select the range of Number of Mountains', num_mountain_options,
                value=[num_mountain_options[0], num_mountain_options[-1]], key='park_num_mountains_filter_slider')

            # Setup Number of Trails slider
            num_trails[1][0], num_trails[1][1] = st.select_slider('Select the range of Number of Trails', num_trail_options,
                value=[num_trail_options[0], num_trail_options[-1]], key='park_num_trails_filter_slider')

# Sets up the main dataframe
def set_up_main_section():
    params = []

    # If a param is not empty, add it to the list of params
    if country[1] != '':
        params += [country]
    if region[1] != '':
        params += [region]
    if sp[1] != '':
        params += [sp]
    if park[1] != '':
        params += [park]
    if area[1] != [None, None]:
        params += [area]
    if visitors[1] != [None, None]:
        params += [visitors]
    if year[1] != [None, None]:
        params += [year]
    if num_lakes[1] != [None, None]:
        params += [num_lakes]
    if num_mountains[1] != [None, None]:
        params += [num_mountains]
    if num_trails[1] != [None, None]:
        params += [num_trails]

    global joined_dataframe
    joined_dataframe = gen_joined_dataframe(params)

    main_dataframe_container = st.container()
    with main_dataframe_container:
        st.table(joined_dataframe)

# Function for displaying the sub tables on the bottom of the screen
def set_up_subtable_section():
    sub_table_expander = st.expander('View Sub Tables')

    with sub_table_expander:
        sub_table_container = st.container()

        with sub_table_container:
            lake_column, mountain_column, trail_column = st.columns(3)

            with lake_column:
                st.subheader('Lakes')
                global lake_dataframe
                lake_dataframe = gen_filtered_lake_dataframe()
                st.table(lake_dataframe)

            with mountain_column:
                st.subheader('Mountains')
                global mountain_dataframe
                mountain_dataframe = gen_filtered_mountain_dataframe()
                st.table(mountain_dataframe)

            with trail_column:
                st.subheader('Trails')
                global trail_dataframe
                trail_dataframe = gen_filtered_trail_dataframe()
                st.table(trail_dataframe)

def main():
    # Sets the page config to be wide
    st.set_page_config(
        page_title="Search Page",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    set_up_filter_section()
    set_up_main_section()
    set_up_subtable_section()
    
main()