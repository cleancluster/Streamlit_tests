import streamlit as st
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect
import toml

#print(st.secrets["gcp_service_account"])
#data = toml.load(st.secrets["gcp_service_account"])
st.write(st.secrets["gcp_service_account"])
connection = connect(
    ":memory:",
    adapter_kwargs={
        "gsheetsapi": {
            "service_account_file": st.secrets["gcp_service_account"],
        },
    },
)
cursor = connection.cursor()

SQL = """
SELECT *
FROM "https://docs.google.com/spreadsheets/d/1-FQwy2py4xRr1WBp9B9V7yy0pbhCTbVCEZGD4cpUvzM/edit#gid=0"
"""
for row in cursor.execute(SQL):
    print(row)