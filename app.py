import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("testing")

data = pd.read_csv("data.csv")

filtered_data = data[(data['country'] == 'sweden') & (data['platform'] == 'workaway') ]


location_nights = data.groupby('location')['nights'].sum()

fig, ax = plt.subplots()
ax.pie(location_nights, labels=location_nights.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Ensures the pie chart is a circle

st.write("Nights Spent per Location:")
st.pyplot(fig)

#st.write("two countries only")
#st.write(filtered_data)

#st.write("all data")
#st.write(data)


    
