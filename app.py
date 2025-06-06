import streamlit as st
import pandas as pd

st.title("🧬 SARS-CoV-2 Variant Monitoring Dashboard")

uploaded_file = st.file_uploader("Upload your SARS-CoV-2 data (.csv)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Preview of Uploaded Data")
    st.write(df.head())

    st.subheader("📊 Summary")
    st.write(df.describe())

    st.subheader("🧪 Mutation Frequency")
    mutation_cols = [col for col in df.columns if col.startswith("S:")]
    if mutation_cols:
        mutation_summary = df[mutation_cols].sum().sort_values(ascending=False)
        st.bar_chart(mutation_summary)
    else:
        st.warning("No mutation columns found (e.g., columns starting with 'S:').")
else:
    st.info("Please upload a CSV file to begin.")
