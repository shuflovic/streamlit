import streamlit as st
import pandas as pd  # New import for data

# 1. PAGE SETUP
st.set_page_config(
    page_title="tam vonku - dashboard",
    layout="wide"
)

# 2. THEME TOGGLE LOGIC
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

theme_toggle = st.toggle("change mode here", value=st.session_state.dark_mode)

# 3. CSS INJECTION BASED ON TOGGLE
if theme_toggle:
    bg_color, text_color, border_color = "#0e1117", "#ffffff", "#30363d"
else:
    bg_color, text_color, border_color = "#ffffff", "#000000", "#e6e9ef"

st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        h1, h2, h3, p {{ color: {text_color} !important; }}
        .stInfo {{ background-color: {border_color}; color: {text_color}; }}
    </style>
    """, unsafe_allow_html=True)

# --- NEW: DATA LOADING SECTION ---
# Make sure 'data.csv' is in the same folder as gemini.py
@st.cache_data # This makes the app faster by not reloading the file every time
def load_data():
    df = pd.read_csv("data.csv")
    df['country'] = df['country'].str.title() # Make sure countries look nice
    return df

data = load_data()

# 4. HEADER
st.title("tam vonku - dashboard")
st.divider()

# 5. THREE COLUMN LAYOUT
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌍 Visited Countries")
    
    # Process the data for the table
    # We group by country and sum up the nights
    visited_df = data.groupby('country')['nights'].sum().reset_index()
    
    # Sort by nights (most visited first)
    visited_df = visited_df.sort_values('nights', ascending=False)
    
    # Reset index to start from 1 for the table
    visited_df.index = range(1, len(visited_df) + 1)
    visited_df.index.name = "Index"
    
    # Rename columns as requested
    visited_df.columns = ["Country", "Nights Spent"]
    
    # Display the table
    st.dataframe(visited_df, use_container_width=True)

with col2:
    st.subheader("Column 2")
    st.write("Here comes **Price per Person**.")
    st.info("Empty Data Slot 2")

with col3:
    st.subheader("Column 3")
    st.write("Here comes **Activity Breakdown**.")
    st.info("Empty Data Slot 3")

st.divider()
