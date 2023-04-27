import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import time
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
from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)

#Import data from Google sheets
#from google.oauth2 import service_account
#from shillelagh.backends.apsw.db import connect

# Sets up Favicon, webpage title and layout


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
add_logo()

##### Helper functions #####
# Get Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Delete (hide) a page
def delete_page(main_script_path_str, page_name):

    current_pages = get_pages(main_script_path_str)

    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]
            break
        else:
            pass
    _on_pages_changed.send()

# Add (make visible) a page 
def add_page(main_script_path_str, page_name):
    
    pages = get_pages(main_script_path_str)
    main_script_path = Path(main_script_path_str)
    pages_dir = main_script_path.parent / "pages"

    script_path = [f for f in list(pages_dir.glob("*.py"))+list(main_script_path.parent.glob("*.py")) if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())
    pi, pn = page_icon_and_name(script_path)
    psh = calc_md5(script_path_str)
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }
    _on_pages_changed.send()


# Define function for each page
def Patent():
    st.header("Patentapplications")
    st.write("This page will provide information about the applications of patents around the world")

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
st.set_page_config(page_title="**CLEAN INSIGHTS**")
selection = st.sidebar.radio("Go to", list(sidebar_options.keys()))
st.sidebar.info('This application is developed so that you can gain insights in the danish ecosystem of companies working with environmental technology.', icon="ℹ️")

# Display the selected page
page = sidebar_options[selection]
page()
