import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import load_data, apply_filters

def show_time_analysis():
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
    
    # Calculate weekday order
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Orders", f"{len(page_filtered_df):,}")
    with col2:
        st.metric("Revenue", f"₹{page_filtered_df['total_revenue'].sum():,.0f}")
    with col3:
        if page_filtered_df['date'].nunique() > 0:
            avg_daily_orders = len(page_filtered_df) / page_filtered_df['date'].nunique()
        else:
            avg_daily_orders = 0
        st.metric("Avg Daily Orders", f"{avg_daily_orders:.0f}")
    with col4:
        if not page_filtered_df.empty:
            peak_orders = page_filtered_df.groupby('date').size().max()
        else:
            peak_orders = 0
        st.metric("Peak Day Orders", f"{peak_orders}")
    
    # Visualizations
    tab1, tab2, tab3 = st.tabs(["Monthly Trends", "Weekly Patterns", "Daily Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly revenue trend
            monthly_data = page_filtered_df.groupby('month_name').agg({
                'total_revenue': 'sum',
                'order_id': 'count'
            })
            available_months = [m for m in ['April', 'May', 'June'] if m in monthly_data.index]
            if available_months:
                monthly_data = monthly_data.reindex(available_months)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Revenue', x=monthly_data.index, 
                                   y=monthly_data['total_revenue'],
                                   yaxis='y', marker_color='lightblue'))
                fig.add_trace(go.Scatter(name='Order Count', x=monthly_data.index, 
                                       y=monthly_data['order_id'],
                                       yaxis='y2', marker_color='red', mode='lines+markers'))
                
                fig.update_layout(
                    title='Monthly Revenue and Order Trends',
                    yaxis=dict(title='Revenue (₹)', side='left'),
                    yaxis2=dict(title='Order Count', side='right', overlaying='y'),
                    hovermode='x'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected filters")
        
        with col2:
            # Monthly category performance
            if not page_filtered_df.empty:
                monthly_category = page_filtered_df.groupby(['month_name', 'category'])['total_revenue'].sum().unstack(fill_value=0)
                available_months = [m for m in ['April', 'May', 'June'] if m in monthly_category.index]
                if available_months:
                    monthly_category = monthly_category.reindex(available_months)
                    
                    fig = px.bar(monthly_category.T, barmode='group',
                                title='Category Performance by Month')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected filters")
            else:
                st.info("No data available for the selected filters")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        # Calculate sales_per_weekday dynamically
        sales_per_weekday = page_filtered_df.groupby('day_of_week').agg({
            'order_id': 'count',
            'total_revenue': 'sum',
            'amount': 'mean',
            'Quantity': 'sum'
        }).round(2)
        
        if not sales_per_weekday.empty:
            sales_per_weekday.columns = ['Total_Orders', 'Total_Revenue', 'Avg_Order_Value', 'Total_Quantity']
            available_days = [d for d in weekday_order if d in sales_per_weekday.index]
            if available_days:
                sales_per_weekday = sales_per_weekday.reindex(available_days)
            
            with col1:
                # Weekly pattern
                fig = px.bar(sales_per_weekday.reset_index(), x='day_of_week', y='Total_Revenue',
                            title='Revenue by Day of Week',
                            color='Total_Revenue', color_continuous_scale='Greens')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Order volume by weekday
                fig = px.line(sales_per_weekday.reset_index(), x='day_of_week', y='Total_Orders',
                             title='Order Volume by Day of Week', markers=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            col1.info("No data available for the selected filters")
            col2.info("No data available for the selected filters")
    
    with tab3:
        if not page_filtered_df.empty:
            # Daily trends
            daily_data = page_filtered_df.groupby('date').agg({
                'order_id': 'count',
                'total_revenue': 'sum',
                'amount': 'mean'
            }).reset_index()
            
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                               subplot_titles=('Daily Orders', 'Daily Revenue'))
            
            fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['order_id'],
                                   mode='lines', name='Orders', line=dict(color='blue')),
                         row=1, col=1)
            
            fig.add_trace(go.Scatter(x=daily_data['date'], y=daily_data['total_revenue'],
                                   mode='lines', name='Revenue', line=dict(color='green')),
                         row=2, col=1)
            
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Orders", row=1, col=1)
            fig.update_yaxes(title_text="Revenue (₹)", row=2, col=1)
            fig.update_layout(height=600, showlegend=False, title='Daily Sales Trends')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Peak hours analysis (simulated since we don't have hour data)
            st.subheader("Order Distribution Patterns")
            col1, col2 = st.columns(2)
            
            with col1:
                # Orders by day of month
                day_of_month = page_filtered_df.groupby(page_filtered_df['date'].dt.day).size()
                if not day_of_month.empty:
                    fig = px.bar(x=day_of_month.index, y=day_of_month.values,
                                title='Orders by Day of Month',
                                labels={'x': 'Day', 'y': 'Order Count'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected filters")
            
            with col2:
                # Heatmap of orders by week and day
                if 'week' not in page_filtered_df.columns:
                    page_filtered_df['week'] = page_filtered_df['date'].dt.isocalendar().week
                heatmap_data = page_filtered_df.groupby(['week', 'day_of_week']).size().unstack(fill_value=0)
                available_days = [d for d in weekday_order if d in heatmap_data.columns]
                if available_days:
                    heatmap_data = heatmap_data[available_days]
                    
                    fig = px.imshow(heatmap_data, 
                                   labels=dict(x="Day of Week", y="Week", color="Orders"),
                                   title="Order Heatmap by Week and Day",
                                   color_continuous_scale='YlOrRd')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available for the selected filters")
        else:
            st.info("No data available for the selected filters")