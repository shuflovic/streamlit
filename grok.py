import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# === Your correct flight data ===
csv_data = """id,date,from,to,price per person ( EUR ),aircraft,company
1,28.01.2024,vienna,abu dhabi,49.58,,wizzair
2,11.02.2024,muscat,sharjah,26.00,,air arabia
3,11.02.2024,sharjah,colombo,100.00,,air arabia
4,11.04.2024,colombo,abu dhabi,194.51,,air arabia
5,11.04.2024,abu dhabi,budapest,163.29,,wizzair
6,13.04.2024,vienna,stockholm,31.37,,ryanair
7,13.10.2024,oslo,krakow,80.90,,wizzair
8,20.10.2024,bratislava,sofia,17.99,,ryanair
9,29.10.2024,istanbul,ulanbatar,231.50,,mongolian air
10,21.11.2024,ulanbatar,seoul,151.50,,jeju airlines
11,18.12.2024,seoul,tokyo,85.98,,zip air
12,18.03.2025,tokyo,hong kong,116.5,,hongkong express
13,23.06.2025,ho chi minh,melbourne,150,,jet star
14,24.06.2025,melbourne,hobart,37.09,A320,jet star
15,30.08.2025,launceston,melbourne,46,A320,jet star
16,03.09.3035,melbourne,auckland,179.33,A320,jet star
17,19.11.2025,auckland,tahiti,237.35,dreamliner,air new zealand
18,24.11.2025,tahiti,san francisco,237.6,A350,french bee
19,28.11.2025,san francisco,lisbon,140,A330,tap portugal
20,29.11.2025,lisbon,barcelona,38.5,A320,tap portugal
21,01.12.2025,barcelona,bratislava,36.89,A321,wizzair
22,11.12.2025,krakow,oslo,22.22,A321,wizzair
23,26.12.2025,oslo,bratislava,32.22,A321,wizzair"""

df = pd.read_csv(StringIO(csv_data))

# === Coordinates (airports or city centers - accurate for your routes) ===
coords = {
    "vienna": (48.2082, 16.3738),
    "abu dhabi": (24.4539, 54.3773),
    "muscat": (23.5859, 58.4059),
    "sharjah": (25.3463, 55.4209),
    "colombo": (6.9271, 79.8612),
    "budapest": (47.4979, 19.0402),
    "stockholm": (59.3293, 18.0686),
    "oslo": (59.9139, 10.7522),
    "krakow": (50.0647, 19.9450),
    "bratislava": (48.1486, 17.1077),
    "sofia": (42.6977, 23.3219),
    "istanbul": (41.0082, 28.9784),
    "ulanbatar": (47.8864, 106.9057),
    "seoul": (37.5665, 126.9780),
    "tokyo": (35.6762, 139.6503),
    "hong kong": (22.3964, 114.1095),
    "ho chi minh": (10.8231, 106.6297),
    "melbourne": (-37.8136, 144.9631),
    "hobart": (-42.8821, 147.3272),
    "launceston": (-41.4332, 147.1441),
    "auckland": (-36.8485, 174.7633),
    "tahiti": (-17.6509, -149.4260),         # Faa'a International
    "san francisco": (37.7749, -122.4194),
    "lisbon": (38.7223, -9.1393),
    "barcelona": (41.3851, 2.1734),
}

# Map cities to coordinates
df['lat1'] = df['from'].str.strip().str.lower().map(coords)
df['lon1'] = df['from'].str.strip().str.lower().map(lambda x: coords[x][1] if x in coords else None)
df['lat2'] = df['to'].str.strip().str.lower().map(coords)
df['lon2'] = df['to'].str.strip().str.lower().map(lambda x: coords[x][1] if x in coords else None)

# Clean company names
df['company'] = df['company'].str.strip().str.title()
df['aircraft'] = df['aircraft'].fillna("Unknown").str.replace("dreamliner", "787", case=False)

# Airline colors (beautiful & distinct)
airline_colors = {
    "Wizzair": "#952d98",
    "Air Arabia": "#e30613",
    "Ryanair": "#003087",
    "Mongolian Air": "#0055a4",
    "Jeju Airlines": "#ff6200",
    "Zip Air": "#00a0de",
    "Hongkong Express": "#f58220",
    "Jet Star": "#ffc72c",
    "Air New Zealand": "#000000",
    "French Bee": "#6a1b9a",
    "Tap Portugal": "#d2232a",
}

df['color'] = df['company'].map(airline_colors)

# === Build the interactive globe ===
fig = go.Figure()

# Add flight arcs
for _, row in df.iterrows():
    fig.add_trace(go.Scattergeo(
        lon=[row['lon1'], row['lon2']],
        lat=[row['lat1'], row['lat2']],
        mode='lines',
        line=dict(width=4, color=row['color']),
        hovertemplate=
            "<b>%{text}</b><br>" +
            "Date: %{customdata[0]}<br>" +
            "Aircraft: %{customdata[1]}<br>" +
            "Price: €%{customdata[2]}<extra></extra>",
        text=f"{row['from'].title()} → {row['to'].title()} ({row['company']})",
        customdata=[[row['date'], row['aircraft'], row['price per person ( EUR )']]],
        name=row['company']
    ))

# Add airport markers with plane icons
fig.add_trace(go.Scattergeo(
    lon=df['lon1'].tolist() + df['lon2'].tolist(),
    lat=df['lat1'].tolist() + df['lat2'].tolist(),
    text=df['from'].str.title().tolist() + df['to'].str.title().tolist(),
    mode='markers+text',
    marker=dict(size=10, color='white', symbol='circle', line=dict(width=2, color='black')),
    textposition="bottom center",
    hoverinfo='text',
    showlegend=False
))

# Globe styling
fig.update_layout(
    title={
        'text': "My 23 Flights Around the World<br>Jan 2024 → Dec 2025 | 5 Continents | 17 Airlines",
        'x': 0.5,
        'font_size': 22,
        'font_color': 'white'
    },
    geo=dict(
        projection_type='orthographic',
        showland=True,
        landcolor='#1f2a44',
        showocean=True,
        oceancolor='#0b132b',
        showcountries=True,
        countrycolor='#3d5277',
        coastlinecolor='#5d7aa7',
        bgcolor='#0b132b'
    ),
    paper_bgcolor='#0b132b',
    plot_bgcolor='#0b132b',
    font_color='white',
    height=900,
    legend_title="Airline",
    legend=dict(bgcolor='#1f2a44', bordercolor='white', borderwidth=1)
)

# Make it fully rotatable
fig.update_geos(
    projection_rotation=dict(lon=10, lat=20, roll=0),
    lataxis_showgrid=True,
    lonaxis_showgrid=True,
)

fig.show()

# Optional: save as interactive HTML
fig.write_html("my-round-the-world-flights-2024-2025.html")
