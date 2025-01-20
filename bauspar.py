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

# Beispielaufruf
tarif_name = "Classic20 F3"
sparzins = 0.05
regelsparbeitrag = 3
abschlussgebuehr = 1.6
jahresentgelt = 0.30
regelsparzeit = 11.25  # 11 Jahre und 3 Monate
sollzins = 2.25

st.title("Bausparrechner")
st.sidebar.radio("Wähle deinen Tarif:", ["Classic20 F3", "Sprint22", "Komfort22", "Classic20 F8", "Classic20 Plus F", "Spar25"])
display_tarif_konditionen(tarif_name, sparzins, regelsparbeitrag, abschlussgebuehr, jahresentgelt, regelsparzeit, sollzins)













