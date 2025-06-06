import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SARS-CoV-2 Mutation Dashboard", layout="wide")

# ---------- Sidebar ----------
st.sidebar.title("🧪 Mutation Dashboard Controls")

uploaded_file = st.sidebar.file_uploader("📁 Upload Nextclade CSV", type="csv")
show_spike_plot = st.sidebar.checkbox("🧬 Show Spike Mutation Position Map", value=True)

# VOC mutation signatures
VOC_MUTATIONS = {
    "Alpha": {"S:N501Y"},
    "Beta": {"S:N501Y", "S:E484K", "S:K417N"},
    "Gamma": {"S:N501Y", "S:E484K", "S:K417T"},
    "Delta": {"S:L452R", "S:T478K", "S:D614G"},
    "Omicron": {"S:N501Y", "S:E484A", "S:D614G", "S:K417N"}
}

VOC_COLORS = {
    "Alpha": "green",
    "Beta": "blue",
    "Gamma": "orange",
    "Delta": "red",
    "Omicron": "purple",
    "Other/Unclassified": "gray"
}

st.title("🧬 SARS-CoV-2 Variant Monitoring Dashboard")

if uploaded_file:
    df = pd.read_csv(uploaded_file, sep=";")
    df["aaSubstitutions"] = df["aaSubstitutions"].fillna("").astype(str)
    df["Mutations"] = df["aaSubstitutions"].str.split(",")

    # Risk scoring
    high_risk_set = {"S:N501Y", "S:E484K", "S:L452R", "S:T478K", "S:D614G"}
    df["risk_score"] = df["Mutations"].apply(lambda muts: sum(m in high_risk_set for m in muts))

    # VOC classification
    def classify_variant(mutations):
        for variant, signature in VOC_MUTATIONS.items():
            if signature.issubset(set(mutations)):
                return variant
        return "Other/Unclassified"

    df["Predicted_Variant"] = df["Mutations"].apply(classify_variant)

    # ---------------------
    st.subheader("📄 Full Annotated Table")
    st.dataframe(df[["seqName", "Nextclade_pango", "clade", "risk_score", "Predicted_Variant", "aaSubstitutions"]])

    # ---------------------
    st.subheader("📊 Most Common Mutations")
    mutation_series = df["Mutations"].explode()
    top_mutations = mutation_series.value_counts().head(20)
    st.bar_chart(top_mutations)

    # ---------------------
    st.subheader("🧬 Variant Alert Table (Color Coded)")
    variant_counts = df["Predicted_Variant"].value_counts()
    for variant, count in variant_counts.items():
        st.markdown(f"- <span style='color:{VOC_COLORS[variant]}'><b>{variant}</b></span>: {count} sequences", unsafe_allow_html=True)

    # ---------------------
    st.subheader("🔍 Filter by Mutation")
    mutation_choice = st.selectbox("Choose a mutation", top_mutations.index)
    filtered_df = df[df["Mutations"].apply(lambda muts: mutation_choice in muts)]

    st.write(f"Showing {len(filtered_df)} sequences with mutation: **{mutation_choice}**")
    st.dataframe(filtered_df[["seqName", "clade", "Nextclade_pango", "risk_score", "Predicted_Variant", "aaSubstitutions"]])

    csv_download = filtered_df.to_csv(index=False)
    st.download_button(
        "💾 Download Filtered CSV",
        data=csv_download,
        file_name=f"filtered_{mutation_choice}.csv",
        mime="text/csv"
    )

    # ---------------------
    if show_spike_plot:
        st.subheader("📌 Spike Protein Mutation Map (Positions)")
        spike_mutations = mutation_series[mutation_series.str.startswith("S:")]
        spike_positions = spike_mutations.index.str.extract(r"S:(\D+)?(\d+)")[1].dropna().astype(int)
        counts = spike_positions.value_counts().sort_index()

        plt.figure(figsize=(12, 3))
        plt.bar(counts.index, counts.values, width=5)
        plt.xlabel("Spike Position")
        plt.ylabel("Mutation Count")
        plt.title("Spike Protein Mutation Hotspots")
        st.pyplot(plt)

else:
    st.info("Upload a `.csv` from Nextclade in the sidebar to begin.")
