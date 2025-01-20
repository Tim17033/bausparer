import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# Berechnung der Ansparphase
def calculate_ansparphase(bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung):
    restbetrag = -abschlussgebuehr  # Anfangswert: Abschlussgebühr
    monate = 0
    zinsen_gesamt = 0
    guthaben_verlauf = [restbetrag]

    # Mindestsparguthaben (z. B. 40 % der Bausparsumme)
    mindestsparguthaben = bausparsumme * 0.4

    while restbetrag < mindestsparguthaben:
        zinsen = max(0, restbetrag) * (sparzins / 100 / 12)  # Zinsen nur auf positives Guthaben
        jahresentgelt_betrag = min((bausparsumme / 1000) * jahresentgelt, 30) / 12  # Monatliches Jahresentgelt
        sparbetrag = monatlicher_sparbeitrag - jahresentgelt_betrag
        restbetrag += sparbetrag + zinsen
        zinsen_gesamt += zinsen
        monate += 1
        guthaben_verlauf.append(restbetrag)

    return monate, restbetrag, zinsen_gesamt, guthaben_verlauf

# Berechnung der Darlehensphase
def calculate_darlehensphase(bausparsumme, zins_tilgung, darlehenszins):
    darlehensbetrag = bausparsumme * 0.6
    monatliche_rate = bausparsumme * zins_tilgung / 1000
    restschuld = darlehensbetrag
    monate = 0
    restschuld_verlauf = [restschuld]

    while restschuld > 0:
        zinsen = restschuld * (darlehenszins / 100 / 12)
        tilgung = monatliche_rate - zinsen
        restschuld -= tilgung
        restschuld_verlauf.append(max(0, restschuld))
        monate += 1

    return monate, restschuld_verlauf

# Berechnung der erforderlichen Sparrate für eine gewünschte Zuteilungszeit
def calculate_required_rate(bausparsumme, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung, zuteilungszeit):
    mindestsparguthaben = bausparsumme * 0.4  # 40 % der Bausparsumme
    jahresentgelt_betrag = min((bausparsumme / 1000) * jahresentgelt, 30) * zuteilungszeit  # Jahresentgelt über gesamte Zeit
    zielguthaben = mindestsparguthaben + abschlussgebuehr + jahresentgelt_betrag - einmalzahlung

    # Anzahl der Monate
    monate = zuteilungszeit * 12

    # Berechnung der Sparrate
    r = zielguthaben / (
        monate
        + (monate * (monate + 1) / 2) * (sparzins / 100 / 12)
    )
    return r

# Funktion zur Anzeige der Tarifkonditionen
def show_tarif_details(tarif_name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins):
    st.markdown(f"### Tarifkonditionen – {tarif_name}")
    st.markdown(
        f"""
        **Ansparphase:**
        - Sparzins: **{sparzins:.2f}%**
        - Monatlicher Regelsparbeitrag: **{regelsparbeitrag}‰** der Bausparsumme
        - Abschlussgebühr: **{abschlussgebuehr:.2f}%** der Bausparsumme
        - Jahresentgelt: **{jahresentgelt:.2f} €** pro 1.000 € Bausparsumme (max. 30 € pro Jahr)

        **Darlehensphase:**
        - Fester Sollzins: **{darlehenszins:.2f}%**
        - Zins- und Tilgungsbeitrag: **{zins_tilgung}‰** der Bausparsumme (monatlich)
        """
    )

