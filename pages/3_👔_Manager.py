#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 11:13:09 2022

@author: timyouellservian
"""

import streamlit as st
import pandas as pd
import requests
from fpl_api_collection import (
    get_bootstrap_data, get_manager_history_data, get_manager_team_data,
    get_manager_details
)

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='Manager', page_icon=':necktie:', layout='wide')

st.sidebar.subheader('About')
st.sidebar.write("""This website is designed to help you analyse and
                 ultimately pick the best Fantasy Premier League Football
                 options for your team.""")
st.sidebar.write('[Github](https://github.com/TimYouell15)')


def display_frame(df):
    '''display dataframe with all float columns rounded to 1 decimal place'''
    float_cols = df.select_dtypes(include='float64').columns.values
    st.dataframe(df.style.format(subset=float_cols, formatter='{:.1f}'))


# st.write please enter your FPL id below
#st. text input box
# is there a way to view total number of FPL players?
def get_total_fpl_players():
    base_resp = requests.get(base_url + 'bootstrap-static/')
    return base_resp.json()['total_players']


fpl_id = st.text_input('Please enter your FPL ID:', '')


if fpl_id == '':
	st.write('')
else:
    try:
        fpl_id = int(fpl_id)
        total_players = get_total_fpl_players()
        if fpl_id == 0:
            st.write('Please enter a valid FPL ID.')
        elif fpl_id <= total_players:
            manager_data = get_manager_details(fpl_id)
            manager_name = manager_data['player_first_name'] + ' ' + manager_data['player_last_name']
            manager_team = manager_data['name']
            st.write('Displaying FPL 2022/23 Season Data for ' + manager_name + '\'s Team (' + manager_team + ')')
            man_data = get_manager_history_data(fpl_id)
            man_data.sort_values('event', ascending=False, inplace=True)
            display_frame(man_data)
        else:
            st.write('FPL ID is too high to be a valid ID. Please try again.')
            st.write('The total number of FPL players is: ' + str(total_players))
    except ValueError:
        st.write('Please enter a valid FPL ID.')


events_df = pd.DataFrame(get_bootstrap_data()['events'])
complete_df = events_df.loc[events_df['finished'] == True]

gw_complete_list = complete_df['id'].tolist()

fpl_gw = st.selectbox(
    'Team on specific Gameweek', gw_complete_list
    )


if fpl_id == '':
    st.write('')
else:
    manager_team_df = get_manager_team_data(fpl_id, fpl_gw)
    display_frame(manager_team_df)
