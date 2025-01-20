import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import time

# Berechnung der Ansparphase (mit Regelsparbeitrag)
def calculate_ansparphase(bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung=0):
    restbetrag = -abschlussgebuehr * bausparsumme / 100 + einmalzahlung  # Abschlussgebühr wird direkt abgezogen
    mindestsparguthaben = bausparsumme * 0.4  # Mindestansparsumme (40% der Bausparsumme)
    monate = 0

    while restbetrag < mindestsparguthaben:
        zinsen = max(0, restbetrag) * (sparzins / 100 / 12)
        jahresentgelt_betrag = min((bausparsumme / 1000) * jahresentgelt, 30) / 12
        sparbetrag = monatlicher_sparbeitrag - jahresentgelt_betrag
        restbetrag += sparbetrag + zinsen
        monate += 1

    return monate

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

# Tarifdetails anzeigen (mit Zuteilungszeit)
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
    
    # Eingabe: Bausparsumme
    bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, max_value=500000, step=1000)
    
    if bausparsumme:
        # Dynamischer Vorschlag basierend auf Regelsparbeitrag
        vorschlag_sparrate = bausparsumme * regelsparbeitrag / 1000
        
        # Eingabe: Monatliche Sparrate
        monatlicher_sparbeitrag = st.number_input(
            f"📅 Monatliche Sparrate (Vorschlag: {vorschlag_sparrate:.2f} €, Regelsparbeitrag):",
            min_value=10.0,
            max_value=2000.0,
            value=vorschlag_sparrate,  # Dynamischer Standardwert
            step=10.0,
        )
        st.caption("💡 Der Vorschlag basiert auf dem Regelsparbeitrag des gewählten Tarifs.")

    # Eingabe: Einmalzahlung
    einmalzahlung = st.number_input("💵 Einmalzahlung (€):", min_value=0.0, step=100.0)
    
    # Eingabe: Gewünschte Zuteilungszeit
    zuteilungszeit = st.number_input("⏳ Gewünschte Zeit bis zur Zuteilung (in Jahren):", min_value=1.5, max_value=20.0, step=0.5)

    # Berechnung starten
    if st.button("📊 Berechnung starten"):
        with st.spinner("🔄 Berechnung wird durchgeführt..."):
            time.sleep(2)

        # Ansparphase berechnen
        monate_anspar = calculate_ansparphase(
            bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung
        )

        # Prüfen, ob gewünschte Zuteilungszeit erreicht wird
        if monate_anspar / 12 > zuteilungszeit:
            erforderliche_sparrate = monatlicher_sparbeitrag + 10  # Erhöhungsvorschlag
            st.warning(
                f"⚠️ Die gewünschte Zuteilungszeit von **{zuteilungszeit:.1f} Jahren** kann nicht eingehalten werden. "
                f"Die tatsächliche Ansparzeit beträgt **{monate_anspar / 12:.1f} Jahre**. "
                f"💡 Um die Zuteilungszeit zu erreichen, müsste Ihre monatliche Sparrate auf etwa **{erforderliche_sparrate:.2f} €** erhöht werden."
            )

        # Darlehensphase berechnen
        laufzeit_darlehen, zins_darlehen = calculate_darlehensphase(
            bausparsumme, darlehenszins, zins_tilgung
        )

        st.markdown("## 📋 Ergebnisse")
        st.markdown(
            f"""
            ### 🏦 Ansparphase
            - Dauer bis zur Zuteilung: **{monate_anspar // 12} Jahre und {monate_anspar % 12} Monate**
            - Gesamtes Sparguthaben inkl. Einmalzahlung: **{(monatlicher_sparbeitrag * monate_anspar):,.2f} €**

            ### 💳 Darlehensphase
            - Monatliche Rate (Zins + Tilgung): **{(bausparsumme * zins_tilgung / 1000):,.2f} €**
            - Gesamte Zinskosten während der Darlehensphase: **{zins_darlehen:,.2f} €**
            - Laufzeit des Darlehens: **{laufzeit_darlehen // 12} Jahre und {laufzeit_darlehen % 12} Monate**
            """
        )

# Hauptmenü und Tarifauswahl
st.title("🏠 LBS Bausparrechner")
st.markdown("Wählen Sie einen Tarif aus, um die Berechnungen zu starten.")

tarif = st.radio(
    "Tarif auswählen:",
    ["Classic20 F3", "Sprint22", "Komfort22", "Classic20 F8", "Classic20 Plus F", "Spar25"]
)

if tarif == "Classic20 F3":
    show_tarif_details("Classic20 F3", 0.05, 3, 1.6, 0.30, 3.5, 2.25, 10000)
    tarif_rechner("Classic20 F3", 0.05, 3, 1.6, 0.30, 3.5, 2.25)
elif tarif == "Sprint22":
    show_tarif_details("Sprint22", 0.05, 7, 1.6, 0.30, 6, 1.75, 10000)
    tarif_rechner("Sprint22", 0.05, 7, 1.6, 0.30, 6, 1.75)
elif tarif == "Komfort22":
    show_tarif_details("Komfort22", 0.05, 3, 1.6, 0.30, 7, 2.35, 10000)
    tarif_rechner("Komfort22", 0.05, 3, 1.6, 0.30, 7, 2.35)
elif tarif == "Classic20 F8":
    show_tarif_details("Classic20 F8", 0.05, 3, 1.6, 0.30, 8, 0.95, 10000)
    tarif_rechner("Classic20 F8", 0.05, 3, 1.6, 0.30, 8, 0.95)
elif tarif == "Classic20 Plus F":
    show_tarif_details("Classic20 Plus F", 0.01, 4, 1.6, 0.30, 5, 1.65, 10000)
    tarif_rechner("Classic20 Plus F", 0.01, 4, 1.6, 0.30, 5, 1.65)
elif tarif == "Spar25":
    show_tarif_details("Spar25", 0.25, 5, 1.6, 0.30, 6, 4.25, 10000)
    tarif_rechner("Spar25", 0.25, 5, 1.6, 0.30, 6, 4.25)
```
