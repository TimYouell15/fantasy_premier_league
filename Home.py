import streamlit as st
import pandas as pd
import requests

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='FPL Dashie', page_icon=':soccer:', layout='wide')
st.title('Hello and welcome to FPL Dashie!')
st.write('Please check back soon for Fantasy Premier League Football stats, graphs and predictions.')


st.sidebar.subheader('About')
st.sidebar.write("""This website is designed to help you analyse and
                 ultimately pick the best Fantasy Premier League Football
                 options for your team.""")
st.sidebar.write('[Github](https://github.com/TimYouell15)')


def display_frame(df):
    '''display dataframe with all float columns rounded to 1 decimal place'''
    float_cols = df.select_dtypes(include='float64').columns.values
    st.dataframe(df.style.format(subset=float_cols, formatter='{:.1f}'))


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


# st.write please enter your FPL id below
#st. text input box
# is there a way to view total number of FPL players?

def get_total_fpl_players():
    base_resp = requests.get(base_url + 'bootstrap-static/')
    return base_resp.json()['total_players']

# data = base_resp.json()







