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

def get_player_id_dict():
    ele_df = pd.DataFrame(get_bootstrap_data()['elements'])
    id_dict = dict(zip(ele_df['id'], ele_df['web_name']))
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


































