import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("testing")

# Load the data from your CSV file
data = pd.read_csv("data.csv")

# Filtered data from your original code (optional, you can remove this if you only want the chart)
filtered_data = data[(data['country'] == 'sweden') & (data['platform'] == 'workaway')]
st.write("Two countries only")
st.write(filtered_data)

# ----------------- PIE CHART CODE STARTS HERE -----------------

# Group the data by 'location' and sum the 'nights'
location_nights = data.groupby('location')['nights'].sum()

# Create the pie chart
fig, ax = plt.subplots()
ax.pie(location_nights, labels=location_nights.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Ensures the pie chart is a circle

st.write("Nights Spent per Location:")
# Use st.pyplot() to display the Matplotlib chart in Streamlit
st.pyplot(fig)

# ----------------- PIE CHART CODE ENDS HERE -----------------

st.write("All data:")
st.write(data)
