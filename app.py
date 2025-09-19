import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("testing")

# Load the data from your CSV file
data = pd.read_csv("data.csv")

# Filtered data from your original code (optional)
filtered_data = data[(data['country'] == 'sweden') & (data['platform'] == 'workaway')]
st.write("Two countries only")
st.write(filtered_data)

# ----------------- PIE CHART CODE STARTS HERE -----------------

# 1. Group the data by 'location' and sum the 'nights'
location_nights = data.groupby('location')['nights'].sum()

# 2. Sort the data in descending order and select the top 5
top_5_locations = location_nights.sort_values(ascending=False).head(5)

# 3. Define a function to display the number of nights instead of percentage
def nights_formatter(pct, allvals):
    absolute_nights = int(pct/100.*sum(allvals))
    return f"{absolute_nights} nights"

# 4. Create the pie chart for the top 5 locations
fig, ax = plt.subplots()
ax.pie(
    top_5_locations, 
    labels=top_5_locations.index, 
    autopct=lambda pct: nights_formatter(pct, top_5_locations), 
    pctdistance=0.7 # Adjust the label position
)
ax.axis('equal')  # Ensures the pie chart is a circle

st.write("Top 5 Locations by Nights Spent:")
# Use st.pyplot() to display the Matplotlib chart
st.pyplot(fig)

# ----------------- PIE CHART CODE ENDS HERE -----------------

st.write("All data:")
st.write(data)
