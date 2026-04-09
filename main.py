import streamlit as st
import pandas as pd
from modules.processor import process_data

# Title
st.title("FitSync - Personal Health Analytics")

# Sidebar filter
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["last 7 days", "last 30 days", "all time"],
    index=2
)

# Load data
df = process_data()

if df is not None:

    # Normalize column names: strip spaces and lowercase for consistent referencing
    df.columns = df.columns.str.strip().str.lower()

    # Show columns for debugging (remove this line once confirmed)
    # st.write("Columns in data:", list(df.columns))

    # Handle date column safely (lowercase)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ascending=False)

        if time_range == "last 7 days":
            df = df.head(7)
        elif time_range == "last 30 days":
            df = df.head(30)
    else:
        st.warning("⚠️ No 'date' column found. Showing all data.")

    # Columns layout for metrics
    col1, col2, col3 = st.columns(3)

    # Use safe access with fallback for missing columns
    with col1:
        if 'steps' in df.columns:
            st.metric(label="Average Steps", value=int(df['steps'].mean()))
        else:
            st.metric(label="Average Steps", value="N/A")

    with col2:
        if 'sleep_hours' in df.columns:
            st.metric(label="Average Sleep Hours", value=round(df['sleep_hours'].mean(), 1))
        else:
            st.metric(label="Average Sleep Hours", value="N/A")

    with col3:
        if 'recovery_score' in df.columns:
            st.metric(label="Average Recovery Score", value=round(df['recovery_score'].mean(), 1))
        else:
            st.metric(label="Average Recovery Score", value="N/A")

else:
    st.error("Error loading data.")

# Table showing the full data
st.write("## Processed Health Data")
st.dataframe(df)