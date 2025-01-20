import streamlit as st
import time

# Funktionsdefinition für jeden Tarifrechner
def tarif_rechner(name, sparzins, regelsparbeitrag, mindestsparung, mindestsparzeit, abschlussgebuehr, jahresentgelt, darlehenszins, zins_tilgung):
    st.title(f"🏠 LBS Bausparrechner – {name}")

    # Ansparphase
    st.markdown("### 🏦 Ansparphase")
    st.markdown(f"- **Sparzins:** {sparzins}% p.a.")
    st.markdown(f"- **Regelsparbeitrag:** {regelsparbeitrag}‰ der Bausparsumme")
    st.markdown(f"- **Mindestsparung:** {mindestsparung}% der Bausparsumme")
    st.markdown(f"- **Mindestsparzeit:** {mindestsparzeit}")
    st.markdown(f"- **Abschlussgebühr:** {abschlussgebuehr}% der Bausparsumme")
    st.markdown(f"- **Jahresentgelt:** {jahresentgelt} € pro Jahr pro 1.000 € Bausparsumme (max. 30 €)")

    # Darlehensphase
    st.markdown("### 💳 Darlehensphase")
    st.markdown(f"- **Darlehenszins:** {darlehenszins}% p.a.")
    st.markdown(f"- **Zins- und Tilgungsbeitrag:** {zins_tilgung}‰ der Bausparsumme (monatlich)")

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
        jahresentgelt_betrag = min((bausparsumme / 1000) * jahresentgelt, 30)

        # Ergebnisse anzeigen
        st.markdown("## 📋 Ergebnisse")
        st.markdown(
            f"""
            ### 🏦 Sparphase
            - Monatlicher Regelsparbeitrag: **{monatlicher_sparbeitrag:,.2f} €**
            - Mindestsparguthaben: **{mindestsparguthaben:,.2f} €**
            - Abschlussgebühr: **{abschlussgebuehr_betrag:,.2f} €**
            - Jahresentgelt: **{jahresentgelt_betrag:,.2f} € pro Jahr**
            - Gesamtes Sparguthaben inkl. Einmalzahlung: **{mindestsparguthaben + einmalzahlung:,.2f} €**
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
        jahresentgelt=0.30,
        darlehenszins=2.25,
        zins_tilgung=3.5
    )
elif tarif == "Sprint22":
    tarif_rechner(
        name="Sprint22",
        sparzins=0.05,
        regelsparbeitrag=7,
        mindestsparung=50,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        jahresentgelt=0.30,
        darlehenszins=1.75,
        zins_tilgung=6
    )
elif tarif == "Komfort22":
    tarif_rechner(
        name="Komfort22",
        sparzins=0.05,
        regelsparbeitrag=3,
        mindestsparung=30,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        jahresentgelt=0.30,
        darlehenszins=2.35,
        zins_tilgung=7
    )
elif tarif == "Classic20 F8":
    tarif_rechner(
        name="Classic20 F8",
        sparzins=0.05,
        regelsparbeitrag=3,
        mindestsparung=40,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        jahresentgelt=0.30,
        darlehenszins=0.95,
        zins_tilgung=8
    )
elif tarif == "Classic20 Plus F":
    tarif_rechner(
        name="Classic20 Plus F",
        sparzins=0.01,
        regelsparbeitrag=4,
        mindestsparung=40,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        jahresentgelt=0.30,
        darlehenszins=1.65,
        zins_tilgung=5
    )
elif tarif == "Spar25":
    tarif_rechner(
        name="Spar25",
        sparzins=0.25,
        regelsparbeitrag=5,
        mindestsparung=40,
        mindestsparzeit="1 J. 6 Mo.",
        abschlussgebuehr=1.6,
        jahresentgelt=0.30,
        darlehenszins=4.25,
        zins_tilgung=6
    )





