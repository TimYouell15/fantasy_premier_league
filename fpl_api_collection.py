#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 15:26:50 2022

@author: timyouellservian
"""

import pandas as pd
import requests


base_url = 'https://fantasy.premierleague.com/api/'

def get_bootstrap_data(dtype):
    resp = requests.get(base_url + 'bootstrap-static/')
    if resp.status_code != 200:
        raise Exception('Response was status code ' + str(resp.status_code))
    else:
        data = resp.json()
        try:
            boots_data = pd.DataFrame(data[dtype])
            return boots_data
        except KeyError:
            print('Unable to reach FPL bootstrap-static API endpoint.')


def get_total_managers():
    resp = requests.get(base_url + 'bootstrap-static/')
    if resp.status_code != 200:
        raise Exception('Response was status code ' + str(resp.status_code))
    else:
        data = resp.json()
        try:
            return data['total_players']
        except KeyError:
            print('Unable to reach FPL bootstrap-static API endpoint.')


ele_stats_data = get_bootstrap_data('element_stats')
ele_types_data = get_bootstrap_data('element_types')
ele_data = get_bootstrap_data('elements')
events_data = get_bootstrap_data('events')
game_settings_data = get_bootstrap_data('game_settings')
phases_data = get_bootstrap_data('phases')
teams_data = get_bootstrap_data('teams')

total_players = get_total_managers()




resp = requests.get(base_url + 'bootstrap-static/')

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




fixt_resp = requests.get(base_url + 'fixtures/')
fixt_data = fixt_resp.json()

player_resp = requests.get(base_url + 'element-summary/5/')
player_data = player_resp.json()

def get_bootstrap_data(data_type):
    resp = requests.get(base_url + 'bootstrap-static/')
    if resp.status_code != 200:
        raise Exception('Response was status code ' + str(resp.status_code))
    data = resp.json()
    try:
        elements_data = pd.DataFrame(data[data_type])
        return elements_data
    except KeyError:
        print('Unable to reach bootstrap API successfully')


