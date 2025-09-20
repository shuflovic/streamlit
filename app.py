import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("tam vonku - dashboard")
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")

data = pd.read_csv("data.csv")
data['average'] = data['average'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)

top_col1, top_col2 = st.columns([6,4])

with top_col1:
    st.write("Top 5 Accommodations (by Nights) Pie Chart:")

    # Group and sort
    location_nights = data.groupby(['location', 'platform'])['nights'].sum()
    top_5_combinations = location_nights.sort_values(ascending=False).head(5)

    # Formatter for nights
    def nights_formatter(pct, allvals):
        absolute_nights = round(pct / 100.0 * sum(allvals))
        return f"{absolute_nights} nights"

    # Pie chart for nights
    fig, ax = plt.subplots()
    ax.pie(
        top_5_combinations.values,   # FIX: use values, not Series
        labels=top_5_combinations.index.map(lambda x: f"{x[0]} ({x[1]})"),
        autopct=lambda pct: nights_formatter(pct, top_5_combinations.values),
        pctdistance=0.7
    )
    ax.axis('equal')
    st.pyplot(fig)
                              
with top_col2:
    st.write("Top 5 Accommodations (by Nights) Table:")

    # Create table of top accommodations
    top_accommodations_df = (
        data.groupby(['country', 'location', 'platform'])['nights']
        .sum()
        .reset_index()
    )
    top_accommodations_df = top_accommodations_df.sort_values('nights', ascending=False).head(5)
    top_accommodations_df.columns = ['Country', 'Accommodation', 'Platform', 'Nights']

    st.dataframe(top_accommodations_df, hide_index=True)

st.divider()

bottom_col1, bottom_col2 = st.columns([4,6])

with bottom_col1:
    st.write("Top 5 Most Expensive Accommodations (Price Per Person):")

    expensive_accommodations = data.groupby(['country', 'location', 'accommodation'])['average'].max()
    top_5_expensive = expensive_accommodations.sort_values(ascending=False).head(5)

    # Formatter for price
    def price_formatter(pct, allvals):
        average_price = (pct / 100.0 * sum(allvals))
        return f"€{average_price:.2f}"

    # Pie chart for prices
    fig2, ax2 = plt.subplots()
    ax2.pie(
        top_5_expensive.values,   # FIX: use values, not Series
        labels=top_5_expensive.index.map(lambda x: f"{x[0]} ({x[1]} - {x[2]})"),
        autopct=lambda pct: price_formatter(pct, top_5_expensive.values),
        pctdistance=0.7
    )
    ax2.axis('equal')
    st.pyplot(fig2)
    
with bottom_col2:
    st.write("Top 5 Most Expensive Accommodations (Price Per Person):")

    top_average_df = (
        data.groupby(['country', 'location', 'accommodation'])['average']
        .max()
        .reset_index()
    )
    top_average_df = top_average_df.sort_values('average', ascending=False).head(5)
    top_average_df.columns = ['Country', 'Location', 'Accommodation', 'Average']

    st.dataframe(top_average_df, hide_index=True)
