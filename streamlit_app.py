#importing streamlit library
import mysql.connector
import streamlit as st
import pandas as pd
import tableManager as tm

import pages.country_page as cp
import pages.state_province_page as sp
import pages.park_page as pp
import pages.mountain_page as mp
import pages.lake_page as lp
import pages.trail_page as tp

is_initialized = None

def init():
    tm.create_search_table_view()

def main():
    print("reset")

    global is_initialized
    if (is_initialized != True):
        is_initialized = True
        init()
        print('initialized')

    st.title('Welcome to the National Park Database!')
    st.write('Please select a page from the sidebar to begin.')

if __name__ == '__main__':
    main()