# Funktionsdefinition für den Tarifrechner
def tarif_rechner(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, zins_tilgung, darlehenszins):
    st.title(f"🏠 LBS Bausparrechner – {name}")

    # Eingaben des Kunden
    bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, max_value=500000, step=1000)
    if bausparsumme:
        # Vorschlag für monatliche Sparrate basierend auf Regelsparbeitrag oder mindestens 50 €
        vorschlag_sparrate = float(max(bausparsumme * regelsparbeitrag / 1000, 50))  
        monatlicher_sparbeitrag = st.number_input(
            f"📅 Monatliche Sparrate (Vorschlag: {vorschlag_sparrate:.2f} €, Regelsparbeitrag):",
            min_value=50.0,  # Minimalwert 50 €
            max_value=2000.0,
            value=vorschlag_sparrate,  # Hier wird der Vorschlag eingebunden
            step=10.0,
        )
        st.caption("💡 Der Vorschlag basiert auf dem Regelsparbeitrag des gewählten Tarifs.")

    einmalzahlung = st.number_input("💵 Einmalzahlung (€):", min_value=0.0, step=100.0)
    zuteilungszeit = st.number_input(
        "⏳ Gewünschte Zeit bis zur Zuteilung (in Jahren):", min_value=1.5, max_value=20.0, step=0.5
    )

    if st.button("📊 Berechnung starten"):
        with st.spinner("🔄 Berechnung wird durchgeführt..."):
            time.sleep(2)  # Simulierte Ladezeit

        # Ansparphase berechnen
        monate_anspar, guthaben, zinsen_anspar, guthaben_verlauf = calculate_ansparphase(
            bausparsumme, monatlicher_sparbeitrag, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung
        )

        # Warnung und Lösungsvorschlag, wenn die gewünschte Zuteilungszeit nicht erreicht wird
        if monate_anspar / 12 > zuteilungszeit:
            required_rate = calculate_required_rate(
                bausparsumme, sparzins, abschlussgebuehr, jahresentgelt, einmalzahlung, zuteilungszeit
            )
            st.warning(
                f"⚠️ Die gewünschte Zuteilungszeit von **{zuteilungszeit} Jahren** kann nicht eingehalten werden. "
                f"Die tatsächliche Ansparzeit beträgt **{monate_anspar / 12:.1f} Jahre**.\n"
                f"💡 Um die Zuteilungszeit zu erreichen, müsste Ihre monatliche Sparrate **{required_rate:.2f} €** betragen."
            )

        # Ergebnisse anzeigen
        st.markdown("## 📋 Ergebnisse")
        st.markdown(
            f"""
            ### 🏦 Ansparphase
            - Dauer bis zur Zuteilung: **{monate_anspar // 12} Jahre und {monate_anspar % 12} Monate**
            - Gesamtes Sparguthaben inkl. Einmalzahlung: **{guthaben:,.2f} €**
            - Insgesamt erhaltene Zinsen: **{zinsen_anspar:,.2f} €**
            """
        )

        # Ansparphase visualisieren
        st.markdown("### 📊 Ansparverlauf")
        plt.figure(figsize=(10, 5))
        plt.plot(np.arange(len(guthaben_verlauf)), guthaben_verlauf, label="Guthaben inkl. Zinsen", color="green")
        plt.axhline(y=bausparsumme * 0.4, color="blue", linestyle="--", label="Mindestsparguthaben (40%)")
        plt.title("Ansparverlauf")
        plt.xlabel("Monate")
        plt.ylabel("Guthaben (€)")
        plt.legend()
        st.pyplot(plt)

# Hauptmenü
st.title("🏠 LBS Bausparrechner")
st.markdown("Wählen Sie einen Tarif aus, um die Berechnungen zu starten.")

# Tarifauswahl
tarif = st.radio(
    "Tarif auswählen:",
    [
        "Classic20 F3",
        "Sprint22",
        "Komfort22",
        "Classic20 F8",
        "Classic20 Plus F",
        "Spar25"
    ]
)

# Tarifdetails und Berechnungen
if tarif == "Classic20 F3":
    show_tarif_details("Classic20 F3", sparzins=0.05, regelsparbeitrag=3, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=3.5, darlehenszins=2.25)
    tarif_rechner("Classic20 F3", sparzins=0.05, regelsparbeitrag=3, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=3.5, darlehenszins=2.25)
elif tarif == "Sprint22":
    show_tarif_details("Sprint22", sparzins=0.05, regelsparbeitrag=7, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=6, darlehenszins=1.75)
    tarif_rechner("Sprint22", sparzins=0.05, regelsparbeitrag=7, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=6, darlehenszins=1.75)
elif tarif == "Komfort22":
    show_tarif_details("Komfort22", sparzins=0.05, regelsparbeitrag=3, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=7, darlehenszins=2.35)
    tarif_rechner("Komfort22", sparzins=0.05, regelsparbeitrag=3, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=7, darlehenszins=2.35)
elif tarif == "Classic20 F8":
    show_tarif_details("Classic20 F8", sparzins=0.05, regelsparbeitrag=3, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=8, darlehenszins=0.95)
    tarif_rechner("Classic20 F8", sparzins=0.05, regelsparbeitrag=3, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=8, darlehenszins=0.95)
elif tarif == "Classic20 Plus F":
    show_tarif_details("Classic20 Plus F", sparzins=0.01, regelsparbeitrag=4, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=5, darlehenszins=1.65)
    tarif_rechner("Classic20 Plus F", sparzins=0.01, regelsparbeitrag=4, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=5, darlehenszins=1.65)
elif tarif == "Spar25":
    show_tarif_details("Spar25", sparzins=0.25, regelsparbeitrag=5, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=6, darlehenszins=4.25)
    tarif_rechner("Spar25", sparzins=0.25, regelsparbeitrag=5, abschlussgebuehr=1.6, jahresentgelt=0.30, zins_tilgung=6, darlehenszins=4.25)
