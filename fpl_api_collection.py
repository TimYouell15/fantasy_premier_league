#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 15:26:50 2022

@author: timyouellservian
"""

import pandas as pd
from collections import ChainMap
import requests

base_url = 'https://fantasy.premierleague.com/api/'

"""
ENDPOINTS

bootstrap-static/:
    element_stats
    element_types
    elements
    events
    game_settings
    phases
    teams
    total_players

fixtures/

element-summary/<player_id>/:
    fixtures
    history
    history_past

entry/<manager_id>/
entry/<manager_id>/history/
"""

def get_bootstrap_data():
    resp = requests.get(base_url + 'bootstrap-static/')
    if resp.status_code != 200:
        raise Exception('Response was status code ' + str(resp.status_code))
    else:
        try:
         return resp.json()
        except KeyError:
            print('Unable to reach FPL bootstrap-static API endpoint.')


def get_manager_history_data(manager_id):
    manager_hist_url = base_url + 'entry/' + str(manager_id) + '/history/'
    resp = requests.get(manager_hist_url)
    if resp.status_code != 200:
        raise Exception('Response was status code ' + str(resp.status_code))
    json = resp.json()
    try:
        data = pd.DataFrame(json['current'])
        return data
    except KeyError:
        print('Unable to reach FPL entry API endpoint.')


def get_manager_team_data(m_id, gw):
    m_url = base_url + 'entry/' + str(m_id) + '/event/' + str(gw) + '/picks/'
    resp = requests.get(m_url)
    if resp.status_code != 200:
        raise Exception('Response was status code ' + str(resp.status_code))
    json = resp.json()
    try:
        data = pd.DataFrame(json['picks'])
        return data
    except KeyError:
        print('Unable to reach FPL entry API endpoint.')



def get_fixture_data():
    resp = requests.get(base_url + 'fixtures/')
    if resp.status_code != 200:
        raise Exception('Response was status code ' + str(resp.status_code))
    else:
        return pd.DataFrame(resp.json())


def get_manager_details(manager_id):
    manager_hist_url = base_url + 'entry/' + str(manager_id) + '/'
    resp = requests.get(manager_hist_url)
    if resp.status_code != 200:
        raise Exception('Response was status code ' + str(resp.status_code))
    try:
        return resp.json()
    except KeyError:
        print('Unable to reach FPL entry API endpoint.')


'''
ele_stats_data = get_bootstrap_data()['element_stats']
ele_types_data = get_bootstrap_data()['element_types']
ele_data = get_bootstrap_data()['elements']
events_data = get_bootstrap_data()['events']
game_settings_data = get_bootstrap_data()['game_settings']
phases_data = get_bootstrap_data()['phases']
teams_data = get_bootstrap_data()['teams']
total_managers = get_bootstrap_data()['total_players']


fixt = get_fixture_data()


ele_df = pd.DataFrame(ele_data)

events_df = pd.DataFrame(events_data)

#keep only required cols


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

picks_df = get_manager_team_data(9, 4)
'''

# need to do an original data pull to get historic gw_data for every player_id
# shouldn't matter if new player_id's are added via tranfsers etc because it
# should just get added to the big dataset


# get player_id list

def get_player_id_dict(web_name=True) -> dict:
    ele_df = pd.DataFrame(get_bootstrap_data()['elements'])
    teams_df = pd.DataFrame(get_bootstrap_data()['teams'])
    ele_df['team_name'] = ele_df['team'].map(teams_df.set_index('id')['short_name'])
    if web_name == True:
        id_dict = dict(zip(ele_df['id'], ele_df['web_name']))
    else:
        ele_df['full_name'] = ele_df['first_name'] + ' ' + ele_df['second_name'] + ' (' + ele_df['team_name'] + ')'
        id_dict = dict(zip(ele_df['id'], ele_df['full_name']))
    return id_dict

#player_dict = get_player_id_dict()

# cut the sample down to 10 to make it easier to work through
#player_dict_sample = {k: player_dict[k] for k in list(player_dict)[:10]}


def get_player_hist_df(player_id) -> pd.DataFrame():
    req_url = base_url + 'element-summary/' + str(player_id) + '/'
    player_data = requests.get(req_url).json()['history']
    player_df = pd.DataFrame(player_data)
    return player_df


def collate_player_hist() -> pd.DataFrame():
    player_dfs = []
    player_dict = get_player_id_dict()
    for player_id, player_name in player_dict.items():
        print('Getting GW historic data for ' + player_name)
        success = False
        while not success:
            try:
                player_df = get_player_hist_df(player_id)
                player_dfs.append(player_df)
                success = True
            except:
                print('error getting ' + player_name + ' data')
    hist_df = pd.concat(player_dfs)
    return hist_df

#hist_df = pd.concat(player_dfs)

# Team, games_played, wins, losses, draws, goals_for, goals_against, GD, PTS, Form? [W,W,L,D,W]
def get_league_table():
    fixt_df = get_fixture_data()
    teams_df = pd.DataFrame(get_bootstrap_data()['teams'])
    teams_id_list = teams_df['id'].unique().tolist()
    df_list = []
    for t_id in teams_id_list:
        # count times team_id appears in fin_df
        home_data = fixt_df.copy().loc[fixt_df['team_h'] == t_id]
        away_data = fixt_df.copy().loc[fixt_df['team_a'] == t_id]
        home_data.loc[:, 'was_home'] = True
        away_data.loc[:, 'was_home'] = False
        merged_df = pd.concat([home_data, away_data])
        merged_df = merged_df.loc[merged_df['finished']==True]
        merged_df.sort_values('event', inplace=True)
        merged_df.loc[(merged_df['was_home'] == True) & (merged_df['team_h_score'] > merged_df['team_a_score']), 'win'] = True
        merged_df.loc[(merged_df['was_home'] == False) & (merged_df['team_a_score'] > merged_df['team_h_score']), 'win'] = True
        merged_df.loc[(merged_df['team_h_score'] == merged_df['team_a_score']), 'draw'] = True
        merged_df.loc[(merged_df['was_home'] == True) & (merged_df['team_h_score'] < merged_df['team_a_score']), 'loss'] = True
        merged_df.loc[(merged_df['was_home'] == False) & (merged_df['team_a_score'] < merged_df['team_h_score']), 'loss'] = True
        merged_df.loc[(merged_df['was_home'] == True), 'gf'] = merged_df['team_h_score']
        merged_df.loc[(merged_df['was_home'] == False), 'gf'] = merged_df['team_a_score']
        merged_df.loc[(merged_df['was_home'] == True), 'ga'] = merged_df['team_a_score']
        merged_df.loc[(merged_df['was_home'] == False), 'ga'] = merged_df['team_h_score']
        merged_df.loc[(merged_df['win'] == True), 'result'] = 'W'
        merged_df.loc[(merged_df['draw'] == True), 'result'] = 'D'
        merged_df.loc[(merged_df['loss'] == True), 'result'] = 'L'
        merged_df.loc[(merged_df['was_home'] == True) & (merged_df['team_a_score'] == 0), 'clean_sheet'] = True
        merged_df.loc[(merged_df['was_home'] == False) & (merged_df['team_h_score'] == 0), 'clean_sheet'] = True
        ws = len(merged_df.loc[merged_df['win'] == True])
        ds = len(merged_df.loc[merged_df['draw'] == True])
        l_data = {'id': [t_id], 'GP': [len(merged_df)], 'W': [ws], 'D': [ds],
                  'L': [len(merged_df.loc[merged_df['loss'] == True])],
                  'GF': [merged_df['gf'].sum()], 'GA': [merged_df['ga'].sum()],
                  'GD': [merged_df['gf'].sum() - merged_df['ga'].sum()],
                  'CS': [merged_df['clean_sheet'].sum()], 'Pts': [(ws*3) + ds],
                  'Form': [merged_df['result'].tail(5).str.cat(sep='')]}
        df_list.append(pd.DataFrame(l_data))
    league_df = pd.concat(df_list)
    league_df.sort_values(['Pts', 'GD'], ascending=False, inplace=True)
    league_df['team'] = league_df['id'].map(teams_df.set_index('id')['short_name'])
    return league_df


def get_current_gw():
    events_df = pd.DataFrame(get_bootstrap_data()['events'])
    current_gw = events_df.loc[events_df['is_next'] == True].reset_index()['id'][0]
    return current_gw


def get_fixture_dfs():
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
        h_filt = (merged_df['team_h'] == team) & (merged_df['event'].notnull())
        a_filt = (merged_df['team_a'] == team) & (merged_df['event'].notnull())
        merged_df.loc[h_filt, 'next'] = merged_df['team_a'] + ' (H)'
        merged_df.loc[a_filt, 'next'] = merged_df['team_h'] + ' (A)'
        merged_df.loc[merged_df['event'].isnull(), 'next'] = 'BLANK'
        merged_df.loc[h_filt, 'next_fdr'] = merged_df['team_h_difficulty']
        merged_df.loc[a_filt, 'next_fdr'] = merged_df['team_a_difficulty']
        team_fixt_data.append(pd.DataFrame([team] + list(merged_df['next'])).transpose())
        team_fdr_data.append(pd.DataFrame([team] + list(merged_df['next_fdr'])).transpose())
    team_fdr_df = pd.concat(team_fdr_data).set_index(0)
    team_fixt_df = pd.concat(team_fixt_data).set_index(0)
    return team_fdr_df, team_fixt_df























