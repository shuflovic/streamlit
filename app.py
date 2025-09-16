import streamlit as st
import pandas as pd

st.title("CSV File Uploader")


data = pd.read_csv("data.csv")
st.write("data")
