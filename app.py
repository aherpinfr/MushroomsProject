import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connexion à la base SQLite3
conn = sqlite3.connect("data.db")
df = pd.read_sql_query("SELECT * FROM data", conn)

# Création de la table notes si elle n'existe pas
conn.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chart TEXT NOT NULL,
    content TEXT
)
""")
conn.commit()

# Fonctions utilitaires pour les notes
def get_note(chart):
    cur = conn.execute("SELECT content FROM notes WHERE chart = ?", (chart,))
    row = cur.fetchone()
    return row[0] if row else ""

def save_note(chart, content):
    if get_note(chart):
        conn.execute("UPDATE notes SET content = ? WHERE chart = ?", (content, chart))
    else:
        conn.execute("INSERT INTO notes (chart, content) VALUES (?, ?)", (chart, content))
    conn.commit()

def delete_note(chart):
    conn.execute("DELETE FROM notes WHERE chart = ?", (chart,))
    conn.commit()

def get_all_notes():
    cur = conn.execute("SELECT chart, content FROM notes")
    return cur.fetchall()

# Menu de navigation dans la barre latérale
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à :", ["Tableau de bord", "Notes enregistrées"])

# Page 1 : Tableau de bord (graphiques + prise de notes)
if page == "Tableau de bord":
    df["timestamp"] = pd.to_datetime(df["timestamp"])

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

    # Affichage dans Streamlit avec notes à droite
    col1, col2 = st.columns([3, 1])

    with col1:
        st.plotly_chart(fig_temp, use_container_width=True)
    with col2:
        st.markdown("**Note pour la température**")
        note_temp = st.text_area("Ajouter une note", value=get_note("temperature"), key="note_temp")
        if st.button("Enregistrer la note", key="save_temp"):
            save_note("temperature", note_temp)
            st.success("Note enregistrée")
            st.experimental_rerun()


    st.markdown("---")

    col3, col4 = st.columns([3, 1])

    with col3:
        st.plotly_chart(fig_hum, use_container_width=True)
    with col4:
        st.markdown("**Note pour l'humidité**")
        note_hum = st.text_area("Ajouter une note", value=get_note("humidity"), key="note_hum")
        if st.button("Enregistrer la note", key="save_hum"):
            save_note("humidity", note_hum)
            st.success("Note enregistrée")
            st.experimental_rerun()


# Page 2 : Notes enregistrées
elif page == "Notes enregistrées":
    st.title("Notes enregistrées")
    all_notes = get_all_notes()
    if all_notes:
        for chart, content in all_notes:
            col_note, col_btn = st.columns([4, 1])
            with col_note:
                st.markdown(f"**{chart.capitalize()} :**")
                st.write(content if content.strip() else "_(Aucune note)_")
            with col_btn:
                if st.button(f"🗑️ Supprimer", key=f"delete_{chart}_recorded"):
                    delete_note(chart)
                    st.success(f"Note '{chart}' supprimée")
                    st.experimental_rerun()
    else:
        st.write("Aucune note enregistrée.")

conn.close()
