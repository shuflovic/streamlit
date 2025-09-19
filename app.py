import streamlit as st
import pandas as pd

st.title("testing")

data = pd.read_csv("data.csv")

sweden_data = data[data['country'] == 'Sweden']

st.write("sweden only")
st.write(sweden_data)

st.write("all data")
st.write(data)


    
