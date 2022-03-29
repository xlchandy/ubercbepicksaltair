import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
st.title('Uber pickups in Coimbatore')
DATE_COLUMN = 'date/time'
def load_data(nrows):
    data = pd.read_csv('uberdata.csv', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

#Create a text element and let the reader know that the data is loading
data_load_state=st.text('Loading Data..')

#Load 10,000 rows of data into the dataframe
data=load_data(10000)

#Notify the reader that the data was successfully loaded
data_load_state.text('Loading Data..Done')

#Print a Histogram
st.subheader('Number of Pickups by hour')

hist_values =np.histogram(data[DATE_COLUMN].dt.hour,bins=24,range=(0,24))[0]

hist_values_pd = pd.DataFrame(data=hist_values, columns=['Pickups per Hour'])

Chart1 = alt.Chart(hist_values_pd.reset_index()).mark_bar().encode(
       alt.X('index:N', title='Hour of the Day'),
       alt.Y('Pickups per Hour:Q')
       ).properties (width=800,height=400,title='Pick Ups in Coimbatore by Hour').configure_axis(grid=False)

st.altair_chart(Chart1,use_container_width=True)

# Print map of all pickups
st.subheader('Map of Pickups')

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=11.01,
         longitude=76.95,
         zoom=14,
         pitch=0,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=data,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=20,
         ),
     ],
 ))
            
# Print map at 10 AM
hour_to_filter=10
filtered_data=data[data[DATE_COLUMN].dt.hour==hour_to_filter]

st.subheader('Map of all Pickups at '+ str(hour_to_filter) + ':00 AM')
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=11.01,
         longitude=76.95,
         zoom=14,
         pitch=0,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=filtered_data,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=20,
         ),
     ],
 ))

