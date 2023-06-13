import streamlit as st
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(":memory:")

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
cursor = conn.cursor()

query = "SELECT * FROM a_table"
for row in cursor.execute(query):
    print(row)