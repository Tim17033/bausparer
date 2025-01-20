import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import time

# Berechnung der Ansparphase mit dynamischer Sparrate
def calculate_ansparphase(bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung=0):
    restbetrag = -abschlussgebuehr * bausparsumme / 100 + einmalzahlung  # Abschlussgebühr und Einmalzahlung berücksichtigen
    mindestsparguthaben = bausparsumme * 0.4  # Mindestansparsumme (40% der Bausparsumme)
    monate = 0

    while restbetrag < mindestsparguthaben:
        zinsen = max(0, restbetrag) * (sparzins / 100 / 12)
        jahresentgelt_betrag = min((bausparsumme / 1000) * jahresentgelt, 30) / 12
        sparbetrag = monatlicher_sparbeitrag - jahresentgelt_betrag
        restbetrag += sparbetrag + zinsen
        monate += 1

    return monate

# Berechnung des Lösungsansatzes (Sparrate für gewünschte Zuteilungszeit)
def calculate_sparrate_for_target_time(bausparsumme, zielzeit_in_jahren, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung=0):
    zielzeit_in_monaten = int(zielzeit_in_jahren * 12)
    mindestsparguthaben = bausparsumme * 0.4  # 40% der Bausparsumme
    restbetrag = -abschlussgebuehr * bausparsumme / 100 + einmalzahlung
    monatliche_sparrate = 50  # Startwert für die Berechnung
    zinsen_pro_monat = sparzins / 100 / 12

    while True:
        temp_restbetrag = restbetrag
        for monat in range(zielzeit_in_monaten):
            zinsen = max(0, temp_restbetrag) * zinsen_pro_monat
            jahresentgelt_betrag = min((bausparsumme / 1000) * jahresentgelt, 30) / 12
            temp_restbetrag += monatliche_sparrate - jahresentgelt_betrag + zinsen

        if temp_restbetrag >= mindestsparguthaben:
            break
        monatliche_sparrate += 10  # Erhöhe die Sparrate in Schritten von 10 €

    return monatliche_sparrate

# Berechnung der Darlehensphase
def calculate_darlehensphase(bausparsumme, darlehenszins, zins_tilgung):
    darlehensbetrag = bausparsumme * 0.6  # 60% der Bausparsumme
    monatliche_rate = bausparsumme * zins_tilgung / 1000
    laufzeit_monate = 0
    zinskosten_gesamt = 0

    while darlehensbetrag > 0:
        zinsen = darlehensbetrag * (darlehenszins / 100 / 12)
        tilgung = monatliche_rate - zinsen
        darlehensbetrag -= tilgung
        laufzeit_monate += 1
        zinskosten_gesamt += zinsen

    return laufzeit_monate, zinskosten_gesamt

# Tarifdetails anzeigen
def show_tarif_details(tarif_name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins, bausparsumme):
    vorschlag_sparrate = bausparsumme * regelsparbeitrag / 1000
    monate_regelspar = calculate_ansparphase(bausparsumme, vorschlag_sparrate, sparzins, abschlussgebuehr, jahresentgelt)
    zuteilungsdatum = datetime.now() + timedelta(days=(monate_regelspar * 30))

    st.markdown(f"### Tarifkonditionen – {tarif_name}")
    st.markdown(
        f"""
        **Ansparphase:**
        - Sparzins: **{sparzins:.2f}%**
        - Monatlicher Regelsparbeitrag: **{regelsparbeitrag}‰** der Bausparsumme
        - Abschlussgebühr: **{abschlussgebuehr:.2f}%** der Bausparsumme
        - Jahresentgelt: **{jahresentgelt:.2f} €** pro 1.000 € Bausparsumme (max. 30 € pro Jahr)
        - Mindestsparsumme: **40% der Bausparsumme**
        - Zuteilungszeit bei Regelsparbeitrag: **{monate_regelspar // 12} Jahre und {monate_regelspar % 12} Monate** (ca. **{zuteilungsdatum.strftime('%d.%m.%Y')}**)

        **Darlehensphase:**
        - Fester Sollzins: **{darlehenszins:.2f}%**
        - Monatliche Zins- und Tilgungsrate: **{zins_tilgung}‰** der Bausparsumme
        """
    )

# Hauptrechner
def tarif_rechner(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins):
    st.title(f"🏠 LBS Bausparrechner – {name}")
    
    bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, max_value=500000, step=1000)
    if bausparsumme:
        vorschlag_sparrate = bausparsumme * regelsparbeitrag / 1000
        monatlicher_sparbeitrag = st.number_input(
            f"📅 Monatliche Sparrate (Vorschlag: {vorschlag_sparrate:.2f} €, Regelsparbeitrag):",
            min_value=10.0,
            max_value=2000.0,
            value=vorschlag_sparrate,
            step=10.0,
        )
        st.caption("💡 Der Vorschlag basiert auf dem Regelsparbeitrag des gewählten Tarifs.")

    einmalzahlung = st.number_input("💵 Einmalzahlung (€):", min_value=0.0, step=100.0)
    zuteilungszeit = st.number_input("⏳ Gewünschte Zeit bis zur Zuteilung (in Jahren):", min_value=1.5, max_value=20.0, step=0.5)

    if st.button("📊 Berechnung starten"):
        with st.spinner("🔄 Berechnung wird durchgeführt..."):
            time.sleep(2)

        # Ansparphase berechnen
        monate_anspar = calculate_ansparphase(
            bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung
        )

        if monate_anspar / 12 > zuteilungszeit:
            erforderliche_sparrate = calculate_sparrate_for_target_time(
                bausparsumme, zuteilungszeit, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung
            )
            st.warning(
                f"⚠️ Die gewünschte Zuteilungszeit von **{zuteilungszeit:.1f} Jahren** kann nicht eingehalten werden. "
                f"Die tatsächliche Ansparzeit beträgt **{monate_anspar / 12:.1f} Jahre**. "
                f"💡 Um die Zuteilungszeit zu erreichen, müsste Ihre monatliche Sparrate auf etwa **{erforderliche_sparrate:.2f} €** erhöht werden."
            )


