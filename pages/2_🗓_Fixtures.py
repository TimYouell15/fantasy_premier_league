#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 15:57:08 2022

@author: timyouellservian
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
from fpl_api_collection import (
    get_bootstrap_data, get_fixture_data
)

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='Fixtures', page_icon=':calendar:', layout='wide')


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
teams_df = pd.DataFrame(get_bootstrap_data()['teams'])

teams_list = teams_df['short_name'].unique().tolist()

fixt_df['home_team_name'] = fixt_df['team_h'] \
        .map(teams_df.set_index('id')['short_name'])
fixt_df['away_team_name'] = fixt_df['team_a'] \
        .map(teams_df.set_index('id')['short_name'])

fdr_cols = ['event', 'home_team_name', 'team_h_difficulty', 'away_team_name', 'team_a_difficulty']


gw_dict = dict(zip(np.arange(1, 381),
                   [num for num in np.arange(1, 39) for x in range(10)]))
gw_cols = ['GW' + str(num) for num in fixt_df['event'].unique().tolist()]
fixt_df.loc[fixt_df['event'].isnull(), 'event2'] = fixt_df['id'].map(gw_dict)
fixt_df['event2'].fillna(fixt_df['event'], inplace=True)
fixt_df.loc[fixt_df['event'].isnull(), 'blank'] = True
fixt_df['blank'].fillna(False, inplace=True)
fixt_df.sort_values('event2', ascending=True, inplace=True)
fixt_df['home_team_name'] = fixt_df['team_h'] \
    .map(teams_df.set_index('id')['short_name'])
fixt_df['away_team_name'] = fixt_df['team_a'] \
    .map(teams_df.set_index('id')['short_name'])
fixt_df.sort_values(['event2', 'kickoff_time'], ascending=True, inplace=True)
gw_array = np.arange(min_gw, max_gw+1)
ind_array = np.arange(min_gw-1, max_gw)
for team in teams_list:
    if team == teams_list[0]:
        first_df = fixt_df.copy()
        first_df = first_df.loc[(first_df['home_team_name'] == team) |
                                (first_df['away_team_name'] == team)]
        first_df.loc[:, 'team_name_a'] = first_df['away_team_name'] + ' (H)'
        first_df.loc[:, 'team_name_h'] = first_df['home_team_name'] + ' (A)'
        first_df['team_name_h'].replace(team + ' (H)', np.nan, inplace=True)
        first_df['team_name_a'].replace(team + ' (A)', np.nan, inplace=True)
                
        first_df['away_team_name'] = first_df['away_team_name'] + ' (H)'
        first_df['home_team_name'] = first_df['home_team_name'] + ' (A)'
        first_df['away_team_name'].replace(team + ' (H)', np.nan,
                                           inplace=True)
        first_df['home_team_name'].replace(team + ' (A)', np.nan,
                                           inplace=True)
        first_df['next5'] = first_df['home_team_name'].fillna(
            first_df['away_team_name'])
        first_df.loc[first_df['blank'] == True, 'next5'] = 'BLANK'
        first_df['fdr'] = first_df['next5'].str[:3].map(teams_df.set_index(
            'short_name')['strength'])
        dup_df = first_df.duplicated(subset=['event2'],
                                     keep=False).reset_index()
        dup_df.columns = ['index', 'multiple']
        first_df = first_df.reset_index().merge(dup_df, on='index',
                                                how='left')
        first_df = first_df[~((first_df['multiple'] == True) &
                              (first_df['blank'] == True))]
        first_df['next5_new'] = first_df.groupby(['event'])['next5'] \
            .transform(lambda x : ' + '.join(x))
        fdr_gw_aves = first_df[['event2', 'fdr']].groupby(
            'event2').mean().reset_index()
        fdr_gw_aves.columns = ['event2', 'fdr_gw_ave']
        first_df.drop_duplicates('event2', keep='first', inplace=True)
        first_df = first_df.merge(fdr_gw_aves, on='event2', how='left')
        sorted_df = pd.DataFrame(data={'event2': np.arange(min_gw, max_gw+1)})
        sorted_df = sorted_df.merge(first_df, on='event2', how='left')
        sorted_df['next5_new'].fillna('BLANK', inplace=True)
        gw_cols = ['GW' + str(num) for num in gw_array]
        fixt_next = [sorted_df['next5_new'][num] for num in ind_array]
        gw_fdr_cols = ['GW' + str(num) + '_fdr' for num in gw_array]
        fixt_fdr_next = [sorted_df['fdr_gw_ave'][num] for num in ind_array]
        cols = ['short_name'] + gw_cols + gw_fdr_cols
        fixt_data = [team] + fixt_next + fixt_fdr_next
        new_df = pd.DataFrame([fixt_data], columns=cols)
    else:
        rest_df = fixt_df.copy()
        rest_df = rest_df.loc[(rest_df['home_team_name'] == team) |
                                (rest_df['away_team_name'] == team)]
        rest_df.loc[:, 'team_name_a'] = rest_df['away_team_name'] + ' (H)'
        rest_df.loc[:, 'team_name_h'] = rest_df['home_team_name'] + ' (A)'
        rest_df['team_name_h'].replace(team + ' (H)', np.nan, inplace=True)
        rest_df['team_name_a'].replace(team + ' (A)', np.nan, inplace=True)
                
        rest_df['away_team_name'] = rest_df['away_team_name'] + ' (H)'
        rest_df['home_team_name'] = rest_df['home_team_name'] + ' (A)'
        rest_df['away_team_name'].replace(team + ' (H)', np.nan,
                                           inplace=True)
        rest_df['home_team_name'].replace(team + ' (A)', np.nan,
                                           inplace=True)
        rest_df['next5'] = rest_df['home_team_name'].fillna(
            rest_df['away_team_name'])
        rest_df.loc[rest_df['blank'] == True, 'next5'] = 'BLANK'
        rest_df['fdr'] = rest_df['next5'].str[:3].map(teams_df.set_index(
            'short_name')['strength'])
        dup_df = rest_df.duplicated(subset=['event2'],
                                     keep=False).reset_index()
        dup_df.columns = ['index', 'multiple']
        rest_df = rest_df.reset_index().merge(dup_df, on='index',
                                                how='left')
        rest_df = rest_df[~((rest_df['multiple'] == True) &
                              (rest_df['blank'] == True))]
        rest_df['next5_new'] = rest_df.groupby(['event'])['next5'] \
            .transform(lambda x : ' + '.join(x))
        fdr_gw_aves = rest_df[['event2', 'fdr']].groupby(
            'event2').mean().reset_index()
        fdr_gw_aves.columns = ['event2', 'fdr_gw_ave']
        rest_df.drop_duplicates('event2', keep='first', inplace=True)
        rest_df = rest_df.merge(fdr_gw_aves, on='event2', how='left')
        sorted_df2 = pd.DataFrame(data={'event2': np.arange(min_gw, max_gw+1)})
        sorted_df2 = sorted_df2.merge(rest_df, on='event2', how='left')
        sorted_df2['next5_new'].fillna('BLANK', inplace=True)
        gw_cols = ['GW' + str(num) for num in gw_array]
        fixt_next = [sorted_df['next5_new'][num] for num in ind_array]
        gw_fdr_cols = ['GW' + str(num) + '_fdr' for num in gw_array]
        fixt_fdr_next = [sorted_df['fdr_gw_ave'][num] for num in ind_array]
        cols = ['short_name'] + gw_cols + gw_fdr_cols
        fixt_data = [team] + fixt_next + fixt_fdr_next
        two_df = pd.DataFrame([fixt_data], columns=cols)
        new_df = new_df.append(two_df, ignore_index=True)
        
