# streamlit_app.py

import streamlit as st
import pandas as pd
from fuzzywuzzy import process

# Load dataset
df = pd.read_excel("data_output.xlsx")

st.set_page_config(page_title="Ticket Routing from File", layout="centered")
st.title("📌 Smart Ticket Categorization (From File)")

st.write("Enter a **Short Description** to find the corresponding **Assignment Group** and **Intent Cluster** from the dataset.")

# Input
short_desc = st.text_area("Short Description", placeholder="E.g., VPN not working from home...")

# Search button
if st.button("Get Result"):
    if short_desc.strip():
        # Partial matching using fuzzy search
        choices = df["Short Description"].tolist()
        best_match, score = process.extractOne(short_desc, choices)

        if score > 60:  # threshold for match confidence
            match = df[df["Short Description"] == best_match].iloc[0]
            assignment_group = match["Assignment Group"]
            intent_cluster = match["Intent Cluster"]

            st.subheader("Result Found ✅")
            st.write(f"**Best Match:** {best_match}  _(Score: {score})_")
            col1, col2 = st.columns(2)
            col1.metric("Assignment Group", assignment_group)
            col2.metric("Intent Cluster", intent_cluster)
        else:
            st.error("❌ No close match found in the dataset.")
    else:
        st.warning("⚠️ Please enter a short description.")

# Footer
st.markdown("---")
st.caption("Data source: data_output.xlsx")
