
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Επόμενη Κράτηση", layout="centered")
st.title("📅 Επόμενη Κράτηση Βίλας")

uploaded_file = st.file_uploader("📂 Ανέβασε αρχείο Excel με κρατήσεις", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Μετατροπή ημερομηνίας check-in σε datetime
        df['Check-in'] = pd.to_datetime(df['Check-in'], errors='coerce')
        df = df.dropna(subset=['Check-in'])

        # Φιλτράρισμα μελλοντικών κρατήσεων
        today = pd.to_datetime(datetime.now().date())
        upcoming = df[df['Check-in'] >= today].sort_values(by='Check-in')

        # 🔍 Προσθήκη πεδίου αναζήτησης
        search_name = st.text_input("🔍 Αναζήτηση πελάτη (μέρος του ονόματος):").strip().lower()
        if search_name:
            upcoming = upcoming[upcoming['Όνομα/ονόματα πελάτη/-ών'].str.lower().str.contains(search_name)]

        if not upcoming.empty:
            next_booking = upcoming.iloc[0]
            st.success("🔔 Βρέθηκε η επόμενη κράτηση:")

            st.markdown(f"**👤 Πελάτης:** {next_booking['Όνομα/ονόματα πελάτη/-ών']}")
            st.markdown(f"**🏡 Βίλα:** {next_booking['Τύπος μονάδας']}")
            st.markdown(f"**📅 Check-in:** {next_booking['Check-in'].strftime('%d/%m/%Y')}  ")
            st.markdown(f"**📅 Check-out:** {next_booking['Check-out']}")
            st.markdown(f"**👨‍👩‍👧‍👦 Άτομα:** {int(next_booking['αριθμός ενηλίκων']) + int(next_booking['αριθμός παιδιών']) + int(next_booking['αριθμός βρεφών'])}")
            st.markdown(f"**💶 Ποσό:** {next_booking['Έσοδα'] if pd.notna(next_booking['Έσοδα']) else '—'}")
            st.markdown(f"**🌐 Πλατφόρμα:** {next_booking['Πλατφόρμα']}")
        else:
            st.info("Δεν βρέθηκαν επερχόμενες κρατήσεις με αυτό το όνομα.")

    except Exception as e:
        st.error(f"Σφάλμα κατά την επεξεργασία του αρχείου: {e}")
else:
    st.warning("Παρακαλώ ανέβασε αρχείο .xlsx για να εμφανιστεί η επόμενη κράτηση.")
