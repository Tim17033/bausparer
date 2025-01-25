import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import time

# Berechnung der Ansparphase
def calculate_ansparphase_with_pandas(bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung):
    restbetrag = -abschlussgebuehr + einmalzahlung

    # Defining minimum savings percentages for different tariffs
    tarif_mindestansparsumme = {
        "Classic20 Plus F": 0.4,
        "Classic20 F8": 0.4,
        "Komfort22": 0.3,
        "Sprint22": 0.5,
        "Classic20 F3": 0.4,
        "Spar25": 0.4,
    }

    # Define 'tarif_name' dynamically or pass it as a parameter for the function
    if 'tarif_name' not in locals():
        tarif_name = 'Classic20 Plus F'  # Default tariff name for demonstration; replace or pass as needed

    # Ensure 'tarif_name' contains the correct name of the current tariff
    mindestsparguthaben = bausparsumme * tarif_mindestansparsumme.get(tarif_name, 0.4)  # Default to 40% if tariff not listed

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
def calculate_darlehensphase_with_pandas(bausparsumme, angespartes_guthaben, darlehenszins, zins_tilgung):
    darlehensbetrag = bausparsumme - angespartes_guthaben
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

# Berechnung der erforderlichen Sparrate
def calculate_adjusted_sparrate(bausparsumme, abschlussgebuehr, sparzins, jahresentgelt, zuteilungszeit, einmalzahlung):

    # Defining minimum savings percentages for different tariffs
    tarif_mindestansparsumme = {
        "Classic20 Plus F": 0.4,
        "Classic20 F8": 0.4,
        "Komfort22": 0.3,
        "Sprint22": 0.5,
        "Classic20 F3": 0.4,
        "Spar25": 0.4,
    }

    # Define 'tarif_name' dynamically or pass it as a parameter for the function
    if 'tarif_name' not in locals():
        tarif_name = 'Classic20 Plus F'  # Default tariff name for demonstration; replace or pass as needed

    # Ensure 'tarif_name' contains the correct name of the current tariff
    mindestsparguthaben = bausparsumme * tarif_mindestansparsumme.get(tarif_name, 0.4)  # Default to 40% if tariff not listed

    restbetrag = -abschlussgebuehr + einmalzahlung
    jahresentgelt_betrag = min((bausparsumme / 1000) * jahresentgelt, 30)
    monate = int(zuteilungszeit * 12)
    monatlicher_sparbeitrag = (mindestsparguthaben - restbetrag) / monate + (jahresentgelt_betrag / 12)
    return monatlicher_sparbeitrag

