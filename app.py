import streamlit as st
import pandas as pd

st.title("🧬 SARS-CoV-2 Variant Monitoring Dashboard")

uploaded_file = st.file_uploader("Upload your Nextclade CSV", type="csv")

if uploaded_file is not None:
    try:
        # Try reading with semicolon delimiter
        df = pd.read_csv(uploaded_file, sep=";")
        st.success("✅ File uploaded successfully!")
        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        # Display mutation frequency (if aaSubstitutions column exists)
        if "aaSubstitutions" in df.columns:
            st.subheader("🧬 Most Common Amino Acid Substitutions")
            mutation_series = df["aaSubstitutions"].dropna().str.split(",").explode()
            top_mutations = mutation_series.value_counts().head(10)
            st.bar_chart(top_mutations)
        else:
            st.warning("Column 'aaSubstitutions' not found in the uploaded file.")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📁 Please upload a Nextclade `.csv` file to begin.")
