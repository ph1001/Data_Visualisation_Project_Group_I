import streamlit as st
import pandas as pd
import numpy as np 
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px 

crime = pd.read_csv('data/crime_cleaned.csv')
crime2 =pd.read_csv('data/crime_cleaned2.csv')
victim_donut_data = pd.read_excel('data/victims_donut_data.xlsx', index_col = 0)
pop_area_count = pd.read_excel('data/pop_area_count.xlsx', index_col = 0)
crime2['Year_Month'] = pd.to_datetime(crime2['Year_Month'])


left1, right1 = st.beta_columns((2))



# years_selected= st.sidebar.slider('Select a range of years', min(crime.Year), max(crime.Year), (2010,2019))
# years_range = range(years_selected[0], years_selected[1]+1)
# crime = crime.query("Year in @years_range")
# st.write("**All Los Angeles from %i to %i**" % (years_selected[0], (years_selected[1])))



# year_month_selected= st.sidebar.slider('Select a period', min(crime2.Year_Month).date(), max(crime2.Year_Month).date())
# crime = crime2.query("Year_Month == @year_month_selected")

# month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'September', 'October', 'November', 'December']
# # list(crime2.Month.unique())
# year_selected= st.sidebar.selectbox('Select a Year', (list(crime2.Year.unique())))#, default = ['2010'])
# month_selected= st.sidebar.selectbox('Select a Year', (month_list))#, default = ['January'])
# crime = crime2.query("Year == @year_selected and Month == @month_selected")


year_selected= st.sidebar.slider("Select year", min(crime.Year), max(crime.Year))
crime = crime.query("Year == @year_selected")


# year_selected= st.sidebar.slider("Select year", min(crime.Year), max(crime.Year))
# crime = crime.query("Year == @year_selected")

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HeatmapLayer", #'' HexagonLayer
            
                data=data,
                get_position=["LON", "LAT"],
                radius=100,
                elevation_scale=20,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                coverage = 1
            ),
        ]
    ))

zoom_level = 8.5
midpoint = (np.average(crime["LAT"]), np.average(crime["LON"]))
with left1:

    # st.write("**All Los Angeles from %i to %i**" % (years_selected[0], (years_selected[1])))
    st.write("**All Los Angeles crimes in %i**" % (year_selected))
    # st.write(f"**All Los Angeles in {year_month_selected}**")
    # st.write(f"**All Los Angeles crimes in {month_selected} {year_selected}**")
    map(crime, midpoint[0], midpoint[1], zoom_level)

with right1:
    st.write('**BAR PLOT**')


areas = ['Newton',
 'Pacific',
 'Hollywood',
 'Central',
 'Northeast',
 'Hollenbeck',
 'Southwest',
 'Southeast',
 'Rampart',
 'Olympic',
 'Wilshire',
 '77th Street',
 'Harbor',
 'West LA',
 'Van Nuys',
 'West Valley',
 'Mission',
 'Topanga',
 'N Hollywood',
 'Foothill',
 'Devonshire']

st.write('\n')
st.write('\n')
st.write('\n')

expander = st.beta_expander('Select Neighborhood')
area_selected= expander.selectbox('Select a Neighborhood', (areas))

st.write('\n')
st.write('\n')
st.write('\n')

st.write('** LINE PLOT**')

st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')

left3, middle3, right3 = st.beta_columns((1, 1, 1))

def ring(selected):
    data = victim_donut_data[victim_donut_data['AREA NAME'] == selected]
    labels = data['Vict Descent written']
    values = data['Count']

    layout =dict(#title=dict(text=selected),
                 legend = dict(orientation = 'h',
                                y = -0.15))

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)], layout=layout)
    return fig

def bar_chart(selected):
    data = pop_area_count.loc[[selected,'Total Los Angeles'],['Population (approx.)', 'Avg. yearly crime count']]
    data['Avg. number of reported crimes per inhabitants per year'] = data['Avg. yearly crime count'] / data['Population (approx.)']
    data = data.reset_index()
    data = data.rename(columns={'Area name':'Area'})
    title = selected
    fig = px.bar(data, x='Area', y='Avg. number of reported crimes per inhabitants per year')#, title=title)
    return fig

ring = ring(area_selected)
bar = bar_chart(area_selected)

with left3:
    st.write('**NUMBERS**')

with middle3:
    st.plotly_chart(bar, use_container_width= True)

with right3:
    st.plotly_chart(ring, use_container_width = True)