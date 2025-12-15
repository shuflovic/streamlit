import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


# --- Configuration ---
st.set_page_config(layout="wide", page_title="My World Journey Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", sep=',')
    # Convert date columns to datetime objects
    df['check in'] = pd.to_datetime(df['check in'], format='%d.%m.%Y')
    df['check out'] = pd.to_datetime(df['check out'], format='%d.%m.%Y')
    # Calculate actual nights from dates (as 'nights' column might be slightly off for partial days)
    df['calculated_nights'] = (df['check out'] - df['check in']).dt.days

    # Clean 'total price of stay' and 'average' columns
    # Replace comma with dot for decimal conversion, then convert to numeric
    # Handle cases where 'total price of stay' might be just "0" and needs to be float "0.00"
    df['total price of stay'] = df['total price of stay'].str.replace(',', '.', regex=False).astype(float)
    df['average'] = df['average'].str.replace(',', '.', regex=False).astype(float)

    # Fill NaN values in 'platform' (e.g., for wild camping, workaway, etc. where it's not explicitly stated)
    df['platform'] = df['platform'].fillna('Other')

    return df

df = load_data()

# --- Calculate Journey Start and End ---
journey_start = df['check in'].min()
journey_end = df['check out'].max()
total_journey_days = (journey_end - journey_start).days

# --- Sidebar Filters ---
st.sidebar.header("Filter Your Journey Data")

# Date Range Filter
min_date = df['check in'].min().date()
max_date = df['check out'].max().date()
date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="DD/MM/YYYY"
)
filtered_df = df[(df['check in'].dt.date >= date_range[0]) & (df['check out'].dt.date <= date_range[1])]

# Country Filter
all_countries = sorted(filtered_df['country'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=all_countries,
    default=all_countries
)
filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]

# Platform Filter
all_platforms = sorted(filtered_df['platform'].unique())
selected_platforms = st.sidebar.multiselect(
    "Select Platforms",
    options=all_platforms,
    default=all_platforms
)
filtered_df = filtered_df[filtered_df['platform'].isin(selected_platforms)]

# --- Main Dashboard Content ---
st.title("My World Journey Dashboard 🌍✈️")

