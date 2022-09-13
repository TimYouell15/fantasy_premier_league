#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 10:05:54 2022

@author: timyouellservian
"""

import streamlit as st
import pandas as pd
from fpl_api_collection import get_league_table


base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='PL Table', page_icon=':sports-medal:', layout='centered')


st.sidebar.subheader('About')
st.sidebar.write("""This website is designed to help you analyse and
                 ultimately pick the best Fantasy Premier League Football
                 options for your team.""")
st.sidebar.write('[Github](https://github.com/TimYouell15)')

st.title('English Premier League Table')

league_df = get_league_table()

league_df.drop('id', axis=1, inplace=True)
league_df.set_index('team', inplace=True)
league_df['GF'] = league_df['GF'].astype(int)
league_df['GA'] = league_df['GA'].astype(int)
league_df['GD'] = league_df['GD'].astype(int)


st.dataframe(league_df, height=740)

