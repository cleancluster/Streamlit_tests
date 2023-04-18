#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


# In[2]:


# Using "with" notation 
# converting dataframe to csv with utf-8 encoding.
def convert_df(df):
    return df.to_csv().encode('utf-8')


def clear_multi():
    st.session_state.multiselect = []
    return

def convert_excel(path, sheet_name = 'Ark1', pri = True):
    df = pd.read_excel(path, sheet_name)
    if pri:
        print('The first 5 rows of the loaded data:')
        display_html(df.head())
    return df

def choose_headers(df, headers_list, pri):
    temp_df = pd.DataFrame()
    for i in range(len(headers_list)):
        if pri:
            print('Choosing the column "', headers_list[i], '"')
        temp_df = pd.concat([temp_df, df[headers_list[i]]], axis = 1)
    return temp_df

def remove_nan(df):
    df = df.dropna().reset_index(drop=True)
    return df

def choose_subsets(df, column_str_list, subset_str_list, pri):
    temp_df = pd.DataFrame()
    for i in range(len(column_str_list)):
        if pri:
            print('Choosing the rows with "', subset_str_list[i], '" in the "', column_str_list[i], '" column.')
        temp_df = pd.concat([temp_df, df[df[column_str_list[i]] == subset_str_list[i]]])
    return temp_df

# Function to convert the dataframe back into an excel sheet.
# More options will follow if there needs to be more sheets etc.
# Inputs: Dataframe as converted by convert_excel, the name you wish the excel file to have (remember .xlsx)
def convert_dataframe(df, name_str):
    file = df.to_excel(name_str)



# In[3]:


# Overskrift for applikationen
st.header('Patentdata fra 2011 til 2022')

# Beskrivelse af applikationen og en klar instruks om hvad man skal gøre.
st.markdown('Dette er en applikation, der har til formål at fremhæve forskellige aspekter af patentdata fået fra [..]  ')


# In[ ]:


# Load the data
data = pd.read_csv("Patentansøgninger_2023/subset_with_coords.csv")


# Load geojson data for map
geojson_data = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"

# Get list of countries in data
countries = data["country"].unique()

# Load geojson data for the selected countries
geojson = []
for country in countries:
    with open(f"{country}.json", "r") as f:
        geojson.append(f.read())

# Create a map centered at (0, 0)
m = folium.Map(location=[0, 0], zoom_start=2)

# Define a color scheme for the clusters
colors = ["#c7e9b4", "#7fcdbb", "#41b6c4", "#1d91c0", "#225ea8"]

# Add a choropleth map layer for each country in the data
for i, country in enumerate(countries):
    country_data = data[data["country"] == country]
    folium.Choropleth(
        geo_data=geojson[i],
        name="choropleth",
        data=country_data,
        columns=["country", "Cluster"],
        key_on="feature.properties.name",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"Cluster for {country}",
        highlight=True,
        overlay=True,
    ).add_to(m)

# Add markers for each country to the map
for i in range(len(data)):
    lat = data.loc[i, "Latitudes"]
    lon = data.loc[i, "Longitudes"]
    country = data.loc[i, "country"]
    cluster = data.loc[i, "Cluster"]
    color = colors[cluster - 1]
    folium.Marker(location=[lat, lon], tooltip=country, icon=folium.Icon(color=color)).add_to(m)

# Display the map in the Streamlit app
st.markdown("<h1>World Map</h1>", unsafe_allow_html=True)
folium_static(m)

# Add legend to the Streamlit app
st.markdown("<h2>Legend:</h2>", unsafe_allow_html=True)
st.markdown('<i class="fa fa-circle fa-1x" style="color:#c7e9b4"></i><span style="margin-left:10px; font-size:18px;">Cluster 1</span>', unsafe_allow_html=True)
st.markdown('<i class="fa fa-circle fa-1x" style="color:#7fcdbb"></i><span style="margin-left:10px; font-size:18px;">Cluster 2</span>', unsafe_allow_html=True)
st.markdown('<i class="fa fa-circle fa-1x" style="color:#41b6c4"></i><span style="margin-left:10px; font-size:18px;">Cluster 3</span>', unsafe_allow_html=True)
st.markdown('<i class="fa fa-circle fa-1x" style="color:#1d91c0"></i><span style="margin-left:10px; font-size:18px;">Cluster 4</span>', unsafe_allow_html=True)
st.markdown('<i class="fa fa-circle fa-1x" style="color:#225ea8"></i><span style="margin-left:10px; font-size:18px;">Cluster 5</span>', unsafe_allow_html=True)