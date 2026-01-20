import streamlit as st

# 1. PAGE SETUP
st.set_page_config(
    page_title="tam vonku - dashboard",
    layout="wide"
)

# 2. THEME TOGGLE LOGIC
# We use a toggle in the top right or sidebar
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

theme_toggle = st.toggle(f"Current mode: {'Dark' if theme_toggle else 'Light'}", value=st.session_state.dark_mode)

# 3. CSS INJECTION BASED ON TOGGLE
if theme_toggle:
    # DARK CSS
    bg_color = "#0e1117"
    text_color = "#ffffff"
    border_color = "#30363d"
else:
    # LIGHT CSS
    bg_color = "#ffffff"
    text_color = "#000000"
    border_color = "#e6e9ef"

st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        h1, h2, h3, p {{
            color: {text_color} !important;
        }}
        /* This helps style the empty placeholders */
        .stInfo {{
            background-color: {border_color};
            color: {text_color};
        }}
    </style>
    """, unsafe_allow_html=True)

# 4. HEADER
st.title("tam vonku - dashboard")
st.divider()

# 5. THREE COLUMN LAYOUT
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Column 1")
    st.write("Here comes **Accommodation Nights**.")
    st.info("Empty Data Slot 1")

with col2:
    st.subheader("Column 2")
    st.write("Here comes **Price per Person**.")
    st.info("Empty Data Slot 2")

with col3:
    st.subheader("Column 3")
    st.write("Here comes **Activity Breakdown**.")
    st.info("Empty Data Slot 3")

st.divider()
