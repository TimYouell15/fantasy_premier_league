#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 15:57:08 2022

@author: timyouellservian
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpl_api_collection import (
    get_bootstrap_data, get_fixture_data
)

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='Fixtures', page_icon=':calendar:', layout='wide')

st.title("Premier League Fixture List")
st.write('Use the sliders to filter the fixtures down to a specific gameweek range.')

st.sidebar.subheader('About')
st.sidebar.write("""This website is designed to help you analyse and
                 ultimately pick the best Fantasy Premier League Football
                 options for your team.""")
st.sidebar.write('[GitHub](https://github.com/TimYouell15)')


def display_frame(df):
    '''display dataframe with all float columns rounded to 1 decimal place'''
    float_cols = df.select_dtypes(include='float64').columns.values
    st.dataframe(df.style.format(subset=float_cols, formatter='{:.1f}'))


fixt_df = get_fixture_data()
teams_df = pd.DataFrame(get_bootstrap_data()['teams'])

teams_list = teams_df['short_name'].unique().tolist()

# don't need to worry about double fixtures just yet!
fixt_df['team_h'] = fixt_df['team_h'].map(teams_df.set_index('id')['short_name'])
fixt_df['team_a'] = fixt_df['team_a'].map(teams_df.set_index('id')['short_name'])

gw_dict = dict(zip(range(1,381),
                   [num for num in range(1, 39) for x in range(10)]))
fixt_df['event_lock'] = fixt_df['id'].map(gw_dict)


team_fdr_data = []
team_fixt_data = []
for team in teams_list:
    home_data = fixt_df.copy().loc[fixt_df['team_h'] == team]
    away_data = fixt_df.copy().loc[fixt_df['team_a'] == team]
    home_data.loc[:, 'was_home'] = True
    away_data.loc[:, 'was_home'] = False
    merged_df = pd.concat([home_data, away_data])
    merged_df.sort_values('event_lock', inplace=True)
    merged_df.loc[(merged_df['team_h'] == team) & (merged_df['event'].notnull()), 'next'] = merged_df['team_a'] + ' (H)'
    merged_df.loc[(merged_df['team_a'] == team) & (merged_df['event'].notnull()), 'next'] = merged_df['team_h'] + ' (A)'
    merged_df.loc[merged_df['event'].isnull(), 'next'] = 'BLANK'
    merged_df.loc[(merged_df['team_h'] == team) & (merged_df['event'].notnull()), 'next_fdr'] = merged_df['team_h_difficulty']
    merged_df.loc[(merged_df['team_a'] == team) & (merged_df['event'].notnull()), 'next_fdr'] = merged_df['team_a_difficulty']
    team_fixt_data.append(pd.DataFrame([team] + list(merged_df['next'])).transpose())
    team_fdr_data.append(pd.DataFrame([team] + list(merged_df['next_fdr'])).transpose())
    
    
team_fdr_df = pd.concat(team_fdr_data).set_index(0)
team_fixt_df = pd.concat(team_fixt_data).set_index(0)

gw_min = min(fixt_df['event_lock'])
gw_max = max(fixt_df['event_lock'])


def get_annot_size(sl1, sl2):
    ft_size = sl2 - sl1
    if ft_size >= 24:
        annot_size = 2
    elif (ft_size < 24) & (ft_size >= 16):
        annot_size = 3
    elif (ft_size < 16) & (ft_size >= 12):
        annot_size = 4
    elif (ft_size < 12) & (ft_size >= 9):
        annot_size = 5
    elif (ft_size < 9) & (ft_size >= 7):
        annot_size = 6
    elif (ft_size < 7) & (ft_size >= 5):
        annot_size = 7
    else:
        annot_size = 8
    return annot_size


slider1, slider2 = st.slider('Gameweek: ', gw_min, gw_max, [gw_min, gw_max], 1)
annot_size = get_annot_size(slider1, slider2)


filtered_fixt_df = team_fdr_df.iloc[:, slider1-1: slider2]
filtered_team_df = team_fixt_df.iloc[:, slider1-1: slider2]
new_fixt_df = filtered_fixt_df.copy()
new_fixt_df.loc[:, 'fixt_ave'] = new_fixt_df.mean(axis=1)
new_fixt_df.sort_values('fixt_ave', ascending=True, inplace=True)
new_fixt_df.drop('fixt_ave', axis=1, inplace=True)
new_fixt_df = new_fixt_df.astype(float)
filtered_team_df = filtered_team_df.loc[new_fixt_df.index]

fig, ax = plt.subplots()
sns.heatmap(new_fixt_df, ax=ax, annot=filtered_team_df, fmt='', cmap='GnBu', annot_kws={'size': annot_size}, cbar_kws={'label': 'Fixture Difficulty Rating (FDR)'})
ax.set_xlabel('Gameweek')
ax.set_ylabel('Team')
st.write(fig)


def fdr_heatmap(slider1, slider2):
    filtered_fixt_df = team_fdr_df.iloc[:, slider1-1: slider2]
    new_fixt_df = filtered_fixt_df.copy()
    new_fixt_df.loc[:, 'fixt_ave'] = new_fixt_df.mean(axis=1)
    new_fixt_df.sort_values('fixt_ave', ascending=True, inplace=True)
    new_fixt_df.drop('fixt_ave', axis=1, inplace=True)
    fig, ax = plt.subplots()
    sns.heatmap(new_fixt_df, ax=ax, annot=True)
    st.write(fig)
    #return new_fixt_df
    

#test = fdr_heatmap(3, 13)


#sns.heatmap(team_fdr_df, annot=True)
