import streamlit as st
import pandas as pd
import requests

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='Tims First Website', page_icon=':shark:', layout='wide')
st.title('Hello and welcome to Tim\'s first website!')
st.write('Please check back soon for updates and Fantasy Premier League Football tips and stats.')

st.write('[Personal Github Page](https://github.com/TimYouell15)')

if st.button('Click me for a joke'):
	st.write('The change in weather here in Sydney has got me swapping from aerosol deodorant. Roll on next week.')
else:
	st.write('I promise it will be worth it')

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

fpl_id = st.text_input('Please enter your FPL ID:', '')

if fpl_id == '':
	st.write('')
else:
	st.write('Displaying FPL 2022/23 Season Data for FPL ID: ' + str(fpl_id))
	manager_data = get_manager_history_data(fpl_id)
	display_frame(manager_data)
