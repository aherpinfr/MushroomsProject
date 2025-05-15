import streamlit as st
import sqlite3
import pandas as pd

# Connexion à la base SQLite3
conn = sqlite3.connect("data.db")
df = pd.read_sql_query("SELECT * FROM data", conn)
conn.close()

# Affichage dans Streamlit
st.dataframe(df)