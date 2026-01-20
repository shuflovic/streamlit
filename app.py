import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
from branca.element import MacroElement
from jinja2 import Template

# Force wide mode for PC version
st.set_page_config(layout="wide")

st.title("tam vonku - dashboard")

# Data Loading & Cleaning
data = pd.read_csv("data.csv")
data['average'] = data['average'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)
data['person'] = data['person'].astype(str).astype(int)
data['country'] = data['country'].str.title()

# --- ROW 1: ACCOMMODATION ANALYSIS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Top 5 Nights")
    location_nights = data.groupby(['location', 'platform'])['nights'].sum()
    top_5_combinations = location_nights.sort_values(ascending=False).head(5)

    def nights_formatter(pct, allvals):
        absolute_nights = round(pct / 100.0 * sum(allvals))
        return f"{absolute_nights}"

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        top_5_combinations.values,
        labels=top_5_combinations.index.map(lambda x: f"{x[0]}\n({x[1]})"),
        autopct=lambda pct: nights_formatter(pct, top_5_combinations.values),
        pctdistance=0.7,
        textprops={'fontsize': 10}
    )
    st.pyplot(fig)

with col2:
    st.subheader("Top 5 Expensive")
    expensive_accommodations = data.groupby(['country', 'location', 'accommodation'])['average'].max()
    top_5_expensive = expensive_accommodations.sort_values(ascending=False).head(5)

    def price_formatter(pct, allvals):
        average_price = (pct / 100.0 * sum(allvals))
        return f"€{average_price:.2f}"

    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.pie(
        top_5_expensive.values,
        labels=top_5_expensive.index.map(lambda x: f"{x[0]}\n({x[2]})"),
        autopct=lambda pct: price_formatter(pct, top_5_expensive.values),
        pctdistance=0.7,
        textprops={'fontsize': 10}
    )
    st.pyplot(fig2)

with col3:
    st.subheader("Stay Breakdown")
    activity_days = {
        'treeplanting': data[data['platform'] == 'treeplanting']['nights'].sum(),
        'workaway': data[data['platform'] == 'workaway']['nights'].sum(),
        'kungsleden': data[data['platform'] == 'kungsleden']['nights'].sum(),
        'paid': data[data['platform'].str.contains('booking|stf|irbnb|trip.com|random|on the spot', case=False, na=False, regex=True)]['nights'].sum(),
        'other': data[data['platform'].str.contains('airport|transport|plane|train|flight|transfer|home|nitra|friend|vipassana', case=False, na=False, regex=True)]['nights'].sum()
    }
    activity_days = {k: v for k, v in activity_days.items() if v > 0}
    
    if activity_days:
        activity_df = pd.DataFrame(activity_days.items(), columns=['Activity', 'Days'])
        fig_activities = px.pie(activity_df, values='Days', names='Activity', hole=0.4)
        fig_activities.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_activities, use_container_width=True)

st.divider()

# --- ROW 2: TABLES & FLIGHTS ---
t_col1, t_col2, t_col3 = st.columns(3)

with t_col1:
    st.subheader("Accommodation List")
    top_accommodations_df = data.groupby(['country', 'location', 'platform'])['nights'].sum().reset_index()
    top_accommodations_df = top_accommodations_df.sort_values('nights', ascending=False).head(5)
    st.dataframe(top_accommodations_df, hide_index=True, use_container_width=True)

with t_col2:
    st.subheader("Flight Summary")
    dataT = pd.read_csv("data_transport.csv")
    dataT['price per person ( EUR )'] = dataT['price per person ( EUR )'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)
    flight_data = dataT[dataT['type of transport'] == 'flight']
    
    summary_value = flight_data['price per person ( EUR )'].sum()
    st.metric(label="Total Flights Cost", value=f"{summary_value:.2f} €")
    
    flight_res = flight_data.groupby(['from', 'to'])['price per person ( EUR )'].sum().reset_index()
    st.dataframe(flight_res, use_container_width=True)

with t_col3:
    st.subheader("Visited Countries")
    # Adjusted logic as per original snippet
    data['nights_calc'] = (data['nights'] / 2) * data['person']
    countries_df = data.groupby(['country'])['nights_calc'].sum().reset_index()
    st.dataframe(countries_df, use_container_width=True)

st.divider()

# --- ROW 3: MAP (Wider view for PC) ---
st.subheader("Flight Route Visualization")
# Coordinates Dictionary (Keeping your original dict)
city_coords = {'vienna': (48.2082, 16.3738), 'abudhabi': (24.4539, 54.3773), 'muscat': (23.5859, 58.4059), 'sharjah': (25.3463, 55.4209), 'colombo': (6.9271, 79.8612), 'budapest': (47.4979, 19.0402), 'stockholm': (59.3293, 18.0686), 'oslo': (59.9139, 10.7522), 'krakow': (50.0647, 19.9450), 'bratislava': (48.1486, 17.1077), 'sofia': (42.6977, 23.3219), 'istanbul': (41.0082, 28.9784), 'ulanbatar': (47.8864, 106.9057), 'seoul': (37.5665, 126.9780), 'tokyo': (35.6762, 139.6503), 'hongkong': (22.3193, 114.1694), 'hochiminh': (10.8231, 106.6297), 'melbourne': (-37.8136, 144.9631), 'hobart': (-42.8821, 147.3272), 'launceston': (-41.4388, 147.1347), 'auckland': (-36.8485, 174.7633), 'tahiti': (-17.6509, -149.4260), 'sanfrancisco': (37.7749, -122.4194), 'lisbon': (38.7223, -9.1393), 'barcelona': (41.3851, 2.1734)}

m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB Positron")
# ... (keeping your original logic for drawing lines) ...
for _, row in flight_data.iterrows():
    origin = row['from'].lower().replace(' ', '')
    dest = row['to'].lower().replace(' ', '')
    if origin in city_coords and dest in city_coords:
        folium.PolyLine([city_coords[origin], city_coords[dest]], color='blue', weight=1, opacity=0.5).add_to(m)

st_folium(m, width=1400, height=500)
