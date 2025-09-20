import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("testing")

# Load the data from your CSV file
data = pd.read_csv("data.csv")

# Create two columns
col1, col2 = st.columns(2)

# ----------------- PIE CHART CODE STARTS HERE (in the first column) -----------------
with col1:
    st.write("Top 5 Accommodations (by Nights):")

    # 1. Group the data by BOTH 'location' and 'platform' and sum the 'nights'
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
    ax.axis('equal')  # Ensures the pie chart is a circle

    # Use st.pyplot() to display the Matplotlib chart
    st.pyplot(fig)

# ----------------- PIE CHART CODE ENDS HERE -----------------

# ----------------- NEW CODE FOR COUNTRY COLUMN STARTS HERE (in the second column) -----------------
with col2:
    st.write("Top 5 Accommodations (by Nights) Table:")

    # 1. Group by BOTH 'location' and 'platform' and sum the 'nights'
    top_accommodations_df = data.groupby(['location', 'platform'])['nights'].sum().reset_index()

    # 2. Sort the data in descending order and select the top 5
    top_accommodations_df = top_accommodations_df.sort_values('nights', ascending=False).head(5)
    
    # 3. Rename columns for a cleaner display
    top_accommodations_df.columns = ['Accommodation', 'Platform', 'Nights']

    # 4. Display the DataFrame
    st.dataframe(top_accommodations_df)

# ----------------- NEW CODE FOR COUNTRY COLUMN ENDS HERE -----------------
