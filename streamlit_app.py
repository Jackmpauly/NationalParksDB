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



def main():
    print("reset")
    # writing simple text
    # st.text("Hello")


st.text('Hello')