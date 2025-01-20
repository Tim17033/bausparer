import streamlit as st
import time

# Funktionsdefinition für jeden Tarifrechner
def tarif_rechner(name, sparzins, regelsparbeitrag, mindestsparung, mindestsparzeit, abschlussgebuehr, zins_tilgung, max_darlehensanspruch):
    st.title(f"🏠 LBS Bausparrechner – {name}")
    st.markdown(f"**Sparzins:** {sparzins}% p.a.")
    st.markdown(f"**Regelsparbeitrag:** {regelsparbeitrag}‰ der Bausparsumme")
    st.markdown(f"**Mindestsparung:** {mindestsparung}% der Bausparsumme")
    st.markdown(f"**Mindestsparzeit:** {mindestsparzeit}")
    st.markdown(f"**Abschlussgebühr:** {abschlussgebuehr}% der Bausparsumme")
    st.markdown(f"**Zins- und Tilgungsbeitrag:** {zins_tilgung}‰ der Bausparsumme (monatlich)")
    st.markdown(f"**Maximaler Darlehensanspruch:** {max_darlehensanspruch}% der Bausparsumme")

    # Eingaben für den spezifischen Tarif
    bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, max_value=500000, step=1000)
    einmalzahlung = st.number_input("💵 Einmalzahlung zu Beginn (€):", min_value=0, step=100)

    # Berechnung starten
    if st.button("📊 Berechnung starten"):
        with st.spinner("🔄 Berechnung wird durchgeführt..."):
            time.sleep(2)  # Simulierte Ladezeit

        # Berechnungen
        monatlicher_sparbeitrag = bausparsumme * regelsparbeitrag / 1000
        mindestsparguthaben = bausparsumme * mindestsparung / 100
        abschlussgebuehr_betrag = bausparsumme * abschlussgebuehr / 100

        # Ergebnisse anzeigen
        st.markdown("## 📋 Ergebnisse")
        st.markdown(
            f"""
            ### 🏦 Sparphase
            - Monatlicher Regelsparbeitrag: **{monatlicher_sparbeitrag:,.2f} €**
            - Mindestsparguthaben: **{mindestsparguthaben:,.2f} €**
            - Abschlussgebühr: **{abschlussgebuehr_betrag:,.2f} €**
            - Gesamtes Sparguthaben inkl. Einmalzahlung: **{mindestsparguthaben + einmalzahlung:,.2f} €**

            ### 💳 Darlehensphase
            - Maximaler Darlehensanspruch: **{bausparsumme * max_darlehensanspruch / 100:,.2f} €**
            """
        )

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

# Tarif-Bedingungen und spezifische Berechnungen
if tarif == "Classic20 F3":
    tarif_rechner(
        name="Classic20 F3",
        sparzins=0.05,
        regelsparbeitrag=3,
        mindestsparung=40,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        zins_tilgung=3.5,
        max_darlehensanspruch=60
    )
elif tarif == "Sprint22":
    tarif_rechner(
        name="Sprint22",
        sparzins=0.05,
        regelsparbeitrag=7,
        mindestsparung=50,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        zins_tilgung=6,
        max_darlehensanspruch=50
    )
elif tarif == "Komfort22":
    tarif_rechner(
        name="Komfort22",
        sparzins=0.05,
        regelsparbeitrag=3,
        mindestsparung=30,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        zins_tilgung=7,
        max_darlehensanspruch=70
    )
elif tarif == "Classic20 F8":
    tarif_rechner(
        name="Classic20 F8",
        sparzins=0.05,
        regelsparbeitrag=3,
        mindestsparung=40,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        zins_tilgung=8,
        max_darlehensanspruch=60
    )
elif tarif == "Classic20 Plus F":
    tarif_rechner(
        name="Classic20 Plus F",
        sparzins=0.01,
        regelsparbeitrag=4,
        mindestsparung=40,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        zins_tilgung=5,
        max_darlehensanspruch=60
    )
elif tarif == "Spar25":
    tarif_rechner(
        name="Spar25",
        sparzins=0.25,
        regelsparbeitrag=5,
        mindestsparung=40,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        zins_tilgung=6,
        max_darlehensanspruch=60
    )


