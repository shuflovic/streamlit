import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("testing")

# Load the data from your CSV file
data = pd.read_csv("data.csv")

# Filtered data from your original code (optional)
filtered_data = data[(data['country'] == 'sweden') & (data['platform'] == 'workaway')]
#st.write("Two countries only")
#st.write(filtered_data)

# ----------------- PIE CHART CODE STARTS HERE -----------------

# 1. Group the data by BOTH 'location' and 'platform' and sum the 'nights'
#   Pass a list of column names to groupby()
location_platform_nights = data.groupby(['location', 'platform'])['nights'].sum()

# 2. Sort the data in descending order and select the top 5
top_5_combinations = location_platform_nights.sort_values(ascending=False).head(5)

# 3. Define a function to display the number of nights
def nights_formatter(pct, allvals):
    absolute_nights = int(pct / 100. * sum(allvals))
    return f"{absolute_nights} nights"

# 4. Create the pie chart
fig, ax = plt.subplots()
ax.pie(
    top_5_combinations,
    # The labels will be a combination of location and platform
    labels=top_5_combinations.index.map(lambda x: f"{x[0]} ({x[1]})"),
    autopct=lambda pct: nights_formatter(pct, top_5_combinations),
    pctdistance=0.7
)
ax.axis('equal')  # Ensures the pie chart is a circle

st.write("Top 5 Accommodations (by Nights):")
# Use st.pyplot() to display the Matplotlib chart
st.pyplot(fig)

# ----------------- PIE CHART CODE ENDS HERE -----------------

# Create a new column for top 5 countries
# ----------------- NEW CODE FOR COUNTRY COLUMN STARTS HERE -----------------

st.write("Top 5 Countries (by Nights):")

# 1. Group the data by 'country' and sum the 'nights'
country_nights = data.groupby('country')['nights'].sum()

# 2. Sort the data in descending order and select the top 5
top_5_countries = country_nights.sort_values(ascending=False).head(5)

# 3. Convert the sorted Series to a DataFrame for display
top_5_countries_df = top_5_countries.reset_index()
top_5_countries_df.columns = ['Country', 'Nights']

# 4. Display the DataFrame
st.dataframe(top_5_countries_df)

# ----------------- NEW CODE FOR COUNTRY COLUMN ENDS HERE -----------------
