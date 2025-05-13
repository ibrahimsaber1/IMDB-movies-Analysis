import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Amazon Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

# Initialize session state for filters
if 'selected_state' not in st.session_state:
    st.session_state.selected_state = 'All'
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = 'All'
if 'selected_day' not in st.session_state:
    st.session_state.selected_day = 'All'

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛍️ Amazon Sales Dashboard")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🗺️ Geographic Analysis", "📅 Time Analysis", "🛍️ Product & Customer Analysis"]
)

# Route to appropriate page
if page == "🏠 Home":
    from pages.home import show_home_page
    show_home_page()
elif page == "🗺️ Geographic Analysis":
    from pages.geographic_analysis import show_geographic_analysis
    show_geographic_analysis()
elif page == "📅 Time Analysis":
    from pages.time_analysis import show_time_analysis
    show_time_analysis()
elif page == "🛍️ Product & Customer Analysis":
    from pages.product_customer_analysis import show_product_customer_analysis
    show_product_customer_analysis()

# Footer
st.markdown("---")
st.markdown("📊 Amazon Sales Dashboard | Data Analysis Project")
