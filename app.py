import streamlit as st
import pandas as pd
import base64

# Function to convert image to base64 
def get_base64_of_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

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

# Try to load the background image
try:
    # Update this path to match your actual file location
    
    img_path = ".\streamlit\static\powerBISalesDashboard-banner.jpg"
    img_base64 = get_base64_of_image(img_path)
    
    # Custom CSS with base64 image
    st.markdown(f"""
    <style>
        .metric-container {{
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
        }}
        .main-header {{
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            padding: 50px 20px;
            text-align: center;
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .main-header h1 {{
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
        }}
    </style>
    """, unsafe_allow_html=True)
except:
    # Fallback CSS without background image
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
        .main-header {
            background-color: #1f4788;
            padding: 50px 20px;
            text-align: center;
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Title with background
st.markdown("""
<div class="main-header">
    <h1>🛍️ Amazon Sales Dashboard</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🗺️ Geographic Analysis", "📅 Time Analysis", "🛍️ Product & Customer Analysis"]
)

# Route to appropriate page
if page == "🏠 Home":
    from pages_files.home import show_home_page
    show_home_page()
elif page == "🗺️ Geographic Analysis":
    from pages_files.geographic_analysis import show_geographic_analysis
    show_geographic_analysis()
elif page == "📅 Time Analysis":
    from pages_files.time_analysis import show_time_analysis
    show_time_analysis()
elif page == "🛍️ Product & Customer Analysis":
    from pages_files.product_customer_analysis import show_product_customer_analysis
    show_product_customer_analysis()

# Footer
st.markdown("---")
st.markdown("📊 Amazon Sales Dashboard || Data Analysis Project || By IBRAHIM SABER")
st.markdown("https://github.com/ibrahimsaber1")
st.markdown("Github repo Link===> https://github.com/ibrahimsaber1/Amazon-Sales-Analysis")
