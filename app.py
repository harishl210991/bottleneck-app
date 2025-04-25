import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Streamlit Layout
st.title("Bottleneck Analysis Web App")
st.write("Upload your CSV data to analyze the bottlenecks and get insights.")

# Upload CSV File
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    # Read the uploaded CSV file into a DataFrame
    data = pd.read_csv(uploaded_file)

    # Show the first few rows of the uploaded data
    st.write("### Preview of Uploaded Data:")
    st.dataframe(data.head())

    # Step 1: Convert columns to datetime if necessary (assuming 'Start Time' and 'End Time' columns)
    if 'Start Time' in data.columns and 'End Time' in data.columns:
        data['Start Time'] = pd.to_datetime(data['Start Time'])
        data['End Time'] = pd.to_datetime(data['End Time'])

    # Step 2: Add Duration Column
    data['Duration'] = (data['End Time'] - data['Start Time']).dt.total_seconds()

    # Step 3: Filter Data
    st.write("### Filter Data:")
    start_date = st.date_input('Start date', min_value=data['Start Time'].min().date(), max_value=data['Start Time'].max().date())
    end_date = st.date_input('End date', min_value=data['Start Time'].min().date(), max_value=data['Start Time'].max().date())
    filtered_data = data[(data['Start Time'].dt.date >= start_date) & (data['End Time'].dt.date <= end_date)]

    st.write("Filtered Data:")
    st.dataframe(filtered_data)

    # Step 5: Visualize Bottleneck with a Bar Chart (Summation of Duration)
    st.write("### Bottleneck Analysis Visualization (Bar Chart)")

    # Aggregating the data to calculate the total duration spent at each step
    bottleneck_data = filtered_data.groupby('Step').agg(
        total_duration=('Duration', 'sum'),
        task_count=('ID', 'count')
    ).reset_index()

    # Create the bar chart to visualize the bottlenecks (Total duration)
    fig = px.bar(bottleneck_data, x='Step', y='total_duration', color='Step', 
                 title="Total Duration Spent at Each Step",
                 labels={'total_duration': 'Total Duration (seconds)', 'Step': 'Process Step'})

    # Show the bar chart
    st.plotly_chart(fig)

    # Step 6: Identify the Bottleneck (Step with the longest total duration)
    bottleneck_step = bottleneck_data.loc[bottleneck_data['total_duration'].idxmax()]
    st.write("### Bottleneck Insight:")
    st.write(f"The bottleneck in the process is at the '{bottleneck_step['Step']}' step, with a total duration of {bottleneck_step['total_duration']} seconds.")
else:
    st.warning("Please upload a CSV file to begin the analysis.")