#need to fix the above
        
        





fdr_df = pd.DataFrame({'team': teams_list}, columns=['team'] + gw_cols)



fixture_list = 

fdr_df.append(fixture_list)

fixt_df = fixt_df.loc[(fixt_df['event2'] >= min_gw) &
                      (fixt_df['event2'] <= max_gw)]




def get_new_df_from_sorted(min_gw, sorted_df, team, max_gw):
    gw_array = np.arange(min_gw, max_gw+1)
    gw_cols = ['GW' + str(min_gw) for num in gw_array]
    fixt_next = [sorted_df['next5_new'][num] for num in gw_array]
    gw_fdr_cols = ['GW' + str(min_gw) + '_fdr' for num in gw_array]
    fixt_fdr_next = [sorted_df['fdr_gw_ave'][num] for num in gw_array]
    cols = ['short_name'] + gw_cols + gw_fdr_cols
    fixt_data = [team] + fixt_next + fixt_fdr_next
    new_df = pd.DataFrame([fixt_data], columns=cols)
    return new_df


def get_upcoming_fixtures(min_gw, max_gw):
    fixt_df = get_fixture_data()
    gw_dict = dict(zip(np.arange(1, 381),
                       [num for num in np.arange(1, 39) for x in range(10)]))
    fixt_df.loc[fixt_df['event'].isnull(), 'event2'] = fixt_df['id'].map(gw_dict)
    fixt_df['event2'].fillna(fixt_df['event'], inplace=True)
    fixt_df.loc[fixt_df['event'].isnull(), 'blank'] = True
    fixt_df['blank'].fillna(False, inplace=True)
    fixt_df.sort_values('event2', ascending=True, inplace=True)
    teams_df = pd.DataFrame(get_bootstrap_data()['teams'])
    team_list = teams_df['short_name'].unique().tolist()
    
    fixt_df = fixt_df.loc[(fixt_df['event2'] >= min_gw) &
                          (fixt_df['event2'] <= max_gw)]
    fixt_df['home_team_name'] = fixt_df['team_h'] \
        .map(teams_df.set_index('id')['short_name'])
    fixt_df['away_team_name'] = fixt_df['team_a'] \
        .map(teams_df.set_index('id')['short_name'])
    for team in team_list:
        if team == team_list[0]:
            first_df = fixt_df[(fixt_df['home_team_name'] == team) |
                               (fixt_df['away_team_name'] == team)]
            first_df.sort_values(['event2', 'kickoff_time'],
                                 ascending=True, inplace=True)
            first_df['away_team_name'] = first_df['away_team_name'] + ' (H)'
            first_df['home_team_name'] = first_df['home_team_name'] + ' (A)'
            first_df['away_team_name'].replace(team + ' (H)', np.nan,
                                               inplace=True)
            first_df['home_team_name'].replace(team + ' (A)', np.nan,
                                               inplace=True)
            first_df['next5'] = first_df['home_team_name'].fillna(
                first_df['away_team_name'])
            first_df.loc[first_df['blank'] == True, 'next5'] = 'BLANK'
            first_df['fdr'] = first_df['next5'].str[:3].map(teams_df.set_index(
                'short_name')['strength'])
            dup_df = first_df.duplicated(subset=['event'],
                                         keep=False).reset_index()
            dup_df.columns = ['index', 'multiple']
            first_df = first_df.reset_index().merge(dup_df, on='index',
                                                    how='left')
            first_df = first_df[~((first_df['multiple'] == True) &
                                  (first_df['blank'] == True))]
            first_df['next5_new'] = first_df.groupby(['event'])['next5'] \
                .transform(lambda x : ' + '.join(x))
            fdr_gw_aves = first_df[['event', 'fdr']].groupby(
                'event').mean().reset_index()
            fdr_gw_aves.columns = ['event', 'fdr_gw_ave']
            first_df.drop_duplicates('event', keep='first', inplace=True)
            first_df = first_df.merge(fdr_gw_aves, on='event', how='left')
            sorted_df = pd.DataFrame(data={'event': np.arange(min_gw, max_gw)})
            sorted_df = sorted_df.merge(first_df, on='event', how='left')
            sorted_df['next5_new'].fillna('BLANK', inplace=True)
            new_df = get_new_df_from_sorted(min_gw, sorted_df, team, max_gw)
        else:
            rest_df = fixt_df[(fixt_df['home_team_name'] == team) |
                              (fixt_df['away_team_name'] == team)]
            rest_df.sort_values(['event2', 'kickoff_time'],
                                ascending=True, inplace=True)
            rest_df['away_team_name'] = rest_df['away_team_name'] + ' (H)'
            rest_df['home_team_name'] = rest_df['home_team_name'] + ' (A)'
            rest_df['away_team_name'].replace(team + ' (H)', np.nan,
                                              inplace=True)
            rest_df['home_team_name'].replace(team + ' (A)', np.nan,
                                              inplace=True)
            rest_df['next5'] = rest_df['home_team_name'].fillna(
                rest_df['away_team_name'])
            rest_df.loc[rest_df['blank'] == True, 'next5'] = 'BLANK'
            rest_df['fdr'] = rest_df['next5'].str[:3].map(teams_df.set_index(
                'short_name')['strength'])
            dup_df = rest_df.duplicated(subset=['event2'],
                                        keep=False).reset_index()
            dup_df.columns = ['index', 'multiple']
            rest_df = rest_df.reset_index().merge(dup_df, on='index',
                                                  how='left')
            rest_df = rest_df[~((rest_df['multiple'] == True) &
                                (rest_df['blank'] == True))]
            rest_df['next5_new'] = rest_df.groupby(['event2'])['next5'] \
                .transform(lambda x : ' + '.join(x))
            rest_fdr_gw_aves = rest_df[['event2', 'fdr']].groupby(
                'event2').mean().reset_index()
            rest_fdr_gw_aves.columns = ['event2', 'fdr_gw_ave']
            rest_df.drop_duplicates('event2', keep='first', inplace=True)
            rest_df = rest_df.merge(rest_fdr_gw_aves, on='event2', how='left')
            sorted_df2 = pd.DataFrame(
                data={'event': np.arange(min_gw, max_gw)})
            sorted_df2 = sorted_df2.merge(rest_df, on='event', how='left')
            sorted_df2['next5_new'].fillna('BLANK', inplace=True)
            two_df = get_new_df_from_sorted(min_gw, sorted_df2, team, max_gw)
            new_df = new_df.append(two_df, ignore_index=True)
            fdr_list = ['GW' + str(num) + '_fdr' for num in np.arange(
                min_gw, max_gw)]
            new_df['next5_fdr_ave'] = new_df[fdr_list].mean(axis=1)
            new_df.sort_values('next5_fdr_ave', ascending=True, inplace=True)
    return new_df




sorted_fixt_df = get_upcoming_fixtures(1, 38)



fixt_df = fixt_df[fdr_cols]



min_gw = min(fixt_df['event'])
max_gw = max(fixt_df['event'])



gw_min = min(fixt_df['event'])
gw_max = max(fixt_df['event'])

slider1, slider2 = st.slider('Gameweek: ', gw_min, gw_max, [gw_min, gw_max], 1)
filtered_fixt_df = fixt_df.loc[(fixt_df['event'] >= slider1) & (fixt_df['event'] <= slider2)]

# filtered_fixt_df = fixt_df.iloc[slider1:slider2].reset_index(drop=True)
display_frame(filtered_fixt_df)