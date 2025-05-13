import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """Load the cleaned data"""
    df = pd.read_csv('data/Amazon_Sales_Cleaned.csv')
    df['date'] = pd.to_datetime(df['date'])
    # Ensure categorical columns exist
    if 'price_tier' in df.columns:
        df['price_tier'] = pd.Categorical(df['price_tier'], 
                                         categories=['Budget', 'Mid-range', 'Premium', 'Luxury'], 
                                         ordered=True)
    return df

def apply_filters(df, state='All', month='All', day='All'):
    """Apply filters to the dataframe"""
    filtered_df = df.copy()
    
    if state != 'All':
        filtered_df = filtered_df[filtered_df['ship_state'] == state]
    if month != 'All':
        filtered_df = filtered_df[filtered_df['month_name'] == month]
    if day != 'All':
        filtered_df = filtered_df[filtered_df['day_of_week'] == day]
    
    return filtered_df