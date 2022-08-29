import streamlit as st
import altair as alt
import pandas as pd
import requests
from fpl_api_collection import (
    get_bootstrap_data
)

base_url = 'https://fantasy.premierleague.com/api/'

st.set_page_config(page_title='FPL Dashie', page_icon=':soccer:', layout='wide')
st.title('Hello and welcome to FPL Dashie!')
st.write('Please check back soon for Fantasy Premier League Football stats, graphs and predictions.')


st.sidebar.subheader('About')
st.sidebar.write("""This website is designed to help you analyse and
                 ultimately pick the best Fantasy Premier League Football
                 options for your team.""")
st.sidebar.write('[Github](https://github.com/TimYouell15)')



# st.write please enter your FPL id below
#st. text input box
# is there a way to view total number of FPL players?

def get_total_fpl_players():
    base_resp = requests.get(base_url + 'bootstrap-static/')
    return base_resp.json()['total_players']

# data = base_resp.json()


ele_data = get_bootstrap_data()['elements']

ele_df = pd.DataFrame(ele_data)
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

ele_df.sort_values('total_points', ascending=False, inplace=True)

ele_df['games_played'] = (ele_df['total_points'].astype(float)/ele_df['points_per_game'].astype(float)).round(0)
ele_df['games_played'].fillna(0, inplace=True)
ele_df['games_played'] = ele_df['games_played'].astype(int)


ele_df['now_cost'] = ele_df['now_cost']/10


ele_df['selected_by_percent'] = ele_df['selected_by_percent'].astype(float)

def display_frame(df):
    '''display dataframe with all float columns rounded to 1 decimal place'''
    float_cols = df.select_dtypes(include='float64').columns.values
    st.dataframe(df.style.format(subset=float_cols, formatter='{:.1f}'))

st.header('Season Totals')
display_frame(ele_df)


scatter_x_var = st.selectbox(
    'X axis variable',
    ['now_cost', 'minutes', 'selected_by_percent', 'games_played']
)

scatter_lookup = {'games_played': 'games_played', 'now_cost': 'now_cost', 'minutes': 'minutes', 'selected_by_percent': 'selected_by_percent'}

st.header('Points per ' + scatter_x_var)
c = alt.Chart(ele_df).mark_circle(size=75).encode(
    x=scatter_lookup[scatter_x_var],
    y='total_points',
    color='element_type',
    tooltip=['web_name', 'total_points']
)
st.altair_chart(c, use_container_width=True)


st.header('Differentials')
ele_df['point_per_selected_by'] = ele_df['total_points'].astype(float)/ele_df['selected_by_percent'].astype(float)





