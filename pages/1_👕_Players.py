#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 11:13:09 2022

@author: timyouellservian
"""

import streamlit as st
import pandas as pd
from fpl_api_collection import (
    get_player_id_dict, get_bootstrap_data, get_player_hist_df,
    get_league_table
)
import plotly.graph_objects as go

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='Player Stats', page_icon=':shirt:', layout='wide')

# 2 drop-down menus choosing 2 players
full_player_dict = get_player_id_dict(web_name=False)


st.sidebar.subheader('About')
st.sidebar.write("""This website is designed to help you analyse and
                 ultimately pick the best Fantasy Premier League Football
                 options for your team.""")
st.sidebar.write('[GitHub](https://github.com/TimYouell15)')


ele_types_data = get_bootstrap_data()['element_types']
ele_types_df = pd.DataFrame(ele_types_data)

teams_data = get_bootstrap_data()['teams']
teams_df = pd.DataFrame(teams_data)

ele_data = get_bootstrap_data()['elements']
ele_df = pd.DataFrame(ele_data)

ele_df['element_type'] = ele_df['element_type'].map(ele_types_df.set_index('id')['singular_name_short'])


ele_cols = ['id', 'web_name', 'chance_of_playing_this_round', 'element_type',
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

# df_cut = ele_df.loc[ele_df['minutes'] >= 90]
# pivot=ele_df.pivot_table(index='element_type', values='total_points', aggfunc=np.mean).reset_index()
# pp_position = pivot.sort_values('total_points',ascending=False)



# comparison of players via spider web method?
# - chances per 90
# - assists per 90
# - goals per 90
# - xA per 90
# - xG per 90
# - crosses per 90
# - shots per 90

# # comparison of keepers - automatically switch to keeper stats
# - saves per 90
# - bps per 90
# - etc

st.title("Players")
st.write("Currently only looking at data available through the FPL API. FBRef and Understat data being added is on the To-Do list.")

# get player id from player name
# player1_id = ...


def collate_hist_df_from_name(player_name):
    p_id = [k for k, v in full_player_dict.items() if v == player_name]
    p_df = get_player_hist_df(str(p_id[0]))
    p_df.loc[p_df['was_home'] == True, 'result'] = p_df['team_h_score']\
        .astype(str) + '-' + p_df['team_a_score'].astype(str)
    p_df.loc[p_df['was_home'] == False, 'result'] = p_df['team_a_score']\
            .astype(str) + '-' + p_df['team_h_score'].astype(str)
    col_rn_dict = {'round': 'GW', 'opponent_team': 'vs',
                   'total_points': 'Pts', 'minutes': 'Mins',
                   'goals_scored': 'GS', 'assists': 'A', 'clean_sheets': 'CS',
                   'goals_conceded': 'GC', 'own_goals': 'OG',
                   'penalties_saved': 'Pen_Save',
                   'penalties_missed': 'Pen_Miss', 'yellow_cards': 'YC',
                   'red_cards': 'RC', 'saves': 'S', 'bonus': 'B',
                   'bps': 'BPS', 'influence': 'I', 'creativity': 'C',
                   'threat': 'T', 'ict_index': 'ICT', 'value': '£',
                   'selected': 'SB', 'transfers_in': 'Tran_In',
                   'transfers_out': 'Tran_Out'}
    p_df.rename(columns=col_rn_dict, inplace=True)
    col_order = ['GW', 'vs', 'result', 'Pts', 'Mins', 'GS', 'A', 'Pen_Miss',
                 'CS', 'GC', 'OG', 'Pen_Save', 'S', 'YC', 'RC', 'B', 'BPS',
                 '£', 'I', 'C', 'T', 'ICT', 'SB', 'Tran_In', 'Tran_Out']
    p_df = p_df[col_order]
    # map opponent teams
    p_df['vs'] = p_df['vs'].map(teams_df.set_index('id')['short_name'])
    p_df.set_index('GW', inplace=True)
    return p_df


def collate_total_df_from_name(player_name):
    p_id = [k for k, v in full_player_dict.items() if v == player_name]
    df = ele_df.copy()
    p_total_df = df.loc[df['id'] == p_id[0]]
    # index = web_name
    col_rn_dict = {'form': 'Form', 'points_per_game': 'PPG',
                   'total_points': 'Pts', 'minutes': 'Mins',
                   'goals_scored': 'GS', 'clean_sheets': 'CS',
                   'goals_conceded': 'GC', 'own_goals': 'OG', 'assists': 'A',
                   'penalties_saved': 'Pen_Save', 'now_cost': '£',
                   'penalties_missed': 'Pen_Miss', 'yellow_cards': 'YC',
                   'red_cards': 'RC', 'saves': 'S', 'bonus': 'B', 'bps': 'BPS',
                   'selected_by_percent': 'TSB%', 'influence': 'I',
                   'creativity': 'C', 'threat': 'T', 'ict_index': 'ICT'}
    p_t = p_total_df.rename(columns=col_rn_dict)
    col_order = ['web_name', 'team', 'Form', 'PPG', 'Pts', 'Mins', 'GS', 'A',
                 'Pen_Miss', 'CS', 'GC', 'OG', 'Pen_Save', 'S', 'YC', 'RC',
                 'B', 'BPS', 'I', 'C', 'T', 'ICT', '£', 'TSB%', 'element_type']
    p_t = p_t[col_order]
    p_t.set_index('web_name', inplace=True)
    return p_t


def collated_spider_df_from_name(player_name):
    sp_df = collate_total_df_from_name(player_name)
    league_df = get_league_table()
    sp_df['gp'] = sp_df['team'].map(league_df.set_index('id')['GP'])
    sp_df['90s'] = sp_df['Mins']/90
    sp_df['G/90'] = sp_df['GS']/sp_df['90s']
    sp_df['A/90'] = sp_df['A']/sp_df['90s']
    sp_df['BPS/90'] = sp_df['BPS']/sp_df['90s']
    sp_df['Ave_Mins'] = sp_df['Mins']/sp_df['gp']
    sp_df['Influence/90'] = sp_df['I'].astype(float)/sp_df['90s']
    sp_df['Creativity/90'] = sp_df['C'].astype(float)/sp_df['90s']
    sp_df['Threat/90'] = sp_df['T'].astype(float)/sp_df['90s']
    sp_df['ICT/90'] = sp_df['ICT'].astype(float)/sp_df['90s']
    sp_df['CS/90'] = sp_df['CS']/sp_df['90s']
    sp_df['GC/90'] = sp_df['GC']/sp_df['90s']
    sp_df['YC/90'] = sp_df['YC']/sp_df['90s']
    sp_df['B/90'] = sp_df['B']/sp_df['90s']
    sp_df['S/90'] = sp_df['S']/sp_df['90s']
    return sp_df


def display_frame(df):
    '''display dataframe with all float columns rounded to 1 decimal place'''
    float_cols = df.select_dtypes(include='float64').columns.values
    st.dataframe(df.style.format(subset=float_cols, formatter='{:.1f}'))


def get_ICT_spider_plot(player_name1, player_name2):
    cats = ['BPS/90', 'Ave_Mins', 'Influence/90', 'Creativity/90', 'Threat/90',
            'ICT/90']
    sp1_df = collated_spider_df_from_name(player_name1)
    sp1_df['player_name'] = player_name1
    sp1_df.set_index('player_name', inplace=True)
    sp1_df = sp1_df[cats].transpose().reset_index()
    
    sp2_df = collated_spider_df_from_name(player_name2)
    sp2_df['player_name'] = player_name2
    sp2_df.set_index('player_name', inplace=True)
    sp2_df = sp2_df[cats].transpose().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(name=player_name1, r=list(sp1_df[player_name1]), theta=list(sp1_df['index'])))
    fig.add_trace(go.Scatterpolar(name=player_name2, r=list(sp2_df[player_name2]), theta=list(sp2_df['index'])))
    fig.update_layout(legend=dict(x=0.33, y=1.25))
    return fig


def get_stats_spider_plot(player_name1, player_name2):
    cats = ['G/90', 'A/90', 'CS/90', 'GC/90', 'YC/90', 'B/90', 'S/90']
    sp1_df = collated_spider_df_from_name(player_name1)
    sp1_df['player_name'] = player_name1
    sp1_df.set_index('player_name', inplace=True)
    sp1_df = sp1_df[cats].transpose().reset_index()
    
    sp2_df = collated_spider_df_from_name(player_name2)
    sp2_df['player_name'] = player_name2
    sp2_df.set_index('player_name', inplace=True)
    sp2_df = sp2_df[cats].transpose().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(name=player_name1, r=list(sp1_df[player_name1]), theta=list(sp1_df['index'])))
    fig.add_trace(go.Scatterpolar(name=player_name2, r=list(sp2_df[player_name2]), theta=list(sp2_df['index'])))
    fig.update_layout(legend=dict(x=0.33, y=1.25))
    return fig


rows = st.columns(2)

player1 = rows[0].selectbox("Choose Player One", full_player_dict.values(), index=5)
player1_df = collate_hist_df_from_name(player1)
player1_total_df = collate_total_df_from_name(player1)
player1_total_df.drop('team', axis=1, inplace=True)
rows[0].dataframe(player1_df)
rows[0].dataframe(player1_total_df)


player2 = rows[1].selectbox("Choose Player Two", full_player_dict.values(), index=17)
player2_df = collate_hist_df_from_name(player2)
player2_total_df = collate_total_df_from_name(player2)
player2_total_df.drop('team', axis=1, inplace=True)
rows[1].dataframe(player2_df)
rows[1].dataframe(player2_total_df)


rows[0].plotly_chart(get_ICT_spider_plot(player1, player2))
rows[1].plotly_chart(get_stats_spider_plot(player1, player2))
#st.plotly_chart(get_spider_plot(player1, player2), use_container_width=True)





