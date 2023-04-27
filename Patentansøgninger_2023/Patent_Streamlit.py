import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd

#For Lottie animations
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import requests

#For login part (necsesary for streamlit_authenticator)
import yaml
from yaml import load, dump
from yaml.loader import SafeLoader

#To add logo
from PIL import Image

# To send emails (For password recovery)
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#To delete Admin page, when user is not admin
from pathlib import Path
#Import data from Google sheets
#from google.oauth2 import service_account
#from shillelagh.backends.apsw.db import connect

# Sets up Favicon, webpage title and layout

st.set_page_config(page_title="**CLEAN INSIGHTS**")
# Top sidebar CLEAN logo + removal of "Made with Streamlit" & Streamlit menu + no padding top and bottom
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://cleancluster.dk/wp-content/uploads/2022/09/CLEAN-logo-white.png);
                background-repeat: no-repeat;
                background-position: 20px 20px;
                background-size: 265px;
                width: 325px;
                height: 215px;
            }

            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}

            div.block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                }

        </style>
        """,
        unsafe_allow_html=True,
    )
#add_logo()

##### Helper functions #####
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


# Define function for each page
def Patent():
    st.header("Patentapplications in the period 2011 - 2022")
    st.write("This page will provide information about the applications of patents around the world")
    df_rådata = convert_excel("Patentansøgninger_2023/Miljøteknologi rådata.xlsx", sheet_name="DATA_til_eksport_v2", pri=False)
    df_countrycodes = convert_excel("Patentansøgninger_2023/Countrycodes.xlsx", sheet_name="Countrycodes", pri=False)
    df_populations = convert_excel("Patentansøgninger_2023/world_population.xlsx", sheet_name="world_population", pri=False)
    df_dk = choose_subsets(df_rådata, ["person_ctry_code"], ["DK"], True)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total amount of patents mapped", len(df_rådata.index))
        st.metric("Patents involved with water", df_rådata["Vand"].count(), help="Some patents have multiple areas that they are involved in.")

    with col2:
        st.metric("Number of different countries included:", len(df_rådata["person_ctry_code"].unique()), help="Some countries might be excluded from later conclusions due to specific tax regulations in said countries. This will also be specified therein.")
        st.metric("Patents involved with climate adaptation", df_rådata["Klimatilpasning"].count(), help="Some patents have multiple areas that they are involved in.")
    with col3:
        st.metric("Patents applied for by danish companies", len(df_dk))
        st.metric("Patents involved with Waste, Ressources and Materials", df_rådata["Affald"].count(), help="Some patents have multiple areas that they are involved in.")

    with col4:
        st.metric("Number of danish companies:", len(df_dk["psn_name"].unique()), help="The number of danish companies responsible for the patent applications. Some of which might be out of business at this point in time.")
        st.metric("Patents involved with Air", df_rådata["Luft"].count(), help="Some patents have multiple areas that they are involved in.")

    with col5:
        st.metric("TBD", "TBD")
        st.metric("Patents involved with Nature", df_rådata["Natur"].count(), help="Some patents have multiple areas that they are involved in.")

    
def page2():
    st.header("Page 2")
    st.write("This is the second page of the application.")

def page3():
    st.header("Page 3")
    st.write("This is the third page of the application.")

# Define sidebar options
sidebar_options = {
    "Patentapplications": Patent,
    "Page 2": page2,
    "Page 3": page3
}

# Set the title and the sidebar

selection = st.sidebar.radio("Go to", list(sidebar_options.keys()))
st.sidebar.info('This application is developed so that you can gain insights in the danish ecosystem of companies working with environmental technology.', icon="ℹ️")

# Display the selected page
page = sidebar_options[selection]
page()
