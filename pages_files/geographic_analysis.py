import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, apply_filters

def show_geographic_analysis():
    # Load data
    df = load_data()
    
    # Apply global filters
    filtered_df_global = apply_filters(
        df,
        st.session_state.selected_state,
        st.session_state.selected_month,
        st.session_state.selected_day
    )
    
    # Display active filters
    if (st.session_state.selected_state != 'All' or 
        st.session_state.selected_month != 'All' or 
        st.session_state.selected_day != 'All'):
        st.info(
            f"Active Filters - State: {st.session_state.selected_state} | "
            f"Month: {st.session_state.selected_month} | "
            f"Day: {st.session_state.selected_day}"
        )
    
    # Additional state filter for this page
    col1, col2 = st.columns([3, 1])
    with col1:
        available_states = sorted(filtered_df_global['ship_state'].unique().tolist())
        selected_state = st.selectbox("Filter by specific state", ['All'] + available_states)
    
    if selected_state != 'All':
        page_filtered_df = filtered_df_global[filtered_df_global['ship_state'] == selected_state]
    else:
        page_filtered_df = filtered_df_global
    
    # Key metrics for selected area
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Orders", f"{len(page_filtered_df):,}")
    with col2:
        st.metric("Revenue", f"₹{page_filtered_df['total_revenue'].sum():,.0f}")
    with col3:
        st.metric("Avg Order Value", f"₹{page_filtered_df['amount'].mean():.2f}")
    with col4:
        st.metric("Cities Served", f"{page_filtered_df['ship_city'].nunique()}")
    
    # Visualizations
    tab1, tab2, tab3 = st.tabs(["State Performance", "City Analysis", "Regional Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Top states by revenue
            sales_per_state = filtered_df_global.groupby('ship_state').agg({
                'order_id': 'count',
                'total_revenue': 'sum',
                'amount': 'mean',
                'Quantity': 'sum'
            }).round(2)
            sales_per_state.columns = ['Total_Orders', 'Total_Revenue', 'Avg_Order_Value', 'Total_Quantity']
            sales_per_state = sales_per_state.sort_values('Total_Revenue', ascending=False)
            
            fig = px.bar(sales_per_state.head(15).reset_index(), 
                        x='Total_Revenue', y='ship_state',
                        orientation='h', title="Top 15 States by Revenue",
                        color='Total_Revenue', color_continuous_scale='Viridis')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # State order volume vs revenue scatter
            fig = px.scatter(sales_per_state.reset_index(), 
                           x='Total_Orders', y='Total_Revenue',
                           size='Total_Quantity', color='Avg_Order_Value',
                           hover_data=['ship_state'], title="Orders vs Revenue by State",
                           color_continuous_scale='Blues')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        if selected_state != 'All':
            city_data = page_filtered_df.groupby('ship_city').agg({
                'order_id': 'count',
                'total_revenue': 'sum',
                'amount': 'mean'
            }).round(2)
            city_data.columns = ['Orders', 'Revenue', 'Avg_Order_Value']
            city_data = city_data.sort_values('Revenue', ascending=False).head(10)
            
            fig = px.bar(city_data.reset_index(), x='ship_city', y='Revenue',
                        title=f"Top 10 Cities in {selected_state}",
                        color='Revenue', color_continuous_scale='Oranges')
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Overall top cities
            city_data = filtered_df_global.groupby('ship_city').agg({
                'order_id': 'count',
                'total_revenue': 'sum'
            }).round(2)
            city_data.columns = ['Orders', 'Revenue']
            top_cities = city_data.sort_values('Revenue', ascending=False).head(20)
            
            fig = px.bar(top_cities.reset_index(), x='ship_city', y='Revenue',
                        title="Top 20 Cities by Revenue",
                        color='Revenue', color_continuous_scale='Oranges')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Regional insights
        col1, col2 = st.columns(2)
        
        with col1:
            # B2B vs B2C by state
            state_customer = filtered_df_global.groupby(['ship_state', 'customer_type']).size().unstack(fill_value=0)
            state_customer = state_customer.loc[state_customer.sum(axis=1).nlargest(10).index]
            
            fig = px.bar(state_customer.reset_index(), x='ship_state', 
                        y=['B2B', 'B2C'], title="B2B vs B2C Orders by Top 10 States",
                        barmode='stack')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Delivery success by state
            delivery_success = filtered_df_global[filtered_df_global['status'].str.contains('Delivered', na=False)]
            state_delivery = (delivery_success.groupby('ship_state').size() / 
                            filtered_df_global.groupby('ship_state').size() * 100).round(2)
            state_delivery = state_delivery.nlargest(15)
            
            fig = px.bar(x=state_delivery.index, y=state_delivery.values,
                        title="Delivery Success Rate by State (Top 15)",
                        labels={'y': 'Success Rate (%)', 'x': 'State'})
            fig.update_layout(height=400)
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)