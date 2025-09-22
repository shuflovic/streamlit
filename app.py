import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from streamlit_folium import st_folium

st.title("tam vonku - dashboard")

data = pd.read_csv("data.csv")
data['average'] = data['average'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)
data['person'] = data['person'].astype(str).astype(int)


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

city_coords = {
    'vienna': (48.2082, 16.3738),
    'abudhabi': (24.4539, 54.3773),
    'muscat': (23.5859, 58.4059),
    'sharjah': (25.3463, 55.4209),
    'colombo': (6.9271, 79.8612),
    'budapest': (47.4979, 19.0402),
    'stockholm': (59.3293, 18.0686),
    'oslo': (59.9139, 10.7522),
    'krakow': (50.0647, 19.9450),
    'bratislava': (48.1486, 17.1077),
    'sofia': (42.6977, 23.3219),
    'istanbul': (41.0082, 28.9784),
    'ulanbatar': (47.8864, 106.9057),
    'seoul': (37.5665, 126.9780),  # Corrected 'soul' to 'seoul'
    'tokyo': (35.6762, 139.6503),  # Corrected 'tokio' to 'tokyo'
    'hongkong': (22.3193, 114.1694),  # Normalized 'hong kong' to 'hongkong'
    'hochiminh': (10.8231, 106.6297),  # Normalized 'ho chi minh' to 'hochiminh'
    'melbourne': (-37.8136, 144.9631),
    'hobart': (-42.8821, 147.3272),
    'launceston': (-41.4388, 147.1347),
    'auckland': (-36.8485, 174.7633)
}


third_col1, third_col2 = st.tabs(["list", "vizual"])
dataT = pd.read_csv("data_transport.csv")
dataT['price per person ( EUR )'] = dataT['price per person ( EUR )'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)

with third_col1:
    flight_data = dataT[dataT['type of transport'] == 'flight']
    result = flight_data.groupby(['from', 'to'], sort=False)['price per person ( EUR )'].sum().reset_index()
    summary_value = flight_data['price per person ( EUR )'].sum()
    st.metric(label="All Flights Per Person", value=f"{summary_value:.2f} €")
    result.index = range(1, len(result) + 1)
    st.dataframe(result, use_container_width=True, hide_index=False)

with third_col2:
    st.write("Visualization")
    # Create a Folium map centered on the average of all coordinates
    m = folium.Map(location=[0, 0], zoom_start=2)
    # Add markers and lines for each flight route
    for _, row in flight_data.iterrows():
        origin = row['from'].lower().replace(' ', '')
        destination = row['to'].lower().replace(' ', '')
        if origin in city_coords and destination in city_coords:
            # Add markers for origin and destination
            folium.Marker(
                location=city_coords[origin],
                popup=f"{row['from']} ({row['price per person ( EUR )']:.2f} EUR)",
                icon=folium.Icon(color='blue')
            ).add_to(m)
            folium.Marker(
                location=city_coords[destination],
                popup=f"{row['to']} ({row['price per person ( EUR )']:.2f} EUR)",
                icon=folium.Icon(color='red')
            ).add_to(m)
            # Add a line connecting origin and destination
            folium.PolyLine(
                locations=[city_coords[origin], city_coords[destination]],
                color='blue',
                weight=2,
                popup=f"{row['from']} to {row['to']}: {row['price per person ( EUR )']:.2f} EUR"
            ).add_to(m)
    # Adjust map to fit all markers
    if not flight_data.empty:
        coords = [city_coords[city.lower().replace(' ', '')] for city in set(flight_data['from']).union(set(flight_data['to'])) if city.lower().replace(' ', '') in city_coords]
        if coords:
            m.fit_bounds(coords)
    # Render the map in Streamlit
                                                                                                       
    st_folium(m, width=700, height=500)

st.title("visited countries")

forth_col1, forth_col2 = st.tabs(["list", "map"])

with forth_col1:
    st.write("list")
    countries_df['nights'] = countries_df['nights'] / 2 * countries_df['person']
    countries_df = (
        data.groupby(['country'], sort=False)['nights']
        .sum()
        .reset_index()
    ) 
    countries_df.index = range(1, len(countries_df) + 1)
    st.dataframe(countries_df)
with forth_col2:
    st.write("map")
