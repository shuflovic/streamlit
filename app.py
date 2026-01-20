import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px

# 1. FORCE WIDE MODE & SETTINGS
st.set_page_config(page_title="tam vonku", layout="wide", initial_sidebar_state="collapsed")

# 2. INJECT DARK THEME CSS (Forces dark backgrounds and white text)
st.markdown("""
    <style>
        stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stMetric {
            background-color: #1e2129;
            padding: 15px;
            border-radius: 10px;
        }
        /* Style for dataframes in dark mode */
        [data-testid="stTable"] {
            background-color: #1e2129;
        }
    </style>
    """, unsafe_content_allowed=True)

# Helper function for Matplotlib Dark Mode
def set_plt_dark():
    plt.style.use('dark_background')
    plt.rcParams.update({
        "figure.facecolor": "#0e1117",
        "axes.facecolor": "#0e1117",
        "savefig.facecolor": "#0e1117",
    })

set_plt_dark()

st.title("tam vonku - dashboard")

# --- DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    df['average'] = df['average'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)
    df['person'] = df['person'].astype(str).astype(int)
    df['country'] = df['country'].str.title()
    return df

data = load_data()

# --- ROW 1: TOP LEVEL VISUALS (3 COLUMNS) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌙 Top 5 Accommodations")
    location_nights = data.groupby(['location', 'platform'])['nights'].sum()
    top_5 = location_nights.sort_values(ascending=False).head(5)
    
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(top_5.values, labels=[f"{x[0][:10]}.." for x in top_5.index], 
           autopct='%1.0f', startangle=140, colors=plt.cm.Pastel1.colors)
    st.pyplot(fig)

with col2:
    st.subheader("💰 Most Expensive (Avg)")
    expensive = data.groupby(['location'])['average'].max().sort_values(ascending=False).head(5)
    
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.barh(expensive.index, expensive.values, color='#1f77b4')
    ax2.invert_yaxis()
    st.pyplot(fig2)

with col3:
    st.subheader("📊 Activity Breakdown")
    activity_days = {
        'Work': data[data['platform'].str.contains('work|tree', case=False, na=False)]['nights'].sum(),
        'Paid': data[data['platform'].str.contains('booking|airb', case=False, na=False)]['nights'].sum(),
        'Other': data[~data['platform'].str.contains('work|tree|booking|airb', case=False, na=False)]['nights'].sum()
    }
    fig_act = px.pie(values=list(activity_days.values()), names=list(activity_days.keys()), 
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
    fig_act.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_act, use_container_width=True)

st.divider()

# --- ROW 2: DATA TABLES (3 COLUMNS) ---
tab_col1, tab_col2, tab_col3 = st.columns(3)

with tab_col1:
    st.markdown("**Top Stays List**")
    st.dataframe(data[['location', 'nights', 'platform']].sort_values('nights', ascending=False).head(8), 
                 hide_index=True, use_container_width=True)

with tab_col2:
    st.markdown("**Flight Costs**")
    dataT = pd.read_csv("data_transport.csv")
    dataT['price'] = dataT['price per person ( EUR )'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)
    flight_data = dataT[dataT['type of transport'] == 'flight']
    
    st.metric("Total Flight Spend", f"{flight_data['price'].sum():.2f} €")
    st.dataframe(flight_data[['from', 'to', 'price']].head(5), hide_index=True, use_container_width=True)

with tab_col3:
    st.markdown("**Visited Countries**")
    countries = data.groupby('country')['nights'].sum().reset_index()
    st.dataframe(countries.sort_values('nights', ascending=False), hide_index=True, use_container_width=True)

st.divider()

# --- ROW 3: MAP (FULL WIDTH) ---
st.subheader("✈️ Flight Route Map")
city_coords = {'vienna': (48.2082, 16.3738), 'abudhabi': (24.4539, 54.3773), 'muscat': (23.5859, 58.4059), 'sharjah': (25.3463, 55.4209), 'colombo': (6.9271, 79.8612), 'budapest': (47.4979, 19.0402), 'stockholm': (59.3293, 18.0686), 'oslo': (59.9139, 10.7522), 'krakow': (50.0647, 19.9450), 'bratislava': (48.1486, 17.1077), 'sofia': (42.6977, 23.3219), 'istanbul': (41.0082, 28.9784), 'ulanbatar': (47.8864, 106.9057), 'seoul': (37.5665, 126.9780), 'tokyo': (35.6762, 139.6503), 'hongkong': (22.3193, 114.1694), 'hochiminh': (10.8231, 106.6297), 'melbourne': (-37.8136, 144.9631), 'hobart': (-42.8821, 147.3272), 'launceston': (-41.4388, 147.1347), 'auckland': (-36.8485, 174.7633), 'tahiti': (-17.6509, -149.4260), 'sanfrancisco': (37.7749, -122.4194), 'lisbon': (38.7223, -9.1393), 'barcelona': (41.3851, 2.1734)}

# Using a Darker Map Tile
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

for _, row in flight_data.iterrows():
    origin = row['from'].lower().replace(' ', '')
    dest = row['to'].lower().replace(' ', '')
    if origin in city_coords and dest in city_coords:
        folium.PolyLine([city_coords[origin], city_coords[dest]], color='#00d4ff', weight=1, opacity=0.4).add_to(m)

st_folium(m, width=1600, height=500)
