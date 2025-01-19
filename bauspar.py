import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Berechnung der Ansparphase
def calculate_ansparphase(bausparsumme, monatsrate, zinssatz, einmalzahlung=0):
    guthaben = einmalzahlung
    monate = 0
    zinsen_gesamt = 0

    # Mindestsparguthaben von 40 % der Bausparsumme
    mindestsparguthaben = bausparsumme * 0.4

    # Ansparphase simulieren
    while guthaben < mindestsparguthaben:
        zinsen = guthaben * (zinssatz / 100 / 12)
        guthaben += zinsen + monatsrate
        zinsen_gesamt += zinsen
        monate += 1

    return monate, guthaben, zinsen_gesamt

# Berechnung der Darlehensphase
def calculate_darlehensphase(bausparsumme, zinssatz_darlehen, monatliche_rate):
    restschuld = bausparsumme * 0.6
    zinsen_gesamt = 0
    monate = 0

    # Darlehensphase simulieren
    while restschuld > 0:
        zinsen = restschuld * (zinssatz_darlehen / 100 / 12)
        tilgung = monatliche_rate - zinsen
        restschuld -= tilgung
        zinsen_gesamt += zinsen
        monate += 1

    return monate, zinsen_gesamt

# Interaktive Eingaben
st.title("🏠 LBS Bausparrechner")
st.markdown("Berechnen Sie Ihre Anspar- und Darlehensphase mit diesem Bausparrechner.")

# Eingabefelder
st.markdown("### 🛠️ Schritt 1: Bausparsumme und Ansparphase")
bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, max_value=500000, step=1000)
monatsrate = st.number_input("📅 Monatliche Sparrate (€):", min_value=50, max_value=2000, step=50)
zinssatz_sparen = st.number_input("📈 Zinsen auf Sparguthaben (% p.a.):", min_value=0.0, max_value=5.0, step=0.1)
einmalzahlung = st.number_input("💵 Einmalzahlung zu Beginn (€):", min_value=0, step=100)

st.markdown("### 🛠️ Schritt 2: Darlehensphase")
zinssatz_darlehen = st.number_input("📉 Zinssatz für das Bauspardarlehen (% p.a.):", min_value=0.5, max_value=5.0, step=0.1)
monatliche_rate_darlehen = st.number_input("📅 Monatliche Rückzahlungsrate (€):", min_value=100, max_value=2000, step=50)

# Berechnung starten
if st.button("📊 Berechnung starten"):
    with st.spinner("🔄 Berechnung wird durchgeführt..."):
        time.sleep(2)  # Simulierte Ladezeit

    # Ansparphase berechnen
    monate_anspar, guthaben, zinsen_anspar = calculate_ansparphase(
        bausparsumme, monatsrate, zinssatz_sparen, einmalzahlung
    )

    # Darlehensphase berechnen
    monate_darlehen, zinsen_darlehen = calculate_darlehensphase(
        bausparsumme, zinssatz_darlehen, monatliche_rate_darlehen
    )

    # Ergebnisse anzeigen
    st.markdown("## 📋 Ergebnisse")
    st.markdown(
        f"""
        ### 🏦 Ansparphase
        - Dauer der Ansparphase: **{monate_anspar // 12} Jahre und {monate_anspar % 12} Monate**
        - Gesamtes Sparguthaben (inkl. Zinsen): **{guthaben:,.2f} €**
        - Insgesamt erhaltene Zinsen: **{zinsen_anspar:,.2f} €**

        ### 💳 Darlehensphase
        - Dauer der Darlehensphase: **{monate_darlehen // 12} Jahre und {monate_darlehen % 12} Monate**
        - Insgesamt gezahlte Zinsen im Darlehen: **{zinsen_darlehen:,.2f} €**
        """
    )

    # Visualisierung der Ansparphase
    st.markdown("### 📊 Ansparverlauf")
    monate = np.arange(1, monate_anspar + 1)
    guthaben_werte = [einmalzahlung + i * monatsrate + sum([(j * (zinssatz_sparen / 100 / 12)) for j in range(i)]) for i in monate]

    plt.figure(figsize=(10, 5))
    plt.plot(monate, guthaben_werte, label="Guthaben inkl. Zinsen", color="orange")
    plt.axhline(y=bausparsumme * 0.4, color="green", linestyle="--", label="Mindestsparguthaben (40%)")
    plt.title("Ansparverlauf")
    plt.xlabel("Monate")
    plt.ylabel("Guthaben (€)")
    plt.legend()
    st.pyplot(plt)

    # Visualisierung der Darlehensphase
    st.markdown("### 📊 Darlehensverlauf")
    restschuld = bausparsumme * 0.6
    monate = np.arange(1, monate_darlehen + 1)
    restschulden_werte = []

    for _ in monate:
        zinsen = restschuld * (zinssatz_darlehen / 100 / 12)
        tilgung = monatliche_rate_darlehen - zinsen
        restschuld -= tilgung
        restschulden_werte.append(restschuld)

    plt.figure(figsize=(10, 5))
    plt.plot(monate, restschulden_werte, label="Restschuld", color="red")
    plt.title("Darlehensverlauf")
    plt.xlabel("Monate")
    plt.ylabel("Restschuld (€)")
    plt.legend()
    st.pyplot(plt)
