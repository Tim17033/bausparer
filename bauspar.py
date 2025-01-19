import streamlit as st
import time

# Funktionsdefinition für jeden Tarifrechner
def tarif_rechner(name, regelsparbeitrag, mindestsparzeit, bausparsumme=None):
    st.title(f"🏠 LBS Bausparrechner – {name}")
    st.markdown(f"**Regelsparbeitrag:** {regelsparbeitrag}‰")
    st.markdown(f"**Mindestsparzeit:** {mindestsparzeit}")

    # Eingaben für den spezifischen Tarif
    bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, max_value=500000, step=1000)
    einmalzahlung = st.number_input("💵 Einmalzahlung zu Beginn (€):", min_value=0, step=100)
    zinssatz_sparen = st.number_input("📈 Zinsen auf Sparguthaben (% p.a.):", min_value=0.0, max_value=5.0, step=0.1)

    # Berechnung starten
    if st.button("📊 Berechnung starten"):
        with st.spinner("🔄 Berechnung wird durchgeführt..."):
            time.sleep(2)  # Simulierte Ladezeit

        # Beispielhafte Berechnung: Guthaben und Zinsen
        monatliche_rate = bausparsumme * regelsparbeitrag / 1000
        ansparzeit = mindestsparzeit
        zinsen_gesamt = (bausparsumme * zinssatz_sparen / 100 * ansparzeit)

        # Ergebnisse anzeigen
        st.markdown("## 📋 Ergebnisse")
        st.markdown(
            f"""
            ### 🏦 Ansparphase
            - Gesamtes Sparguthaben (inkl. Zinsen): **{bausparsumme + zinsen_gesamt:,.2f} €**
            - Monatlicher Regelsparbeitrag: **{monatliche_rate:,.2f} €**
            - Dauer der Ansparphase: **{ansparzeit} Jahre**

            ### 💵 Einmalzahlung
            - Ihre Einmalzahlung reduziert die benötigte Ansparzeit entsprechend.
            """
        )

# Hauptmenü
st.title("🏠 LBS Bausparrechner")
st.markdown("Bitte wählen Sie einen Tarif aus, um die Berechnung zu starten.")

# Kategorien und Tarife
option = st.selectbox(
    "Kategorie wählen:",
    ["Für Immo kaufen", "Für Modernisierung"]
)

if option == "Für Immo kaufen":
    tarif = st.radio(
        "Tarif auswählen:",
        [
            "Classic20 F3 – Geringer monatlicher Aufwand",
            "Sprint22 – Schnelle Zuteilung und Tilgung",
            "Komfort22 – Jugendbonus, geringer monatlicher Aufwand"
        ]
    )
    if tarif == "Classic20 F3 – Geringer monatlicher Aufwand":
        tarif_rechner("Classic20 F3", regelsparbeitrag=3, mindestsparzeit=11)
    elif tarif == "Sprint22 – Schnelle Zuteilung und Tilgung":
        tarif_rechner("Sprint22", regelsparbeitrag=7, mindestsparzeit=6)
    elif tarif == "Komfort22 – Jugendbonus, geringer monatlicher Aufwand":
        tarif_rechner("Komfort22", regelsparbeitrag=3, mindestsparzeit=8.5)

elif option == "Für Modernisierung":
    tarif = st.radio(
        "Tarif auswählen:",
        [
            "Classic20 F8 – Schnelle Tilgung",
            "Classic20 Plus F – Mittlere Laufzeit"
        ]
    )
    if tarif == "Classic20 F8 – Schnelle Tilgung":
        tarif_rechner("Classic20 F8", regelsparbeitrag=3, mindestsparzeit=11)
    elif tarif == "Classic20 Plus F – Mittlere Laufzeit":
        tarif_rechner("Classic20 Plus F", regelsparbeitrag=4, mindestsparzeit=8.5)

