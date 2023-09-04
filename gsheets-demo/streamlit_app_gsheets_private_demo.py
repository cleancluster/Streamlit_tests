import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

skey = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)
client = gspread.authorize(credentials)


# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(url, sheet_name="Transactions"):
    sh = client.open_by_url(url)
    df = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())
    worksheet = sh.get_worksheet(0)
    st.button("Test update", on_click=worksheet.update("A2", "CHANGED"))
    return df

dataframe = load_data(st.secrets["private_gsheets_url"], sheet_name="Sheet1")
st.experimental_data_editor(dataframe)