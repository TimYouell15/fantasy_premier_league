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
st.sidebar.write('[GitHub](https://github.com/TimYouell15)')



# st.write please enter your FPL id below
#st. text input box
# is there a way to view total number of FPL players?

def get_total_fpl_players():
    base_resp = requests.get(base_url + 'bootstrap-static/')
    return base_resp.json()['total_players']


def display_frame(df):
    '''display dataframe with all float columns rounded to 1 decimal place'''
    float_cols = df.select_dtypes(include='float64').columns.values
    st.dataframe(df.style.format(subset=float_cols, formatter='{:.1f}'))


ele_types_data = get_bootstrap_data()['element_types']
ele_types_df = pd.DataFrame(ele_types_data)

teams_data = get_bootstrap_data()['teams']
teams_df = pd.DataFrame(teams_data)

ele_data = get_bootstrap_data()['elements']
ele_df = pd.DataFrame(ele_data)

ele_df['element_type'] = ele_df['element_type'].map(ele_types_df.set_index('id')['singular_name_short'])
ele_df['team'] = ele_df['team'].map(teams_df.set_index('id')['short_name'])

rn_cols = {'web_name': 'Name', 'team': 'Team', 'element_type': 'Pos', 
           'event_points': 'GW_Pts', 'total_points': 'Pts', 'now_cost': '£',
           'selected_by_percent': 'TSB%', 'minutes': 'Mins',
           'goals_scored': 'GS', 'assists': 'A',
           'penalties_missed': 'Pen_Miss', 'clean_sheets': 'CS',
           'goals_conceded': 'GC', 'own_goals': 'OG',
           'penalties_saved': 'Pen_Save', 'saves': 'S',
           'yellow_cards': 'YC', 'red_cards': 'RC', 'bonus': 'B', 'bps': 'BPS',
           'value_form': 'Value', 'points_per_game': 'PPG', 'influence': 'I',
           'creativity': 'C', 'threat': 'T', 'ict_index': 'ICT',
           'influence_rank': 'I_Rank', 'creativity_rank': 'C_Rank',
           'threat_rank': 'T_Rank', 'ict_index_rank': 'ICT_Rank',
           'tranfers_in_event': 'T_In', 'transfers_out_event': 'T_Out'}
ele_df.rename(columns=rn_cols, inplace=True)


ele_df.sort_values('Pts', ascending=False, inplace=True)

ele_df['GP'] = (ele_df['Pts'].astype(float)/ele_df['PPG'].astype(float)).round(0)
ele_df['GP'].fillna(0, inplace=True)
ele_df['GP'] = ele_df['GP'].astype(int)


ele_df['£'] = ele_df['£']/10


ele_df['TSB%'] = ele_df['TSB%'].astype(float)

st.header('Season Totals')

ele_cols = ['Name', 'Team', 'Pos', 'GW_Pts', 'Pts', '£', 'TSB%', 'GP', 'Mins',
            'GS', 'A', 'Pen_Miss', 'CS', 'GC', 'OG', 'Pen_Save', 'S', 'YC',
            'RC', 'B', 'BPS', 'Value', 'PPG', 'I', 'C', 'T', 'ICT', 'I_Rank',
            'C_Rank', 'T_Rank', 'ICT_Rank']

ele_df = ele_df[ele_cols]

indexed_ele_df = ele_df.set_index('Name')

display_frame(indexed_ele_df)


scatter_x_var = st.selectbox(
    'X axis variable',
    ['£', 'Mins', 'TSB%', 'GP']
)

scatter_lookup = {'GP': 'GP', '£': '£', 'Mins': 'Mins', 'TSB%': 'TSB%'}

st.header('Points per ' + scatter_x_var)
c = alt.Chart(ele_df).mark_circle(size=75).encode(
    x=scatter_lookup[scatter_x_var],
    y='Pts',
    color='Pos',
    tooltip=['Name', 'Pts']
)
st.altair_chart(c, use_container_width=True)


st.header('Differentials')
ele_df['point_per_selected_by'] = ele_df['Pts'].astype(float)/ele_df['TSB%'].astype(float)





