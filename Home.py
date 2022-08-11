import streamlit as st
import pandas as pd
import requests
from fpl_api_collection import (
    get_bootstrap_data, get_fixture_data
)

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='FPL Dashie', page_icon=':soccer:', layout='wide')
st.title('Hello and welcome to FPL Dashie!')
st.write('Please check back soon for Fantasy Premier League Football stats, graphs and predictions.')


st.sidebar.subheader('About')
st.sidebar.write("""This website is designed to help you analyse and
                 ultimately pick the best Fantasy Premier League Football
                 options for your team.""")
st.sidebar.write('[Github](https://github.com/TimYouell15)')


def display_frame(df):
    '''display dataframe with all float columns rounded to 1 decimal place'''
    float_cols = df.select_dtypes(include='float64').columns.values
    st.dataframe(df.style.format(subset=float_cols, formatter='{:.1f}'))


fixt_df = get_fixture_data()

display_frame(fixt_df)



# st.write please enter your FPL id below
#st. text input box
# is there a way to view total number of FPL players?

def get_total_fpl_players():
    base_resp = requests.get(base_url + 'bootstrap-static/')
    return base_resp.json()['total_players']

# data = base_resp.json()







