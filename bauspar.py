import streamlit as st
import time

# Tarifinformationen
TARIFE = {
    "Classic20 F3": {"regelsparbeitrag": 3, "mindestsparung": 40, "mindestsparzeit": 1.5, "abschlussgebuehr": 1.6, "jahresentgelt": 0.30, "darlehenszins": 2.25, "zins_tilgung": 3.5},
    "Sprint22": {"regelsparbeitrag": 7, "mindestsparung": 50, "mindestsparzeit": 1.5, "abschlussgebuehr": 1.6, "jahresentgelt": 0.30, "darlehenszins": 1.75, "zins_tilgung": 6},
    "Komfort22": {"regelsparbeitrag": 3, "mindestsparung": 30, "mindestsparzeit": 1.5, "abschlussgebuehr": 1.6, "jahresentgelt": 0.30, "darlehenszins": 2.35, "zins_tilgung": 7},
    "Classic20 F8": {"regelsparbeitrag": 3, "mindestsparung": 40, "mindestsparzeit": 1.5, "abschlussgebuehr": 1.6, "jahresentgelt": 0.30, "darlehenszins": 0.95, "zins_tilgung": 8},
    "Classic20 Plus F": {"regelsparbeitrag": 4, "mindestsparung": 40, "mindestsparzeit": 1.5, "abschlussgebuehr": 1.6, "jahresentgelt": 0.30, "darlehenszins": 1.65, "zins_tilgung": 5},
    "Spar25": {"regelsparbeitrag": 5, "mindestsparung": 40, "mindestsparzeit": 1.5, "abschlussgebuehr": 1.6, "jahresentgelt": 0.30, "darlehenszins": 4.25, "zins_tilgung": 6}
}

# Tarifauswahl basierend auf Eingaben
def finde_tarif(bausparsumme, monatliche_rate, zuteilung):
    passende_tarife = []
    for tarif, details in TARIFE.items():
        if monatliche_rate >= bausparsumme * details["regelsparbeitrag"] / 1000 and zuteilung >= details["mindestsparzeit"]:
            passende_tarife.append(tarif)
    return passende_tarife

# Berechnungen für Anspar- und Darlehensphase
def berechnung_tarif(tarif, bausparsumme, einmalzahlung):
    details = TARIFE[tarif]
    monatlicher_sparbeitrag = bausparsumme * details["regelsparbeitrag"] / 1000
    abschlussgebuehr_betrag = bausparsumme * details["abschlussgebuehr"] / 100
    jahresentgelt_betrag = min((bausparsumme / 1000) * details["jahresentgelt"], 30)
    mindestsparguthaben = bausparsumme * details["mindestsparung"] / 100

    return {
        "tarif": tarif,
        "monatlicher_sparbeitrag": monatlicher_sparbeitrag,
        "abschlussgebuehr": abschlussgebuehr_betrag,
        "jahresentgelt": jahresentgelt_betrag,
        "mindestsparguthaben": mindestsparguthaben + einmalzahlung
    }

# App-Start
st.title("🏠 LBS Bausparrechner – Kundenberatung")
st.markdown("Finden Sie den perfekten Tarif für Ihren Kunden basierend auf seinen Bedürfnissen.")

# Fragen an den Kunden
st.markdown("### 🔍 Fragen an den Kunden")
ziel = st.selectbox("Wofür möchten Sie den Bausparer nutzen?", ["Eigenheim", "Modernisierung", "Allgemeines Sparen"])
zuteilung = st.number_input("Wann möchten Sie in die Zuteilung kommen? (in Jahren):", min_value=1.5, step=0.5)
bausparsumme = st.number_input("Wie hoch soll die Bausparsumme sein? (€):", min_value=10000, step=1000)
monatliche_rate = st.number_input("Wie viel können Sie monatlich einzahlen? (€):", min_value=50, step=10)
einmalzahlung = st.number_input("Haben Sie eine Einmalzahlung? (€):", min_value=0, step=100)

# Tarif finden und berechnen
if st.button("📊 Tarif berechnen"):
    with st.spinner("🔄 Wir finden den passenden Tarif..."):
        time.sleep(2)  # Simulierte Ladezeit
    tarife = finde_tarif(bausparsumme, monatliche_rate, zuteilung)
    if tarife:
        st.success(f"Passende Tarife: {', '.join(tarife)}")
        tarif = tarife[0]  # Erster passender Tarif wird gewählt
        ergebnisse = berechnung_tarif(tarif, bausparsumme, einmalzahlung)

        st.markdown("## 📋 Ergebnisse")
        st.markdown(
            f"""
            ### 🏦 Ansparphase ({ergebnisse['tarif']})
            - Monatlicher Sparbeitrag: **{ergebnisse['monatlicher_sparbeitrag']:.2f} €**
            - Abschlussgebühr: **{ergebnisse['abschlussgebuehr']:.2f} €**
            - Jahresentgelt: **{ergebnisse['jahresentgelt']:.2f} €**
            - Gesamtes Sparguthaben inkl. Einmalzahlung: **{ergebnisse['mindestsparguthaben']:.2f} €**
            """
        )
    else:
        st.error("Kein Tarif passt zu den Eingaben. Bitte prüfen Sie die monatliche Rate oder die Zuteilungszeit.")






