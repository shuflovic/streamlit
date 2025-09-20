import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("tam vonku - dashboard")

data = pd.read_csv("data.csv")

col1, col2 = st.columns(2)

with col1:
    st.write("Top 5 Accommodations (by Nights) Pie Chart:")

    location_nights = data.groupby(['location', 'platform'])['nights'].sum()

    top_5_combinations = location_nights.sort_values(ascending=False).head(5)

    def nights_formatter(pct, allvals):
        absolute_nights = int(pct / 100. * sum(allvals))
        return f"{absolute_nights} nights"

    fig, ax = plt.subplots()
    ax.pie(
        top_5_combinations,
        labels=top_5_combinations.index.map(lambda x: f"{x[0]} ({x[1]})"),
        autopct=lambda pct: nights_formatter(pct, top_5_combinations),
        pctdistance=0.7
    )
    ax.axis('equal')  # Ensures the pie chart is a circle

    # Use st.pyplot() to display the Matplotlib chart
    st.pyplot(fig)

with col2:
    st.write("Top 5 Accommodations (by Nights) Table:")

    top_accommodations_df = data.groupby(['country', 'location', 'platform'])['nights'].sum().reset_index()

    top_accommodations_df = top_accommodations_df.sort_values('nights', ascending=False).head(5)
    
    top_accommodations_df.columns = ['Country', 'Accommodation', 'Platform', 'Nights']

    st.dataframe(top_accommodations_df, hide_index=True)