st.markdown("""
Welcome to my personal travel dashboard! Here you can find statistics about my journey around the world,
including days spent, costs, types of accommodation, and more.
""")

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
else:
    st.subheader("Journey Overview (Filtered)")

    # Recalculate overview metrics for the filtered data
    filtered_journey_start = filtered_df['check in'].min()
    filtered_journey_end = filtered_df['check out'].max()
    filtered_total_journey_days = (filtered_journey_end - filtered_journey_start).days if not filtered_df.empty else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Filtered Start", filtered_journey_start.strftime("%d %b %Y") if not filtered_df.empty else "N/A")
    with col2:
        st.metric("Filtered End", filtered_journey_end.strftime("%d %b %Y") if not filtered_df.empty else "N/A")
    with col3:
        st.metric("Filtered Days on Road", f"{filtered_total_journey_days} days")
    with col4:
        total_nights_stay = filtered_df[filtered_df['calculated_nights'] > 0]['calculated_nights'].sum()
        st.metric("Total Nights in Stays", f"{total_nights_stay} nights")

    # Total cost calculation
    total_spent = filtered_df['total price of stay'].sum()
    st.metric("Total Accommodation Cost (Filtered)", f"${total_spent:,.2f}")

    st.subheader("Accommodation & Activities Breakdown (Filtered)")

    # --- Days by Type of Activity (Workaway, Treeplanting, Wild Camping) ---
    st.markdown("### Days by Activity Type")
    activity_days = {
        'Treeplanting': filtered_df[filtered_df['platform'] == 'treeplanting']['calculated_nights'].sum(),
        'Workaway': filtered_df[filtered_df['platform'] == 'workaway']['calculated_nights'].sum(),
        'Wild Camping': filtered_df[filtered_df['platform'] == 'wild camping']['calculated_nights'].sum(),
        'Vipassana': filtered_df[filtered_df['platform'] == 'vipassana']['calculated_nights'].sum(),
        'Transport': filtered_df[filtered_df['accommodation'].str.contains('airport|plane|train|flight|transfer', case=False, na=False, regex=True)]['calculated_nights'].sum()
    }
    # Filter out activities with 0 days for cleaner display
    activity_days = {k: v for k, v in activity_days.items() if v > 0}

    if activity_days:
        activity_df = pd.DataFrame(activity_days.items(), columns=['Activity', 'Days'])
        fig_activities = px.pie(activity_df, values='Days', names='Activity',
                                title='Days Spent on Specific Activities',
                                hole=0.4,
                                color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_activities, use_container_width=True)
    else:
        st.write("No specific activity days recorded for the current filters.")

    # --- Countries Visited ---
    st.markdown("### Countries Visited")
    countries_visited = filtered_df['country'].nunique()
    st.write(f"You have visited **{countries_visited}** unique countries.")

    st.write("List of Countries:")
    st.write(", ".join(filtered_df['country'].unique()))

    # --- Accommodation Platform Usage ---
    st.markdown("### Accommodation Platform Usage")
    platform_counts = filtered_df['platform'].value_counts().reset_index()
    platform_counts.columns = ['Platform', 'Count']
    if not platform_counts.empty:
        fig_platforms = px.bar(platform_counts, x='Platform', y='Count',
                               title='Number of Stays per Platform',
                               labels={'Count': 'Number of Stays'},
                               color='Platform', # Color by platform for distinction
                               color_discrete_sequence=px.colors.qualitative.Light24)
        st.plotly_chart(fig_platforms, use_container_width=True)
    else:
        st.write("No platform usage data for the current filters.")

    # --- Cost Analysis by Country ---
    st.markdown("### Cost Analysis")
    cost_by_country = filtered_df.groupby('country')['total price of stay'].sum().sort_values(ascending=False).reset_index()
    cost_by_country.columns = ['Country', 'Total Cost']
    if not cost_by_country.empty:
        fig_country_cost = px.bar(cost_by_country, x='Country', y='Total Cost',
                                 title='Total Accommodation Cost per Country',
                                 labels={'Total Cost': 'Cost ($)'},
                                 color='Country',
                                 color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_country_cost, use_container_width=True)
    else:
        st.write("No cost data by country for the current filters.")

    # --- Average Daily Cost per Person ---
    st.markdown("### Average Daily Cost per Person")
    # Calculate total cost / total person-nights for a better average
    filtered_df['person_nights'] = filtered_df['calculated_nights'] * filtered_df['person']
    total_person_nights = filtered_df['person_nights'].sum()
    average_daily_cost_overall = filtered_df['total price of stay'].sum() / total_person_nights if total_person_nights > 0 else 0
    st.metric("Overall Average Daily Cost Per Person (Filtered)", f"${average_daily_cost_overall:,.2f}")

    # Average daily cost per person by country (only for non-zero costs and nights)
    avg_daily_cost_country = filtered_df[filtered_df['total price of stay'] > 0].groupby('country').apply(
        lambda x: x['total price of stay'].sum() / (x['calculated_nights'] * x['person']).sum() if (x['calculated_nights'] * x['person']).sum() > 0 else 0
    ).reset_index(name='Avg Daily Cost Per Person')
    avg_daily_cost_country = avg_daily_cost_country[avg_daily_cost_country['Avg Daily Cost Per Person'] > 0] # Filter out 0 averages
    avg_daily_cost_country = avg_daily_cost_country.sort_values(by='Avg Daily Cost Per Person', ascending=False)

    if not avg_daily_cost_country.empty:
        fig_avg_cost_country = px.bar(avg_daily_cost_country, x='Country', y='Avg Daily Cost Per Person',
                                    title='Average Daily Cost Per Person by Country (Filtered)',
                                    labels={'Avg Daily Cost Per Person': 'Cost ($)'},
                                    color='Country',
                                    color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_avg_cost_country, use_container_width=True)
    else:
        st.write("No cost data available for average daily cost per person by country for the current filters.")

    # --- Interactive Map (Conceptual Placeholder) ---
    st.markdown("### Your Journey Across the Globe (Conceptual)")
    st.write("While a real interactive map requires geographical coordinates, imagine your filtered journey paths visualized here!")
    # Placeholder for a world map image
    # Note: For an actual interactive map, you'd integrate libraries like folium or add lat/lon to your data
    st.image("https://raw.githubusercontent.com/streamlit/streamlit-example-app/master/media/world_map_globe.png", caption="Conceptual World Map")


# Instructions to run:
# 1. Save this code as `app.py`
# 2. Make sure `data.txt` is in the same directory
# 3. Run `pip install streamlit pandas plotly`
# 4. In your terminal, run `streamlit run app.py`
