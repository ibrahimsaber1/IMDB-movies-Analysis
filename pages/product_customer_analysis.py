import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import load_data, apply_filters

def show_product_customer_analysis():
    # Load data
    df = load_data()
    
    # Apply global filters
    page_filtered_df = apply_filters(
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
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        available_categories = sorted(page_filtered_df['category'].unique().tolist())
        selected_category = st.selectbox("Select Category", ['All'] + available_categories)
    with col2:
        selected_customer = st.selectbox("Customer Type", ['All', 'B2B', 'B2C'])
    with col3:
        if 'price_tier' in page_filtered_df.columns:
            available_tiers = sorted(page_filtered_df['price_tier'].cat.categories.tolist())
            selected_tier = st.selectbox("Price Tier", ['All'] + available_tiers)
        else:
            selected_tier = 'All'
    
    # Filter data
    if selected_category != 'All':
        page_filtered_df = page_filtered_df[page_filtered_df['category'] == selected_category]
    if selected_customer != 'All':
        page_filtered_df = page_filtered_df[page_filtered_df['customer_type'] == selected_customer]
    if selected_tier != 'All' and 'price_tier' in page_filtered_df.columns:
        page_filtered_df = page_filtered_df[page_filtered_df['price_tier'] == selected_tier]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Products Sold", f"{page_filtered_df['Quantity'].sum():,}")
    with col2:
        st.metric("Revenue", f"₹{page_filtered_df['total_revenue'].sum():,.0f}")
    with col3:
        valid_unit_prices = page_filtered_df[page_filtered_df['unit_price'] != float('inf')]['unit_price']
        avg_unit_price = valid_unit_prices.mean() if not valid_unit_prices.empty else 0
        st.metric("Avg Unit Price", f"₹{avg_unit_price:.2f}")
    with col4:
        cancellation_rate = (page_filtered_df['status'] == 'Cancelled').mean() * 100 if not page_filtered_df.empty else 0
        st.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Category Analysis", "Customer Insights", "Size Analysis", "Price Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Category revenue - using global filtered data
            filtered_df_global = apply_filters(
                df,
                st.session_state.selected_state,
                st.session_state.selected_month,
                st.session_state.selected_day
            )
            category_revenue = filtered_df_global.groupby('category')['total_revenue'].sum().sort_values(ascending=False)
            if not category_revenue.empty:
                fig = px.bar(x=category_revenue.index, y=category_revenue.values,
                            title='Revenue by Category',
                            labels={'x': 'Category', 'y': 'Revenue (₹)'},
                            color=category_revenue.values, color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters")
        
        with col2:
            # Category volume
            category_volume = filtered_df_global.groupby('category')['Quantity'].sum().sort_values(ascending=False)
            if not category_volume.empty:
                fig = px.pie(values=category_volume.values, names=category_volume.index,
                            title='Sales Volume by Category')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters")
        
        # Cancellation rate by category
        if not filtered_df_global.empty:
            cancellation_by_category = filtered_df_global.groupby('category', group_keys=False).apply(
                lambda x: (x['status'] == 'Cancelled').sum() / len(x) * 100 if len(x) > 0 else 0
            ).sort_values(ascending=False)
            
            if not cancellation_by_category.empty:
                fig = px.bar(x=cancellation_by_category.index, y=cancellation_by_category.values,
                            title='Cancellation Rate by Category',
                            labels={'x': 'Category', 'y': 'Cancellation Rate (%)'},
                            color=cancellation_by_category.values, color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters")
        else:
            st.info("No data available for the selected filters")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # B2B vs B2C comparison
            filtered_df_global = apply_filters(
                df,
                st.session_state.selected_state,
                st.session_state.selected_month,
                st.session_state.selected_day
            )
            if not filtered_df_global.empty:
                customer_comparison = filtered_df_global.groupby('customer_type').agg({
                    'order_id': 'count',
                    'total_revenue': 'sum',
                    'amount': 'mean'
                }).round(2)
                customer_comparison.columns = ['Orders', 'Revenue', 'AOV']
                
                fig = px.bar(customer_comparison.reset_index(), x='customer_type', 
                            y=['Orders', 'Revenue'], barmode='group',
                            title='B2B vs B2C Comparison')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters")
        
        with col2:
            # Customer type by category
            if not filtered_df_global.empty:
                customer_category = filtered_df_global.groupby(['category', 'customer_type']).size().unstack(fill_value=0)
                fig = px.bar(customer_category.reset_index(), x='category', 
                            y=['B2B', 'B2C'], barmode='stack',
                            title='Customer Type Distribution by Category')
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters")
        
        # Promotion impact by customer type
        if not filtered_df_global.empty and 'has_promotion' in filtered_df_global.columns:
            promo_impact = filtered_df_global.groupby(['customer_type', 'has_promotion'])['amount'].mean().unstack(fill_value=0)
            fig = px.bar(promo_impact.reset_index(), x='customer_type', 
                        y=[False, True], barmode='group',
                        title='Average Order Value: With vs Without Promotion',
                        labels={'value': 'AOV (₹)', 'variable': 'Has Promotion'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters")
    
    with tab3:
        # Size distribution by category
        if not page_filtered_df.empty:
            size_category = page_filtered_df.groupby(['category', 'size'])['Quantity'].sum().unstack(fill_value=0)
            
            # Get top sizes
            top_sizes = page_filtered_df.groupby('size')['Quantity'].sum().nlargest(7).index
            size_category = size_category[size_category.columns.intersection(top_sizes)]
            
            if not size_category.empty:
                fig = px.bar(size_category.reset_index(), x='category', y=size_category.columns.tolist(),
                            title='Size Distribution by Category', barmode='stack')
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters")
            
            # Most popular size by category
            col1, col2 = st.columns(2)
            
            with col1:
                popular_sizes = page_filtered_df.groupby(['category', 'size'])['Quantity'].sum()
                if not popular_sizes.empty:
                    popular_sizes = popular_sizes.groupby('category').nlargest(1).reset_index(level=1)
                    
                    fig = px.bar(popular_sizes.reset_index(), x='category', y='Quantity',
                                color='size', title='Most Popular Size by Category')
                    fig.update_xaxes(tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected filters")
            
            with col2:
                # Size revenue contribution
                size_revenue = page_filtered_df.groupby('size')['total_revenue'].sum().sort_values(ascending=False).head(10)
                if not size_revenue.empty:
                    fig = px.pie(values=size_revenue.values, names=size_revenue.index,
                                title='Revenue Contribution by Size (Top 10)')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected filters")
        else:
            st.info("No data available for the selected filters")
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Price tier distribution
            if 'price_tier' in page_filtered_df.columns and not page_filtered_df.empty:
                tier_dist = page_filtered_df['price_tier'].value_counts()
                fig = px.pie(values=tier_dist.values, names=tier_dist.index,
                            title='Order Distribution by Price Tier')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Price tier data not available")
        
        with col2:
            # Revenue by price tier
            if 'price_tier' in page_filtered_df.columns and not page_filtered_df.empty:
                tier_revenue = page_filtered_df.groupby('price_tier')['total_revenue'].sum()
                fig = px.bar(x=tier_revenue.index, y=tier_revenue.values,
                            title='Revenue by Price Tier',
                            color=tier_revenue.values, color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Price tier data not available")
        
        # Price analysis by category
        valid_prices = page_filtered_df[page_filtered_df['unit_price'] != float('inf')]
        if not valid_prices.empty:
            category_prices = valid_prices.groupby('category')['unit_price'].mean().sort_values(ascending=False)
            
            fig = px.bar(x=category_prices.index, y=category_prices.values,
                        title='Average Unit Price by Category',
                        labels={'x': 'Category', 'y': 'Avg Unit Price (₹)'},
                        color=category_prices.values, color_continuous_scale='Viridis')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Price distribution
            st.subheader("Price Distribution Analysis")
            fig = px.histogram(valid_prices, x='unit_price', nbins=50,
                              title='Unit Price Distribution',
                              labels={'unit_price': 'Unit Price (₹)', 'count': 'Frequency'})
            fig.update_xaxes(range=[0, 2000])  # Limit range for better visualization
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No valid price data available for the selected filters")