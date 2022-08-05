import streamlit as st


st.set_page_config(page_title='Tims First Website', page_icon=':shark:', layout='wide')
st.title('Hello and welcome to Tim\'s first website!')
st.write('Please check back soon for updates and Fantasy Premier League Football tips and stats.')

st.write('[Personal Github Page](https://github.com/TimYouell15)')

if st.button('Click me for a joke'):
	st.write('The change in weather here in Sydney has got me swapping from aerosol deodorant. Roll on next week.')
else:
	st.write('I promise it will be worth it')


