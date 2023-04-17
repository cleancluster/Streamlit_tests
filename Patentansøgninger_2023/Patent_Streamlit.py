#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px


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

# Define the color scheme for the groups
color_scheme = {0: 'blue', 1: 'red', 2: 'green', 3: 'yellow', 4: 'purple'}

# Create a scatter plot with markers for each country, color-coded by group
fig = px.scatter_geo(data, lat='Latitudes', lon='Longitudes', color='Cluster',
                     color_discrete_sequence=[color_scheme[0], color_scheme[1], color_scheme[2], color_scheme[3], color_scheme[4]], hover_name='country')

# Update the layout to set the map projection and the size
fig.update_geos(projection_type='natural earth', showland=True, landcolor='lightgray',
                showocean=True, oceancolor='azure', showcountries=True, countrycolor='gray')
fig.update_layout(width=800, height=600, margin={"r":0,"t":0,"l":0,"b":0})

# Display the map
st.plotly_chart(fig)

