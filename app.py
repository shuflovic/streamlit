import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.express as px
from branca.element import MacroElement  # Fixed import: from branca.element, not folium.features
from jinja2 import Template

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

# Define city coordinates
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
    'seoul': (37.5665, 126.9780),
    'tokyo': (35.6762, 139.6503),
    'hongkong': (22.3193, 114.1694),
    'hochiminh': (10.8231, 106.6297),
    'melbourne': (-37.8136, 144.9631),
    'hobart': (-42.8821, 147.3272),
    'launceston': (-41.4388, 147.1347),
    'auckland': (-36.8485, 174.7633),
    'tahiti': (-17.6509, -149.4260),
    'sanfrancisco': (37.7749, -122.4194),
    'lisbon': (38.7223, -9.1393),
    'barcelona': (41.3851, 2.1734)
}

# Create tabs for list and visualization
third_col1, third_col2 = st.tabs(["List", "Visualization"])

# Load and process flight data
dataT = pd.read_csv(r"c:\Users\pavel\streamlit\streamlit\data_transport.csv")
dataT['price per person ( EUR )'] = dataT['price per person ( EUR )'].astype(str).str.replace('€', '').str.replace(',', '.').astype(float)

with third_col1:
    flight_data = dataT[dataT['type of transport'] == 'flight']
    result = flight_data.groupby(['from', 'to'], sort=False)['price per person ( EUR )'].sum().reset_index()
    summary_value = flight_data['price per person ( EUR )'].sum()
    st.metric(label="All Flights Per Person", value=f"{summary_value:.2f} €")
    result.index = range(1, len(result) + 1)
    st.dataframe(result, use_container_width=True, hide_index=False)

with third_col2:
    st.write("Flight Route Visualization")
    # Create a Folium map centered on the world
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB Positron")

    all_coords = []
    flight_count = 0

    # Function to adjust line if crossing the antimeridian
    def adjust_for_antimeridian(coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        # Normalize longitudes to [-180, 180]
        if lon1 > 180: lon1 -= 360
        if lon2 > 180: lon2 -= 360
        if lon1 < -180: lon1 += 360
        if lon2 < -180: lon2 += 360

        # Check if crossing ±180° longitude
        if abs(lon1 - lon2) > 180:
            # Shift longitudes so the line wraps correctly
            if lon1 > 0:
                lon1 -= 360
            else:
                lon2 -= 360

        return [(lat1, lon1), (lat2, lon2)]

    # Add markers and routes
    for _, row in flight_data.iterrows():
        origin = row['from'].lower().replace(' ', '')
        destination = row['to'].lower().replace(' ', '')

        if origin in city_coords and destination in city_coords:
            flight_count += 1

            # Add origin marker
            folium.Marker(
                location=city_coords[origin],
                popup=f"{row['from']} ({row['price per person ( EUR )']:.2f} EUR)",
                icon=folium.Icon(color='blue', icon='plane-departure', prefix='fa')
            ).add_to(m)

            # Add destination marker
            folium.Marker(
                location=city_coords[destination],
                popup=f"{row['to']} ({row['price per person ( EUR )']:.2f} EUR)",
                icon=folium.Icon(color='red', icon='plane-arrival', prefix='fa')
            ).add_to(m)

            # Draw line, adjusted for antimeridian
            coords = adjust_for_antimeridian(city_coords[origin], city_coords[destination])
            folium.PolyLine(
                locations=coords,
                color='blue',
                weight=2,
                opacity=0.6,
                popup=f"{row['from']} to {row['to']}: {row['price per person ( EUR )']:.2f} EUR"
            ).add_to(m)

            all_coords.extend(coords)
        else:
            st.warning(f"Skipping flight from {row['from']} to {row['to']}: City not found in coordinates.")

    # Adjust map bounds
    if all_coords:
        m.fit_bounds(all_coords)
    else:
        st.error("No valid flight routes to display. Check city names in data_transport.csv.")

    st.write(f"Total flights displayed: {flight_count}")
    st_folium(m, width=700, height=500)

st.title("visited countries")

forth_col1, forth_col2 = st.tabs(["list", "map"])

with forth_col1:
    st.write("list")
    data['nights'] = (data['nights'] / 2) * data['person']
    countries_df = (
        data.groupby(['country'], sort=False)['nights']
        .sum()
        .reset_index()
    ) 
    countries_df.index = range(1, len(countries_df) + 1)
    st.dataframe(countries_df)
with forth_col2:
    st.write("map")

st.divider()

st.title("Type Of Stay - Breakdown")
activity_days = {
      'treeplanting': data[data['platform'] == 'treeplanting']['nights'].sum(),
      'workaway': data[data['platform'] == 'workaway']['nights'].sum(),
      'kungsleden': data[data['platform'] == 'kungsleden']['nights'].sum(),
      'paid accommodation': data[data['platform'].str.contains('booking|stf|irbnb|trip.com|random|on the spot', case=False, na=False, regex=True)]['nights'].sum(),
      'other(transfers, vipassana, home, ..)': data[data['platform'].str.contains('airport|transport|plane|train|flight|transfer|home|nitra|friend|vipassana', case=False, na=False, regex=True)]['nights'].sum()
  }
activity_days = {k: v for k, v in activity_days.items() if v > 0}
  
if activity_days:
      activity_df = pd.DataFrame(activity_days.items(), columns=['Activity', 'Days'])
      activity_df['Activity_with_Days'] = activity_df.apply(lambda row: f"{row['Activity']} - {int(row['Days'])} nights", axis=1)
      
      fig_activities = px.pie(
          activity_df,
          values='Days',
          names='Activity_with_Days',  # Use the new column with activity and days
          title='% Of Days Spent on Specific Activities',
          hole=0.4,
          color_discrete_sequence=px.colors.qualitative.Pastel
      )
      st.plotly_chart(fig_activities, use_container_width=True)
else:
      st.write("No specific activity days recorded for the current filters.")