# Anzeige der Tarifkonditionen mit Darlehensphaseninformationen
def display_tarif_konditionen(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins, bausparsumme):
    vorschlag_sparrate = bausparsumme * regelsparbeitrag / 1000
    df_regelspar = calculate_ansparphase_with_pandas(
        bausparsumme, vorschlag_sparrate, sparzins, abschlussgebuehr, jahresentgelt, 0
    )
    monate_regelspar = len(df_regelspar)
    zuteilungsdatum = datetime.now() + timedelta(days=(monate_regelspar * 30))

    angespartes_guthaben = bausparsumme * 0.4
    darlehensphase_df = calculate_darlehensphase_with_pandas(
        bausparsumme, angespartes_guthaben, darlehenszins, zins_tilgung
    )
    monatliche_darlehensrate = darlehensphase_df["Tilgung"].iloc[0] + darlehensphase_df["Zinsen"].iloc[0]
    laufzeit_darlehen = len(darlehensphase_df)

    st.markdown(f"### Tarifkonditionen")
    st.markdown("### Mindestansparsummen aller Tarife")
    for tarif, prozent in tarif_mindestansparsumme.items():
        st.markdown(f"- **{tarif}**: {bausparsumme * prozent:,.2f} € ({int(prozent * 100)}%)")
    - {name}")
    st.markdown(
        f"""""""
        **Ansparphase:**
        - Sparzins: **{sparzins:.2f}%**
        - Monatlicher Regelsparbeitrag: **{regelsparbeitrag}‰** der Bausparsumme
        - Abschlussgebühr: **{abschlussgebuehr:.2f}%** der Bausparsumme
        - Jahresentgelt: **{jahresentgelt:.2f} €** pro 1.000 € Bausparsumme (max. 30 € pro Jahr)
        - Mindestansparsumme: **{bausparsumme * 0.4:,.2f} €**
        - Zuteilungszeit bei Regelsparbeitrag: **{monate_regelspar // 12} Jahre und {monate_regelspar % 12} Monate** (ca. **{zuteilungsdatum.strftime('%d.%m.%Y')}**)

        **Darlehensphase:**
        - Fester Sollzins: **{darlehenszins:.2f}%**
        - Zins- und Tilgungsrate: **{zins_tilgung}‰** der Bausparsumme
        - Laufzeit des Darlehens: **{laufzeit_darlehen // 12} Jahre und {laufzeit_darlehen % 12} Monate**
        """"""
    )""""""
""""""
# Hauptrechner""""""
def tarif_rechner(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins):""""""
    st.title(f"🏡 LBS Bausparrechner - {name}")"""""""
""""""
    bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, max_value=500000, step=1000)""""""
    if bausparsumme:""""""
        display_tarif_konditionen(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins, bausparsumme)""""""
        vorschlag_sparrate = bausparsumme * regelsparbeitrag / 1000""""""
        monatlicher_sparbeitrag = st.number_input(""""""
            f"📅 Monatliche Sparrate (Vorschlag: {vorschlag_sparrate:.2f} €, Regelsparbeitrag):","""""""
            min_value=1.0,  # Mindestwert angepasst auf 1 €""""""
            max_value=2000.0,""""""
            value=float(max(1.0, vorschlag_sparrate)),""""""
            step=10.0,""""""
        )""""""
        st.caption("💡 Der Vorschlag basiert auf dem Regelsparbeitrag des gewählten Tarifs.")""""""
""""""
    einmalzahlung = st.number_input("💵 Einmalzahlung (€):", min_value=0.0, step=100.0)""""""
    zuteilungszeit = st.number_input("⏳ Gewünschte Zeit bis zur Zuteilung (in Jahren):", min_value=1.5, max_value=20.0, step=0.5)""""""
""""""
    if st.button("📊 Berechnung starten"):""""""
        with st.spinner("🔄 Berechnung wird durchgeführt..."):""""""
            time.sleep(2)""""""
""""""
        df_anspar = calculate_ansparphase_with_pandas(""""""
            bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung""""""
        )""""""
""""""
        monate_anspar = len(df_anspar)""""""
        zinsen_anspar = df_anspar["Zinsen"].sum()""""""
        angespartes_guthaben = df_anspar["Guthaben"].iloc[-1]""""""
""""""
        if monate_anspar / 12 > zuteilungszeit:""""""
            erforderliche_sparrate = calculate_adjusted_sparrate(""""""
                bausparsumme, abschlussgebuehr, sparzins, jahresentgelt, zuteilungszeit, einmalzahlung""""""
            )""""""
            st.warning(""""""
                f"⚠️ Die gewünschte Zuteilungszeit von **{zuteilungszeit:.1f} Jahren** kann nicht eingehalten werden. """"""""
                f"Tatsächliche Ansparzeit: **{monate_anspar / 12:.1f} Jahre**. """"""""
                f"💡 Um die Zuteilungszeit zu erreichen, müsste Ihre Sparrate auf etwa **{erforderliche_sparrate:.2f} €** erhöht werden.""""""""
            )""""""
""""""
        df_darlehen = calculate_darlehensphase_with_pandas(""""""
            bausparsumme, angespartes_guthaben, darlehenszins, zins_tilgung""""""
        )""""""
        laufzeit_darlehen = len(df_darlehen)""""""
        zins_darlehen = df_darlehen["Zinsen"].sum()""""""
""""""
        st.markdown("## 📋 Ergebnisse")""""""
        st.markdown(""""""
            f"""""""
            ### 🏦 Ansparphase
            - Dauer bis zur Zuteilung: **{monate_anspar // 12} Jahre und {monate_anspar % 12} Monate**
            - Gesamtes Sparguthaben inkl. Einmalzahlung: **{df_anspar['Guthaben'].iloc[-1]:,.2f} €**
            - Insgesamt erhaltene Zinsen: **{zinsen_anspar:,.2f} €**

            ### 💳 Darlehensphase
            - Monatliche Rate (Zins + Tilgung): **{df_darlehen['Tilgung'].iloc[0] + df_darlehen['Zinsen'].iloc[0]:,.2f} €**
            - Gesamte Zinskosten während der Darlehensphase: **{zins_darlehen:,.2f} €**
            - Laufzeit des Darlehens: **{laufzeit_darlehen // 12} Jahre und {laufzeit_darlehen % 12} Monate**
            """"""
        )""""""
""""""
        st.markdown("### 📊 Ansparverlauf")"""""""
        plt.figure(figsize=(10, 5))""""""
        plt.plot(df_anspar["Monat"], df_anspar["Guthaben"], label="Guthaben inkl. Zinsen", color="green")""""""
        plt.axhline(y=bausparsumme * 0.4, color="blue", linestyle="--", label="Mindestsparguthaben (40%)")""""""
        plt.xlabel("Monate")""""""
        plt.ylabel("Guthaben (€)")""""""
        plt.title("Ansparverlauf")"""""""
        plt.legend()""""""
        st.pyplot(plt)""""""
""""""
# Hauptmenü und Tarifauswahl""""""
st.title("🏡 LBS Bausparrechner")""""""
st.markdown("Wählen Sie einen Tarif aus, um die Berechnungen zu starten.")""""""
""""""
tarif = st.radio(""""""
    "Tarif auswählen:",""""""
    ["Classic20 F3", "Sprint22", "Komfort22", "Classic20 F8", "Classic20 Plus F", "Spar25"]""""""
)""""""
""""""
# Tarifdetails und Berechnungen""""""
if tarif == "Classic20 F3":""""""
    tarif_rechner("Classic20 F3", 0.05, 3, 1.6, 0.30, 3.5, 2.25)""""""
elif tarif == "Sprint22":""""""
    tarif_rechner("Sprint22", 0.05, 7, 1.6, 0.30, 6, 1.75)""""""
elif tarif == "Komfort22":""""""
    tarif_rechner("Komfort22", 0.05, 3, 1.6, 0.30, 7, 2.35)""""""
elif tarif == "Classic20 F8":""""""
    tarif_rechner("Classic20 F8", 0.05, 3, 1.6, 0.30, 8, 0.95)""""""
elif tarif == "Classic20 Plus F":""""""
    tarif_rechner("Classic20 Plus F", 0.01, 4, 1.6, 0.30, 5, 1.65)""""""
elif tarif == "Spar25":""""""
    tarif_rechner("Spar25", 0.25, 5, 1.6, 0.30, 6, 4.25)""""""
