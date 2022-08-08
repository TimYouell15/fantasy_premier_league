import pandas as pd
import requests


base_url = 'https://fantasy.premierleague.com/api/'

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
        print('Unable to reach bootstrap API successfully')


manager_data = get_manager_history_data(392357)
print(manager_data.head(5))