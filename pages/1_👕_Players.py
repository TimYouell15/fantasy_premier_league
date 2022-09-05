#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 11:13:09 2022

@author: timyouellservian
"""

import streamlit as st
import pandas as pd
import numpy as np
from fpl_api_collection import get_player_id_dict, get_bootstrap_data

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='Player Stats', page_icon=':shirt:', layout='wide')

# 2 drop-down menus choosing 2 players
full_player_dict = get_player_id_dict(web_name=False)

player1 = st.sidebar.selectbox("Choose Player One", full_player_dict.values())

player2 = st.sidebar.selectbox("Choose Player Two", full_player_dict.values())

st.sidebar.subheader('About')
st.sidebar.write("""This website is designed to help you analyse and
                 ultimately pick the best Fantasy Premier League Football
                 options for your team.""")
st.sidebar.write('[Github](https://github.com/TimYouell15)')




ele_types_data = get_bootstrap_data()['element_types']
ele_types_df = pd.DataFrame(ele_types_data)

ele_data = get_bootstrap_data()['elements']
ele_df = pd.DataFrame(ele_data)

ele_df['element_type'] = ele_df['element_type'].map(ele_types_df.set_index('id')['singular_name_short'])


ele_cols = ['web_name', 'chance_of_playing_this_round', 'element_type',
            'event_points', 'form', 'now_cost', 'points_per_game',
            'selected_by_percent', 'team', 'total_points',
            'transfers_in_event', 'transfers_out_event', 'value_form',
            'value_season', 'minutes', 'goals_scored', 'assists',
            'clean_sheets', 'goals_conceded', 'own_goals', 'penalties_saved',
            'penalties_missed', 'yellow_cards', 'red_cards', 'saves', 'bonus',
            'bps', 'influence', 'creativity', 'threat', 'ict_index',
            'influence_rank', 'influence_rank_type', 'creativity_rank',
            'creativity_rank_type', 'threat_rank', 'threat_rank_type',
            'ict_index_rank', 'ict_index_rank_type', 'dreamteam_count']

ele_df = ele_df[ele_cols]

df_cut = ele_df.loc[ele_df['minutes'] >= 90]

pivot=ele_df.pivot_table(index='element_type', values='total_points', aggfunc=np.mean).reset_index()
pp_position = pivot.sort_values('total_points',ascending=False)




'''
# comparison of players via spider web method?
- chances per 90
- assists per 90
- goals per 90
- xA per 90
- xG per 90
- crosses per 90
- shots per 90

# comparison of keepers - automatically switch to keeper stats
- saves per 90
- bps per 90
- etc
'''

