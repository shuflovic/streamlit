import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("testing")

data = pd.read_csv("data.csv")

filtered_data = data[data['country'] == 'sweden']
st.write("Two countries only")
st.write(filtered_data)

country_nights = data.groupby('country')['nights'].sum()

# Create the pie chart
fig, ax = plt.subplots()
ax.pie(country_nights, labels=country_nights.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Ensures the pie chart is a circle

st.write("Nights Spent per Location:")
# Use st.pyplot() to display the Matplotlib chart in Streamlit
st.pyplot(fig)

# ----------------- PIE CHART CODE ENDS HERE -----------------

st.write("All data:")
st.write(data)
