import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="DataGPT Bottleneck Finder", layout="centered")

st.title("🔍 Bottleneck Detector")
st.markdown("Upload your CSV file with process steps and timestamps to find delays.")

# File upload
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Preview of Uploaded Data")
    st.dataframe(df.head())

    # Minimal checks for expected columns
    expected_columns = ['ID', 'Step', 'Timestamp']
    if not all(col in df.columns for col in expected_columns):
        st.error("CSV must contain 'ID', 'Step', and 'Timestamp' columns.")
    else:
        # Convert timestamp to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df.sort_values(by=['ID', 'Timestamp'])

        # Calculate time difference between steps
        df['Time_Diff'] = df.groupby('ID')['Timestamp'].diff().dt.total_seconds() / 60  # in minutes

        # Find average time per step
        step_delay = df.groupby('Step')['Time_Diff'].mean().sort_values(ascending=False).reset_index()

        st.subheader("⏱️ Average Delay by Step (minutes)")
        st.dataframe(step_delay)

        # Highlight top bottleneck
        top_bottleneck = step_delay.iloc[0]
        st.subheader("🚨 Bottleneck Insight")
        st.success(f"The step with the highest average delay is **{top_bottleneck['Step']}** "
                   f"with an average delay of **{top_bottleneck['Time_Diff']:.2f} minutes**.")

        # Download processed CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Analyzed Data", csv, "analyzed_data.csv", "text/csv")
