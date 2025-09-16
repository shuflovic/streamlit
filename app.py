import streamlit as st
import pandas as pd

st.title("CSV File Uploader")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data Preview:")
    st.write(df.head()) # Display the first few rows of the DataFrame

    st.subheader("Data Summary:")
    st.write(df.describe()) # Display a statistical summary of the DataFrame


