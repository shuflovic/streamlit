import streamlit as st

# 1. PAGE SETUP
# 'layout="wide"' is what makes it look like a PC dashboard rather than a mobile app.
st.set_page_config(
    page_title="tam vonku - dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. HEADER
st.title("tam vonku - dashboard")
st.markdown("---") # This adds a clean divider line

# 3. THREE COLUMN LAYOUT
# We create 3 variables (col1, col2, col3) to act as containers.
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Column 1")
    st.write("Here comes the **Accommodation Nights** pie chart.")
    # This creates a grey box placeholder
    st.info("Placeholder for Chart 1")

with col2:
    st.header("Column 2")
    st.write("Here comes the **Price per Person** bar chart.")
    st.info("Placeholder for Chart 2")

with col3:
    st.header("Column 3")
    st.write("Here comes the **Activity Breakdown** donut chart.")
    st.info("Placeholder for Chart 3")

# 4. FOOTER / DIVIDER
st.divider()
st.write("This is the bottom of the page. Later we will add the map here.")
