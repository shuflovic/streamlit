import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("tam vonku - dashboard")

data = pd.read_csv("data.csv")
data['average'] = data['average'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)

st.write("Top 5 Accommodations (by Nights):")
code1, code2 = st.tabs(["pie chart","table"])
with code1:
  
        location_nights = data.groupby(['location', 'platform'])['nights'].sum()
        top_5_combinations = location_nights.sort_values(ascending=False).head(5)
    
        # Formatter for nights
        def nights_formatter(pct, allvals):
            absolute_nights = round(pct / 100.0 * sum(allvals))
            return f"{absolute_nights}"
    
        # Pie chart for nights
        fig, ax = plt.subplots()
        ax.pie(
            top_5_combinations.values,   # FIX: use values, not Series
            labels=top_5_combinations.index.map(lambda x: f"{x[0]} \n({x[1]})"),
            autopct=lambda pct: nights_formatter(pct, top_5_combinations.values),
            pctdistance=0.7,
            textprops={'fontsize': 14} # FIX: Increase font size for readability
        )
        ax.axis('equal')
        st.pyplot(fig)
        st.divider()
                                  
with code2:
        top_accommodations_df = (
            data.groupby(['country', 'location', 'platform'])['nights']
            .sum()
            .reset_index()
        )
        top_accommodations_df = top_accommodations_df.sort_values('nights', ascending=False).head(5)
        top_accommodations_df.columns = ['Country', 'Accommodation', 'Platform', 'Nights']
    
        st.dataframe(top_accommodations_df.style.set_properties(**{'text-align': 'center'}), hide_index=True)
        st.divider()
    
bottom_col1, bottom_col2 = st.tabs(["pie chart","table"])
    
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
            labels=top_5_expensive.index.map(lambda x: f"{x[0]} \n({x[1]} \n{x[2]})"),
            autopct=lambda pct: price_formatter(pct, top_5_expensive.values),
            pctdistance=0.7,
            textprops={'fontsize': 14} # FIX: Increase font size for readability
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
        st.dataframe(top_average_df.style.set_properties(**{'text-align': 'center'}), hide_index=True)

        st.divider()
  
st.title("Flight Tickets")    

third_col1, third_col2 = st.tabs(["list", "vizual"])

dataT = pd.read_csv("data_transport.csv")
dataT['price per person ( EUR )'] = dataT['price per person ( EUR )'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)

with third_col1:
    st.write("Filtered Flight Data")
    flight_data = dataT[dataT['type of transport'] == 'flight']
    result = flight_data.groupby(['from', 'to'], sort=False)['price per person ( EUR )'].mean().reset_index()
    summary_value = flight_data['price per person ( EUR )'].sum()
    summary_row = pd.DataFrame([['Summary', 'All Flights', summary_value]], columns=['from', 'to', 'price per person ( EUR )'])
    result = pd.concat([summary_row, result], ignore_index=True)
    result.index = range(1, len(result) + 1)
    st.dataframe(result, use_container_width=True, hide_index=False)
  
with third_col2:
  st.write("sem pride vizual")
