
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
  

st.write('''
# My first app
Hello *world!*
''')

data = pd.read_csv('data/emissions.csv')

data_pivot = pd.pivot_table(data, values = 'CO2_emissions', columns = 'year', index = 'country_name') 
years = st.sidebar.slider('Select a range of years', min(data.year), max(data.year), (1995,2002))
countries_list = list(data_pivot.index)
countries = st.sidebar.multiselect('Select countries', (countries_list), default = ['Italy', 'Portugal'])

st.write(f'The range of years selected is {years}, and the countries are {countries}')

data_show = data_pivot.loc[countries, years[0] : years[1]]
st.dataframe(data_show)

years_range = range(years[0], years[1]+1)

# left_column, right_column = st.beta_columns(2)

# with right_column:
data_chart = data.query("country_name in @countries and year in @years_range")
data_chart2 = alt.Chart(data_chart).mark_line().encode(
                x = 'year', y = 'CO2_emissions', color = 'country_name'
        )
st.altair_chart(data_chart2)

# with left_column:   
data_plotly = [dict(type = 'scatter',
                        x = data.query("country_name == @country and year in @years_range")['year'],
                        y = data.query("country_name == @country and year in @years_range")['CO2_emissions'],
                        name = country) 
                        for country in countries]
layout_plotly = dict(title = dict(text = f'{countries} data on CO2 emissions'),
                        xaxis = dict(title = 'Years'),
                        yaxis = dict(title = 'CO2 emissions'))
figure = go.Figure(data = data_plotly, layout = layout_plotly)
st.plotly_chart(figure)