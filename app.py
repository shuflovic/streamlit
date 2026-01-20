import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px

# 1. PC CONFIG: Force Wide Mode
st.set_page_config(page_title="tam vonku", layout="wide")

# 2. AGGRESSIVE DARK MODE CSS
# This targets the background of the app, headers, and various containers
st.markdown("""
    <style>
        /* Main background and text */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        
        /* Headers and Titles */
        h1, h2, h3, h4, p {
            color: #ffffff !important;
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #161b22 !important;
        }

        /* Top Bar / Header decoration */
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
            color: white !important;
        }

        /* Dataframe background fix */
        .stDataFrame, div[data-testid="stTable"] {
            background-color: #161b22;
            border-radius: 10px;
        }

        /* Metric widget styling */
        div[data-testid="stMetric"] {
            background-color: #1e2129;
            border: 1px solid #30363d;
            padding: 15px;
            border-radius: 10px;
        }

        /* Force divider color */
        hr {
            border-top: 1px solid #30363d !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. GLOBAL CHART STYLING FOR DARK MODE
plt.style.use('dark_background')
plt.rcParams.update({
    "figure.facecolor": "#0e1117",
    "axes.facecolor": "#0e1117",
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white"
})

st.title("tam vonku - dashboard")

# --- DATA PREP ---
@st.cache_data
def load_and_clean():
    # Accommodation Data
    df = pd.read_csv("data.csv")
    df['average'] = df['average'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)
    df['person'] = df['person'].astype(str).astype(int)
    df['country'] = df['country'].str.title()
    
    # Transport Data
    dfT = pd.read_csv("data_transport.csv")
    dfT['price'] = dfT['price per person ( EUR )'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)
    return df, dfT

data, dataT = load_and_clean()

# --- ROW 1: 3 COLUMNS OF GRAPHS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Top 5 Nights")
    loc_nights = data.groupby(['location', 'platform'])['nights'].sum().sort_values(ascending=False).head(5)
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.pie(loc_nights.values, labels=[f"{x[0]}" for x in loc_nights.index], 
            autopct='%1.0f', colors=plt.cm.Pastel2.colors, textprops={'color':"w"})
    st.pyplot(fig1)

with col2:
    st.subheader("Price per Person (€)")
    top_price = data.groupby(['location'])['average'].max().sort_values(ascending=False).head(5)
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.barh(top_price.index, top_price.values, color='#00d4ff')
    ax2.invert_yaxis()
    st.pyplot(fig2)

with col3:
    st.subheader("Stay Breakdown")
    activity_days = {
        'Volunteer': data[data['platform'].str.contains('work|tree', case=False, na=False)]['nights'].sum(),
        'Paid': data[data['platform'].str.contains('booking|airb|stf', case=False, na=False)]['nights'].sum(),
        'Other': data[data['platform'].str.contains('home|friend|vipassana', case=False, na=False)]['nights'].sum()
    }
    fig3 = px.pie(values=list(activity_days.values()), names=list(activity_days.keys()), hole=0.4, 
                 template="plotly_dark")
    fig3.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="white"
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- ROW 2: 3 COLUMNS OF DATA ---
dcol1, dcol2, dcol3 = st.columns(3)

with dcol1:
    st.markdown("### 🏠 Accommodation")
    st.dataframe(data[['country', 'location', 'nights']].sort_values('nights', ascending=False).head(10), 
                 hide_index=True, use_container_width=True)

with dcol2:
    st.markdown("### ✈️ Flights")
    flights = dataT[dataT['type of transport'] == 'flight']
    st.metric("Total Airfare", f"{flights['price'].sum():.2f} €")
    st.dataframe(flights[['from', 'to', 'price']], hide_index=True, use_container_width=True)

with dcol3:
    st.markdown("### 🌍 Countries")
    data['nights_adj'] = (data['nights'] / 2) * data['person']
    country_sum = data.groupby('country')['nights_adj'].sum().reset_index()
    st.dataframe(country_sum.sort_values('nights_adj', ascending=False), 
                 hide_index=True, use_container_width=True)

st.divider()

# --- ROW 3: FULL WIDTH MAP ---
st.subheader("Flight Route Visualization")
# Using Dark Tiles for the Map
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
# ... Add your markers and lines here ...
st_folium(m, width=1600, height=500)
