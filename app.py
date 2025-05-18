import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connexion à la base SQLite3
conn = sqlite3.connect("data.db")
df = pd.read_sql_query("SELECT * FROM data", conn)
conn.close()

# Création du DataFrame
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Affichage dans Streamlit
st.dataframe(df)

# Nuage de points pour la température
fig_temp = px.scatter(df, x="timestamp", y="temperature", title="Évolution de la température")
fig_temp.add_hrect(y0=15, y1=25, fillcolor="green", opacity=0.4, line_width=0)
fig_temp.update_yaxes(title="Température (°C)", range=[0, 50])
fig_temp.update_xaxes(title="Temps")

# Nuage de points pour l'humidité
fig_hum = px.scatter(df, x="timestamp", y="humidity", title="Évolution du taux d'humidité")
fig_hum.add_hrect(y0=85, y1=90, fillcolor="green", opacity=0.4, line_width=0)
fig_hum.update_yaxes(title="Humidité (%)", range=[0, 120])
fig_hum.update_xaxes(title="Temps")

# Affichage dans Streamlit
st.plotly_chart(fig_temp, use_container_width=True)
st.plotly_chart(fig_hum, use_container_width=True)