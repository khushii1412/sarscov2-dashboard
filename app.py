
import streamlit as st
import pandas as pd

st.title("🧬 SARS-CoV-2 Variant Monitoring Dashboard")

df = pd.read_csv('top_200_confident_high_risk.csv')
st.write(df.head())
