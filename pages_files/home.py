import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, apply_filters

def show_home_page():
    # Load data
    df = load_data()
    
    # Global filters section
    st.header("🔍 Global Filters")
    st.info("Set filters here to apply across all pages")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        all_states = sorted(df['ship_state'].unique().tolist())
        state_options = ['All'] + all_states
        selected_state = st.selectbox(
            "Select State",
            state_options,
            index=state_options.index(st.session_state.selected_state)
        )
        st.session_state.selected_state = selected_state
    
    with col2:
        all_months = sorted(df['month_name'].unique().tolist())
        month_options = ['All'] + all_months
        selected_month = st.selectbox(
            "Select Month",
            month_options,
            index=month_options.index(st.session_state.selected_month)
        )
        st.session_state.selected_month = selected_month
    
    with col3:
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_options = ['All'] + weekday_order
        available_days = sorted(df['day_of_week'].unique().tolist())
        day_options_filtered = ['All'] + [day for day in weekday_order if day in available_days]
        selected_day = st.selectbox(
            "Select Day",
            day_options_filtered,
            index=day_options_filtered.index(st.session_state.selected_day) if st.session_state.selected_day in day_options_filtered else 0
        )
        st.session_state.selected_day = selected_day
    
    # Apply filters
    filtered_df = apply_filters(
        df,
        st.session_state.selected_state,
        st.session_state.selected_month,
        st.session_state.selected_day
    )
    
    # Display active filters
    if (st.session_state.selected_state != 'All' or 
        st.session_state.selected_month != 'All' or 
        st.session_state.selected_day != 'All'):
        st.success(
            f"Active Filters - State: {st.session_state.selected_state} | "
            f"Month: {st.session_state.selected_month} | "
            f"Day: {st.session_state.selected_day}"
        )
    
    st.markdown("---")
    
    # Overview metrics
    st.header("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", f"{len(filtered_df):,}")
    with col2:
        st.metric("Total Revenue", f"₹{filtered_df['total_revenue'].sum():,.0f}")
    with col3:
        st.metric("Average Order Value", f"₹{filtered_df['amount'].mean():.2f}")
    with col4:
        st.metric("Total Products Sold", f"{filtered_df['Quantity'].sum():,}")
    
    st.markdown("---")
    
    # Dataset Information
    st.header("📋 Dataset Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Summary")
        st.write(f"- **Date Range**: {filtered_df['date'].min().strftime('%B %d, %Y')} to {filtered_df['date'].max().strftime('%B %d, %Y')}")
        st.write(f"- **Number of Records**: {len(filtered_df):,}")
        st.write(f"- **Number of Categories**: {filtered_df['category'].nunique()}")
        st.write(f"- **Number of States**: {filtered_df['ship_state'].nunique()}")
        st.write(f"- **Number of Cities**: {filtered_df['ship_city'].nunique()}")
    
    with col2:
        st.subheader("Key Features")
        st.write("- **Order Information**: Order ID, Date, Status")
        st.write("- **Product Details**: Category, Size, Style, SKU")
        st.write("- **Shipping Info**: City, State, Service Level")
        st.write("- **Financial Data**: Amount, Currency, Promotions")
        st.write("- **Customer Type**: B2B vs B2C classification")
    
    # Top Statistics
    st.header("🏆 Top Performers")
    col1, col2 = st.columns(2)  # Fixed: was incorrectly creating single columns
    
    with col1:
        # Calculate sales_per_state dynamically
        sales_per_state = filtered_df.groupby('ship_state').agg({
            'order_id': 'count',
            'total_revenue': 'sum',
            'amount': 'mean',
            'Quantity': 'sum'
        }).round(2)
        sales_per_state.columns = ['Total_Orders', 'Total_Revenue', 'Avg_Order_Value', 'Total_Quantity']
        sales_per_state = sales_per_state.sort_values('Total_Revenue', ascending=False)
        
        top_states = sales_per_state.head(5)
        st.subheader("Top 5 States by Revenue")
        fig = px.bar(top_states.reset_index(), x='ship_state', y='Total_Revenue',
                    color='Total_Revenue', color_continuous_scale='Blues')
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        top_categories = filtered_df.groupby('category')['total_revenue'].sum().sort_values(ascending=False).head(5)
        st.subheader("Top 5 Categories by Revenue")
        fig = px.bar(x=top_categories.index, y=top_categories.values,
                    color=top_categories.values, color_continuous_scale='Greens')
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    

    st.subheader("Order Status Distribution")
    status_dist = filtered_df['status'].value_counts()
    fig = px.pie(values=status_dist.values, names=status_dist.index,
                color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(showlegend=True, height=300)
    st.plotly_chart(fig, use_container_width=True)