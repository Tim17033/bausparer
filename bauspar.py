import streamlit as st
from datetime import datetime, timedelta

def display_tarif_konditionen(name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, regelsparzeit, sollzins):
    regelsparzeit_jahre = int(regelsparzeit)
    regelsparzeit_monate = int((regelsparzeit - regelsparzeit_jahre) * 12)
    regelsparzeit_datum = datetime.now() + timedelta(days=(regelsparzeit_jahre * 365 + regelsparzeit_monate * 30))
    regelsparzeit_datum_formatiert = regelsparzeit_datum.strftime("%d.%m.%Y")

    st.markdown(f"## Tarifkonditionen – {name}")
    st.markdown("### Ansparphase:")
    st.write(f"- **Sparzins**: {sparzins:.2%}")
    st.write(f"- **Monatlicher Regelsparbeitrag**: {regelsparbeitrag}‰ der Bausparsumme")
    st.write(f"- **Abschlussgebühr**: {abschlussgebuehr:.2%} der Bausparsumme")
    st.write(f"- **Jahresentgelt**: {jahresentgelt:.2f} € pro 1.000 € Bausparsumme (max. 30 € pro Jahr)")
    st.write(f"- **Zuteilungszeit bei Regelsparbeitrag**: {regelsparzeit_jahre} Jahre und {regelsparzeit_monate} Monate (ca. {regelsparzeit_datum_formatiert})")

    st.markdown("### Darlehensphase:")
    st.write(f"- **Fester Sollzins**: {sollzins:.2%}")
    st.write(f"- **Monatliche Zins- und Tilgungsrate**: {regelsparbeitrag:.1f}‰ der Bausparsumme")

# Hauptcode
st.title("LBS Bausparrechner")

# Tarifauswahl
st.markdown("### Wähle einen Tarif:")
tarif = st.radio("Verfügbare Tarife:", ["Classic20 F3", "Sprint22", "Komfort22", "Classic20 F8", "Classic20 Plus F", "Spar25"])

# Tarifdaten
if tarif == "Classic20 F3":
    tarif_name = "Classic20 F3"
    sparzins = 0.05
    regelsparbeitrag = 3
    abschlussgebuehr = 1.6
    jahresentgelt = 0.30
    regelsparzeit = 11.25  # 11 Jahre und 3 Monate
    sollzins = 2.25
elif tarif == "Sprint22":
    tarif_name = "Sprint22"
    sparzins = 0.05
    regelsparbeitrag = 7
    abschlussgebuehr = 1.6
    jahresentgelt = 0.30
    regelsparzeit = 6.00  # 6 Jahre
    sollzins = 1.75
# Weitere Tarife hinzufügen...

# Tarifkonditionen anzeigen
display_tarif_konditionen(tarif_name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, regelsparzeit, sollzins)

# Eingabefelder
st.markdown("### Geben Sie Ihre Daten ein:")
bausparsumme = st.number_input("💰 Bausparsumme (€):", min_value=10000, step=1000)
einmalzahlung = st.number_input("💵 Einmalzahlung (€):", min_value=0, step=500)
monatl_sparrate = st.number_input(f"📅 Monatliche Sparrate (Vorschlag: {regelsparbeitrag / 10 * bausparsumme:.2f} €, Regelsparbeitrag):", min_value=0.0, step=10.0)
gew_zuteilung = st.number_input("⏳ Gewünschte Zeit bis zur Zuteilung (in Jahren):", min_value=1.0, step=0.5)

# Berechnung starten
if st.button("Berechnung starten"):
    with st.spinner("Berechnung wird durchgeführt..."):
        regelsparzeit_jahre = int(regelsparzeit)
        regelsparzeit_monate = int((regelsparzeit - regelsparzeit_jahre) * 12)
        regelsparzeit_datum = datetime.now() + timedelta(days=(regelsparzeit_jahre * 365 + regelsparzeit_monate * 30))
        regelsparzeit_datum_formatiert = regelsparzeit_datum.strftime("%d.%m.%Y")

        # Logik für Zuteilung und Lösungsvorschlag
        if gew_zuteilung < regelsparzeit:
            st.warning(
                f"Die gewünschte Zuteilungszeit von **{gew_zuteilung} Jahren** kann nicht eingehalten werden. "
                f"Die tatsächliche Ansparzeit beträgt **{regelsparzeit_jahre} Jahre und {regelsparzeit_monate} Monate** "
                f"(ca. {regelsparzeit_datum_formatiert}). "
                f"💡 Um die Zuteilungszeit zu erreichen, müsste Ihre monatliche Sparrate erhöht werden."
            )
        else:
            st.success(
                f"Die Zuteilungszeit von **{gew_zuteilung} Jahren** kann eingehalten werden! "
                f"Ihre aktuelle Sparrate ist ausreichend. 🎉"
            )














