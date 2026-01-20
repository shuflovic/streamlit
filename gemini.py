import streamlit as st
import pandas as pd

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

# --- DATA LOADING SECTION ---
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    
    # Clean data types
    df['country'] = df['country'].str.title()
    df['person'] = pd.to_numeric(df['person'], errors='coerce').fillna(1)
    df['nights'] = pd.to_numeric(df['nights'], errors='coerce').fillna(0)
    
    # NEW CALCULATION: Total nights = nights / 2 * person
    df['calculated_nights'] = ((df['nights'] / 2) * df['person']).astype(int)
    
    return df

data = load_data()

# 4. HEADER
st.title("tam vonku - dashboard")
st.divider()

# 5. THREE COLUMN LAYOUT
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌍 Visited Countries")
    
    # Group by country using our new 'calculated_nights' column
    visited_df = data.groupby('country')['calculated_nights'].sum().reset_index()
    
    # Sort and prepare table
    visited_df = visited_df.sort_values('calculated_nights', ascending=False)
    visited_df.index = range(1, len(visited_df) + 1)
    visited_df.index.name = "Index"
    
    # Rename for display
    visited_df.columns = ["Country", "Nights Spent"]
    
    # Display the table
  
    st.data_editor(
    visited_df, 
    use_container_width=True, 
    hide_index=True, 
    column_config={
        "Country": st.column_config.TextColumn(alignment="center"),
        "Nights Spent": st.column_config.NumberColumn(alignment="center")
    }
)

with col2:
    st.subheader("Column 2")
    st.write("Ready for the next set of data.")
    st.info("Empty Data Slot 2")

with col3:
    st.subheader("Column 3")
    st.write("Ready for the next set of data.")
    st.info("Empty Data Slot 3")

st.divider()
