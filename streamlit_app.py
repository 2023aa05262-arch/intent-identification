# streamlit_app.py
import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

@st.cache_data
def load_data():
    return pd.read_excel("data_output.xlsx")

df = load_data()

st.set_page_config(page_title="Ticket Routing from File", layout="centered")
st.title("📌 Smart Ticket Categorization (From File)")
st.write("Enter a **Short Description** to find the closest match in the dataset.")

short_desc = st.text_area("Short Description", placeholder="E.g., VPN not working from home...")

CONFIDENCE_THRESHOLD = 60  # tune as you like

if st.button("Get Result"):
    if short_desc.strip():
        choices = df["Short Description"].astype(str).tolist()
        # rapidfuzz returns (match, score, index)
        best_match, score, idx = process.extractOne(
            short_desc, choices, scorer=fuzz.WRatio
        )
        if score >= CONFIDENCE_THRESHOLD:
            row = df.iloc[idx]
            st.subheader("Result Found ✅")
            st.write(f"**Best Match:** {best_match}  _(Score: {int(score)})_")
            c1, c2 = st.columns(2)
            c1.metric("Assignment Group", str(row["Assignment Group"]))
            c2.metric("Intent Cluster", str(row["Intent Cluster"]))
        else:
            st.error("❌ No close match found in the dataset.")
    else:
        st.warning("⚠️ Please enter a short description.")
