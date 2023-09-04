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
    st.session_state.sh = client.open_by_url(url)
    df = pd.DataFrame(st.session_state.sh.worksheet(sheet_name).get_all_records())
    return df

dataframe = load_data(st.secrets["private_gsheets_url"], sheet_name="Sheet1")
worksheet = st.session_state.sh.get_worksheet(0)
def on_click_button():
    cell_list = worksheet.range('A1:A7')
    cell_values = [1,2,3,4,5,6,7]

    for i, val in enumerate(cell_values):  #gives us a tuple of an index and value
        cell_list[i].value = val    #use the index on cell_list and the val from cell_values

    worksheet.update_cells(cell_list) #Fejl i authorization => Google siger også at jeg har en blottet fil i GitHub med Key, men den kan jeg ikke se. ("plasma-bounty"...)
st.button("test af insertion", on_click=on_click_button)


st.experimental_data_editor(dataframe)