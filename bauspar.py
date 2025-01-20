import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time

# Berechnung der Ansparphase
def calculate_ansparphase_with_pandas(bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung):
    restbetrag = -abschlussgebuehr + einmalzahlung
    mindestsparguthaben = bausparsumme * 0.4
    monate = 0
    data = []

    while restbetrag < mindestsparguthaben:
        zinsen = max(0, restbetrag) * (sparzins / 100 / 12)
        jahresentgelt_betrag = min((bausparsumme / 1000) * jahresentgelt, 30) / 12
        sparbetrag = monatlicher_sparbeitrag - jahresentgelt_betrag
        restbetrag += sparbetrag + zinsen

        data.append({"Monat": monate, "Guthaben": restbetrag, "Zinsen": zinsen, "Sparbetrag": sparbetrag})
        monate += 1

    df = pd.DataFrame(data)
    return df

# Berechnung der Darlehensphase
def calculate_darlehensphase_with_pandas(bausparsumme, darlehenszins, zins_tilgung):
    darlehensbetrag = bausparsumme * 0.6
    monatliche_rate = bausparsumme * zins_tilgung / 1000
    laufzeit_monate = 0
    data = []

    while darlehensbetrag > 0:
        zinsen = darlehensbetrag * (darlehenszins / 100 / 12)
        tilgung = monatliche_rate - zinsen
        darlehensbetrag -= tilgung

        data.append({"Monat": laufzeit_monate, "Restschuld": max(0, darlehensbetrag), "Zinsen": zinsen, "Tilgung": tilgung})
        laufzeit_monate += 1

    df = pd.DataFrame(data)
    return df

# Tarifkonditionen anzeigen
def display_tarif_konditionen(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins):
    regelsparrate = regelsparbeitrag / 1000
    regelsparzeit = int(40 / regelsparrate)  # Mindestsparguthaben = 40% der Bausparsumme
    regelsparzeit_monate = int((40 % regelsparrate) * 12 / regelsparrate)
    regelsparzeit_datum = datetime.now() + timedelta(days=(regelsparzeit * 365) + (regelsparzeit_monate * 30))

    st.markdown(f"### Tarifkonditionen – {name}")
    st.markdown("#### Ansparphase:")
    st.markdown(f"- **Sparzins:** {sparzins:.2f}%")
    st.markdown(f"- **Monatlicher Regelsparbeitrag:** {regelsparbeitrag}‰ der Bausparsumme")
    st.markdown(f"- **Abschlussgebühr:** {abschlussgebuehr:.2f}% der Bausparsumme")
    st.markdown(f"- **Jahresentgelt:** {jahresentgelt:.2f} € pro 1.000 € Bausparsumme (max. 30 € pro Jahr)")
    st.markdown(f"- **Zuteilungszeit bei Regelsparbeitrag:** {regelsparzeit} Jahre und {regelsparzeit_monate} Monate (ca. {regelsparzeit_datum.strftime('%d.%m.%Y')})")
    st.markdown("#### Darlehensphase:")
    st.markdown(f"- **Fester Sollzins:** {darlehenszins:.2f}%")
    st.markdown(f"- **Monatliche Zins- und Tilgungsrate:** {zins_tilgung:.1f}‰ der Bausparsumme")

# Hauptrechner
def tarif_rechner(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins):
    display_tarif_konditionen(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins)

    st.markdown("### 📝 Geben Sie Ihre Daten ein:")
    bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, max_value=500000, step=1000)
    einmalzahlung = st.number_input("💵 Einmalzahlung (€):", min_value=0.0, step=100.0)

    if bausparsumme:
        vorschlag_sparrate = max(bausparsumme * regelsparbeitrag / 1000, 50)
        monatlicher_sparbeitrag = st.number_input(
            f"📅 Monatliche Sparrate (Vorschlag: {vorschlag_sparrate:.2f} €, Regelsparbeitrag):",
            min_value=50.0,
            max_value=2000.0,
            value=float(vorschlag_sparrate),
            step=10.0,
        )
        st.caption("💡 Der Vorschlag basiert auf dem Regelsparbeitrag des gewählten Tarifs.")

    zuteilungszeit = st.number_input("⏳ Gewünschte Zeit bis zur Zuteilung (in Jahren):", min_value=1.5, max_value=20.0, step=0.5)

    if st.button("📊 Berechnung starten"):
        with st.spinner("🔄 Berechnung wird durchgeführt..."):
            time.sleep(2)

        df_anspar = calculate_ansparphase_with_pandas(
            bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung
        )

        monate_anspar = len(df_anspar)
        zuteilungsdatum = datetime.now() + timedelta(days=(monate_anspar * 30))

        if monate_anspar / 12 > zuteilungszeit:
            erforderliche_sparrate = monatlicher_sparbeitrag + 10
            st.warning(
                f"⚠️ Die gewünschte Zuteilungszeit von **{zuteilungszeit:.1f} Jahren** kann nicht eingehalten werden. "
                f"Die tatsächliche Ansparzeit beträgt **{monate_anspar / 12:.1f} Jahre** (ca. **{zuteilungsdatum.strftime('%d.%m.%Y')}**). "
                f"💡 Um die Zuteilungszeit zu erreichen, müsste Ihre monatliche Sparrate auf etwa **{erforderliche_sparrate:.2f} €** erhöht werden."
            )

# Hauptmenü und Tarifauswahl
st.title("🏠 LBS Bausparrechner")
st.markdown("Wählen Sie einen Tarif aus, um die Berechnungen zu starten.")

tarif = st.radio(
    "Tarif auswählen:",
    ["Classic20 F3", "Sprint22", "Komfort22", "Classic20 F8", "Classic20 Plus F", "Spar25"]
)

if tarif == "Classic20 F3":
    tarif_rechner("Classic20 F3", 0.05, 3, 1.6, 0.30, 3.5, 2.25)
elif tarif == "Sprint22":
    tarif_rechner("Sprint22", 0.05, 7, 1.6, 0.30, 6, 1.75)
elif tarif == "Komfort22":
    tarif_rechner("Komfort22", 0.05, 3, 1.6, 0.30, 7, 2.35)
elif tarif == "Classic20 F8":
    tarif_rechner("Classic20 F8", 0.05, 3, 1.6, 0.30, 8, 0.95)
elif tarif == "Classic20 Plus F":
    tarif_rechner("Classic20 Plus F", 0.01, 4, 1.6, 0.30, 5, 1.65)
elif tarif == "Spar25":
    tarif_rechner("Spar25", 0.25, 5, 1.6, 0.30, 6, 4.25)












