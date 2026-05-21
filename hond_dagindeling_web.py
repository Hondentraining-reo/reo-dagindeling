import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Hondentraining REO", page_icon="🐾", layout="wide")

# Header met logo
col_logo, col_titel = st.columns([1.2, 5])
with col_logo:
    try:
        st.image("logo.png", width=160)
    except:
        st.markdown("# 🐾")

with col_titel:
    st.title("Honden Dagindeling Tool")
    st.markdown("**Hondentraining REO**")

# Styling
st.markdown("""
<style>
    .stButton>button {background-color: #2e7d32; color: white; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Basis info
col_eig, col_hond = st.columns(2)
with col_eig:
    eigenaar = st.text_input("**Naam Eigenaar**", placeholder="Voor- en achternaam", key="eigenaar")
with col_hond:
    hond = st.text_input("**Naam Hond**", placeholder="Naam van de hond", key="hond_naam")

dag = st.selectbox("**Kies dag**", 
                   ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"], 
                   key="dag_select")

st.divider()

tab1, tab2, tab3 = st.tabs(["🐕 Beweging & 😴 Slaap", "🍖 Eten & 🎾 Spelen", "📋 Gebeurtenissen"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Beweging")
        bew_u = st.number_input("Uren", 0, 24, 1, key="bew_u")
        bew_m = st.number_input("Minuten", 0, 59, 0, key="bew_m")
        bew_tijd = st.text_input("Tijdstippen", "08:00, 13:30, 18:00", key="bew_tijd")
    with c2:
        st.subheader("Slaap")
        slaap_u = st.number_input("Uren", 0, 24, 12, key="slaap_u")
        slaap_m = st.number_input("Minuten", 0, 59, 0, key="slaap_m")
        slaap_tijd = st.text_input("Tijdstippen", "22:00 - 07:00", key="slaap_tijd")

with tab2:
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Eten")
        eten_g = st.number_input("Totale hoeveelheid (gram)", 0, 3000, 400, key="eten_g")
        eten_t = st.text_input("Tijdstippen", "07:30, 18:00", key="eten_t")
    with c4:
        st.subheader("Spelen")
        spel_u = st.number_input("Uren", 0, 24, 0, key="spel_u")
        spel_m = st.number_input("Minuten", 0, 59, 30, key="spel_m")
        spel_t = st.text_input("Tijdstippen", "20:00", key="spel_t")

with tab3:
    st.subheader("Gebeurtenissen & Bijzonderheden")
    gebeurtenissen = st.text_area("Andere opmerkingen", height=130,
                                  placeholder="Alleen thuis, training, dierenarts, etc.", key="gebeurtenissen")

# Opslaan
if st.button("💾 Opslaan voor deze dag", type="primary", use_container_width=True):
    if not eigenaar or not hond:
        st.error("Vul Naam Eigenaar en Naam Hond in.")
    else:
        data = {
            "Eigenaar": eigenaar,
            "Hond": hond,
            "Dag": dag,
            "Beweging_Uren": bew_u,
            "Beweging_Minuten": bew_m,
            "Beweging_Tijdstippen": bew_tijd,
            "Slaap_Uren": slaap_u,
            "Slaap_Minuten": slaap_m,
            "Slaap_Tijdstippen": slaap_tijd,
            "Eten_Gram": eten_g,
            "Eten_Tijdstippen": eten_t,
            "Spelen_Uren": spel_u,
            "Spelen_Minuten": spel_m,
            "Spelen_Tijdstippen": spel_t,
            "Gebeurtenissen": gebeurtenissen,
            "Ingevuld_op": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        filename = "Honden_Dagindeling_REO.xlsx"
        if os.path.exists(filename):
            df = pd.read_excel(filename)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        else:
            df = pd.DataFrame([data])
        
        df.to_excel(filename, index=False)
        st.success(f"✅ {dag} voor **{hond}** opgeslagen!")
        st.balloons()

st.divider()

if st.checkbox("📊 Toon alle ingevulde dagen", key="toon_overzicht"):
    filename = "Honden_Dagindeling_REO.xlsx"
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        st.dataframe(df, use_container_width=True)
        
        with open(filename, "rb") as file:
            excel_data = file.read()
        st.download_button("📥 Download volledige Excel", excel_data, filename)
    else:
        st.info("Nog geen gegevens ingevoerd.")

st.caption("Hondentraining REO")