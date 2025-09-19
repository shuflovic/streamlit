import streamlit as st
import pandas as pd

st.title("testing")

data = pd.read_csv("data.csv")

filtered_data = data[(data['country'] == 'sweden') | (data['platform'] == 'workaway') ]

st.write("two countries only")
st.write(filtered_data)

st.write("all data")
st.write(data)


    
