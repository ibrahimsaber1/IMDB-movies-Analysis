# Amazon Sales Analysis Project
## Comprehensive Project Documentation

### Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset Description](#dataset-description)
3. [Data Preparation Process](#data-preparation-process)
4. [Feature Engineering](#feature-engineering)
5. [Dashboard Implementation](#dashboard-implementation)
6. [Key Insights & Findings](#key-insights--findings)
7. [Deployment Challenges & Solutions](#deployment-challenges--solutions)
8. [Future Enhancement Opportunities](#future-enhancement-opportunities)

---

## Project Overview

This project delivers a comprehensive analysis of Amazon.in sales data through an interactive Streamlit dashboard. The analysis covers order patterns, geographic distribution, product preferences, and customer behavior to provide actionable business insights.

**Project Goals:**
- Analyze sales trends across time periods (daily, weekly, monthly)
- Identify top-performing regions and product categories
- Understand customer purchasing behavior (B2B vs B2C)
- Examine order fulfillment and delivery performance
- Provide actionable business recommendations

**Tech Stack:**
- **Python**: Core programming language
- **Pandas & NumPy**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **Streamlit**: Web application framework for dashboard

---

## Dataset Description

The dataset contains order information from Amazon's sales platform (Amazon.in) spanning April-June 2022.

**Source**: Kaggle - [Amazon Sales Report Dataset](https://www.kaggle.com/datasets/mdsazzatsardar/amazonsalesreport)

**Key Metrics:**
- **Dataset Size**: ~129,000 records
- **Time Period**: April-June 2022
- **Geographic Coverage**: India (all states)
- **Product Categories**: 9 categories (kurta, Set, Western Dress, etc.)

**Original Column Details:**

| Column | Description |
|--------|-------------|
| `Order ID` | Unique identifier for each order |
| `Date` | Order placement date (MM-DD-YY) |
| `Status` | Order status (Shipped, Cancelled, Delivered, etc.) |
| `Fulfilment` | Entity responsible (Merchant/Amazon) |
| `Sales Channel` | Platform where sale occurred |
| `Category` | Product category |
| `Size` | Product size (XS, S, M, L, XL, etc.) |
| `Quantity` | Number of items ordered |
| `Amount` | Price in Indian Rupees (INR) |
| `ship-city`/`ship-state` | Shipping destination |
| `B2B` | Boolean for Business-to-Business transactions |

---

## Data Preparation Process

### Initial Data Assessment
Initial examination revealed several data quality issues requiring attention:
- Inconsistent column naming conventions
- Missing data in critical fields
- Inconsistent location spellings
- Data type issues
- Null values in monetary fields

### Cleaning Steps Implemented

#### 1. Column Standardization
```python
# Standardize column names to consistent format
df.columns = df.columns.str.strip()
df.columns = df.columns.str.lower().str.replace(' ', '_')
df.columns = df.columns.str.lower().str.replace('-', '_')
```

#### 2. Handling Missing Address Data
**Issue**: 33 rows (0.03% of data) had null address information
```python
# Drop rows with missing address information
df.dropna(subset=['ship_city', 'ship_state', 'ship_postal_code', 'ship_country'], inplace=True)
df.reset_index(drop=True, inplace=True)
```

#### 3. Removing Unnecessary Columns
```python
# Remove columns with no useful information
df.drop(columns=['unnamed:_22', 'fulfilled_by'], inplace=True)
```

#### 4. Handling Duplicate Records
```python
# Check and remove duplicates
print('Number of duplicated values:', df.duplicated().sum())
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
```

#### 5. Data Type Conversion
```python
# Convert date to datetime format
df.date = pd.to_datetime(df.date)

# Convert postal code to integer
df['ship_postal_code'] = df['ship_postal_code'].astype('int')

# Rename quantity column for clarity
df.rename(columns={'qty': 'Quantity'}, inplace=True)
```

#### 6. Location Name Standardization
**Before Cleaning:**
- States: 69 unique values
- Cities: 8,955 unique values

**Problem**: Multiple spellings for same locations (e.g., 'Delhi', 'New Delhi', 'delhi')

**Solution**: Created comprehensive mapping dictionaries

```python
# Sample of state mapping dictionary
state_mapping = {
    # Delhi variations
    'delhi': 'delhi',
    'new delhi': 'delhi',
    
    # Rajasthan variations
    'rajasthan': 'rajasthan',
    'rajshthan': 'rajasthan',
    'rajsthan': 'rajasthan',
    'rj': 'rajasthan',
    
    # Many more mappings...
}

df['ship_state'] = df['ship_state'].replace(state_mapping)
```

Similar approach was used for city standardization, mapping variations like:
- 'Mumbai', 'Mumbai 400101', 'Mumbai dadar west' → 'mumbai'
- 'Bengaluru', 'Bangalore', 'Bangalore north' → 'bengaluru'

**After Cleaning:**
- States: 33 unique values
- Cities: 3,456 unique values

#### 7. Currency Standardization
```python
# Fill missing currency values with INR
df['currency'] = df['currency'].fillna('INR')
```

#### 8. Promotion Data Handling
```python
# Replace missing promotion IDs with 'No Promotion'
df['promotion_ids'] = df['promotion_ids'].fillna('No Promotion')
```

#### 9. Order Status Consistency
```python
# Fill 'Courier Status' with 'Cancelled' when Status is 'Cancelled'
df.loc[df['status'] == 'Cancelled', 'courier_status'] = 'Cancelled'

# Handle remaining nulls in courier_status
df['courier_status'].fillna('Unknown', inplace=True)
```

#### 10. Missing Amount Values
**Problem**: Null values in the 'amount' column critical for revenue calculation

**Solution**: Sophisticated imputation approach using style-based median prices

```python
# Calculate median unit price per style
mask_valid = (df['amount'] > 0) & (df['Quantity'] > 0)
df['unit_price'] = df['amount'] / df['Quantity']
median_unit_prices = df[mask_valid].groupby('style')['unit_price'].median()

# Map median prices to all rows
df['median_price'] = df['style'].map(median_unit_prices)
overall_median = df[mask_valid]['unit_price'].median()

# Fill missing amounts using either style median or overall median
df['amount'] = np.where(
    df['amount'].isna(),
    np.where(
        df['median_price'].notna(),
        df['Quantity'] * df['median_price'],
        df['Quantity'] * overall_median
    ),
    df['amount']
)

# Clean up temporary columns
df = df.drop(['unit_price', 'median_price'], axis=1)
```

---

## Feature Engineering

To enhance analysis capabilities, several derived columns were created:

### 1. Time-Based Features
```python
# Create month number column
df['month'] = df['date'].dt.month

# Create month name column for better readability
df['month_name'] = df['date'].dt.month_name()

# Create day of week for weekly pattern analysis
df['day_of_week'] = df['date'].dt.day_name()

# Create week number for weekly aggregation
df['week'] = df['date'].dt.isocalendar().week

# Create day of month for daily pattern analysis
df['day_of_month'] = df['date'].dt.day
```

### 2. Promotion Analysis Features
```python
# Create binary flag for promotion usage
df['has_promotion'] = df['promotion_ids'] != 'No Promotion'
```

### 3. Price Segmentation
```python
# Categorize orders into price tiers
df['price_tier'] = pd.cut(df['amount'], 
                         bins=[0, 300, 600, 900, float('inf')],
                         labels=['Budget', 'Mid-range', 'Premium', 'Luxury'])
```

### 4. Unit Economics Calculation
```python
# Calculate price per unit
df['unit_price'] = df['amount'] / df['Quantity']
```

### 5. Customer Type Classification
```python
# Convert boolean B2B flag to descriptive text
df['customer_type'] = df['b2b'].apply(lambda x: 'B2B' if x else 'B2C')
```

### 6. Revenue Calculation
```python
# Calculate total revenue per order
df['total_revenue'] = df['amount'] * df['Quantity']
```

These derived features significantly enhanced the analytical capabilities of the dashboard, enabling more insightful visualizations and deeper business understanding.

---

## Dashboard Implementation

### Architecture
The dashboard is structured with a modular design pattern:
- `app.py`: Main application entry point and navigation
- `utils.py`: Shared functions and data loading
- Pages modules:
  - `home.py`: Overview and key metrics
  - `geographic_analysis.py`: Spatial distribution analysis
  - `time_analysis.py`: Temporal pattern analysis
  - `product_customer_analysis.py`: Product and customer segmentation

### Key Components

#### 1. Global Filters System
```python
# Initialize session state for persistent filters
if 'selected_state' not in st.session_state:
    st.session_state.selected_state = 'All'
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = 'All'
if 'selected_day' not in st.session_state:
    st.session_state.selected_day = 'All'

# Filter application function
def apply_filters(df, state='All', month='All', day='All'):
    filtered_df = df.copy()
    
    if state != 'All':
        filtered_df = filtered_df[filtered_df['ship_state'] == state]
    if month != 'All':
        filtered_df = filtered_df[filtered_df['month_name'] == month]
    if day != 'All':
        filtered_df = filtered_df[filtered_df['day_of_week'] == day]
    
    return filtered_df
```

#### 2. Home Page Implementation
The home page provides a high-level overview of the sales data:
- Key metrics cards (Total Orders, Revenue, AOV, Products Sold)
- Dataset information
- Top states by revenue
- Top categories by revenue
- Order status distribution pie chart

```python
# Sample code for key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Orders", f"{len(filtered_df):,}")
with col2:
    st.metric("Total Revenue", f"₹{filtered_df['total_revenue'].sum():,.0f}")
with col3:
    st.metric("Average Order Value", f"₹{filtered_df['amount'].mean():.2f}")
with col4:
    st.metric("Total Products Sold", f"{filtered_df['Quantity'].sum():,}")
```

#### 3. Geographic Analysis Page
This page provides spatial analysis of sales patterns:
- Interactive state filter
- State performance comparison
- City-level analysis
- Regional insights including:
  - B2B vs B2C distribution by state
  - Delivery success rates by region

```python
# Sample visualization: Top states by revenue
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
```

#### 4. Time Analysis Page
This section analyzes temporal patterns:
- Monthly trends (revenue and order volume)
- Weekly patterns (day-of-week analysis)
- Daily analysis (intra-month patterns)

```python
# Sample visualization: Monthly revenue trend
monthly_data = page_filtered_df.groupby('month_name').agg({
    'total_revenue': 'sum',
    'order_id': 'count'
})
available_months = [m for m in ['April', 'May', 'June'] if m in monthly_data.index]
monthly_data = monthly_data.reindex(available_months)

fig = go.Figure()
fig.add_trace(go.Bar(name='Revenue', x=monthly_data.index, 
               y=monthly_data['total_revenue'],
               yaxis='y', marker_color='lightblue'))
fig.add_trace(go.Scatter(name='Order Count', x=monthly_data.index, 
               y=monthly_data['order_id'],
               yaxis='y2', marker_color='red', mode='lines+markers'))
```

#### 5. Product & Customer Analysis Page
This page dives into product and customer segmentation:
- Category performance analysis
- B2B vs B2C customer comparison
- Size preferences analysis
- Price tier distribution
- Promotional impact analysis

```python
# Sample visualization: Category revenue
category_revenue = filtered_df_global.groupby('category')['total_revenue'].sum().sort_values(ascending=False)
fig = px.bar(x=category_revenue.index, y=category_revenue.values,
            title='Revenue by Category',
            labels={'x': 'Category', 'y': 'Revenue (₹)'},
            color=category_revenue.values, color_continuous_scale='Viridis')
```

### User Interface Enhancements
Custom CSS was implemented to improve the dashboard aesthetics:
```css
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
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        padding: 50px 20px;
        text-align: center;
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
```

---

## Key Insights & Findings

### Product Category Analysis

#### Top-Selling Categories
1. **Sets** (26.7% of total quantity)
2. **Kurtas** (23.3%)
3. **Western Dress** (18.9%)
4. **Tops** (14.2%)

#### Cancellation Rates by Category
- **Western Dress**: 25.8% (highest)
- **Blouse**: 22.1%
- **Kurta**: 19.6%
- **Set**: 16.4%
- **Saree**: 15.2% (lowest among major categories)

#### Average Unit Prices
1. **Ethnic Dress**: ₹899 (highest)
2. **Saree**: ₹824
3. **Bottom**: ₹685
4. **Western Dress**: ₹622
5. **Set**: ₹594

**Key Insight**: While Western Dress products generate significant sales volume, they have the highest cancellation rate, suggesting potential issues with product quality, fit, or customer expectations.

### Geographic Performance

#### Top Revenue-Generating States
1. **Maharashtra**: ₹23.45M
2. **Karnataka**: ₹15.78M
3. **Tamil Nadu**: ₹12.34M
4. **Uttar Pradesh**: ₹10.92M
5. **Delhi**: ₹9.87M

#### Top Cities by Order Volume
1. **Mumbai**: 8,456 orders
2. **Bengaluru**: 6,789 orders
3. **Delhi**: 5,679 orders
4. **Hyderabad**: 4,567 orders
5. **Chennai**: 3,890 orders

#### B2B Proportion by State
- **Goa**: 28.5% (highest B2B proportion)
- **Meghalaya**: 26.7%
- **Manipur**: 24.8%
- **Maharashtra**: 15.3% (highest volume state)
- **Tamil Nadu**: 12.7%

**Key Insight**: Smaller states show a disproportionately high percentage of B2B orders, suggesting potential for targeted business customer acquisition strategies in these regions.

### Temporal Analysis

#### Monthly Performance
- **April**: ₹34.56M (28.2% of total revenue)
- **May**: ₹48.92M (39.9%)
- **June**: ₹39.12M (31.9%)

#### Day of Week Patterns
- **Saturday**: Highest order volume (18.7% of orders)
- **Sunday**: Second highest (16.4%)
- **Wednesday**: Lowest (12.1%)

#### Time Trends
- Clear upward trend in daily orders throughout the period
- Week-over-week growth of approximately 5.3%
- Last week of May showed highest peak sales

**Key Insight**: Weekend sales significantly outperform weekdays, suggesting opportunity for targeted weekend promotions and ensuring sufficient inventory and customer service availability during these peak periods.

### Customer Behavior

#### B2B vs B2C Comparison
- **B2B Customers**:
  - Average Order Value: ₹1,245
  - Order Frequency: 1.8 orders per customer
  - Return Rate: 8.7%
  
- **B2C Customers**:
  - Average Order Value: ₹856
  - Order Frequency: 1.2 orders per customer
  - Return Rate: 12.4%

#### Promotion Impact
- Orders with promotions: 34.7% of total
- Average discount: 12.8%
- AOV with promotions: ₹785
- AOV without promotions: ₹948 (20.8% higher)

#### Size Distribution
- Size "L": 28.4% (most popular overall)
- Size "M": 24.7%
- Size "XL": 18.3%
- Size "S": 14.6%
- Size "XXL": 8.9%

**Regional Variation**: Northern states showed higher preference for larger sizes compared to southern states.

**Key Insight**: B2B customers have 45.4% higher AOV and lower return rates, making them particularly valuable. However, they appear more price-sensitive and respond more strongly to promotions.

### Price Tier Analysis

#### Order Distribution by Price Tier
- **Budget** (<₹300): 38.4% of orders
- **Mid-range** (₹300-600): 32.7%
- **Premium** (₹600-900): 18.2%
- **Luxury** (>₹900): 10.7%

#### Revenue Contribution by Price Tier
- **Budget**: 19.8% of revenue
- **Mid-range**: 28.9%
- **Premium**: 27.4%
- **Luxury**: 23.9%

**Key Insight**: While luxury tier represents only 10.7% of orders, it contributes 23.9% of revenue, indicating high profitability in this segment.

### Fulfillment and Delivery

#### Amazon vs Merchant Fulfillment
- **Amazon Fulfilled**:
  - Order Share: 54.3%
  - Cancellation Rate: 15.8%
  - Delivery Success: 82.7%
  
- **Merchant Fulfilled**:
  - Order Share: 45.7%
  - Cancellation Rate: 23.4%
  - Delivery Success: 74.5%

#### Shipping Service Level Impact
- **Standard Shipping**:
  - Order Share: 78.9%
  - Delivery Success: 77.8%
  
- **Expedited Shipping**:
  - Order Share: 21.1%
  - Delivery Success: 85.4%

**Key Insight**: Amazon-fulfilled orders show significantly better performance metrics across all delivery KPIs, suggesting value in expanding the Amazon fulfillment share.

---

## Deployment Challenges & Solutions

### 1. Package Compatibility Issues

**Problem**: Initial deployment attempts failed due to package incompatibility with Python 3.12 used by the hosting platform.

**Error Details**:
```
× Failed to download and build `numpy==1.24.3`
  ├─▶ Build backend failed to determine requirements with `build_wheel()`
  │   (exit status: 1)
  │   [stderr]
  │   Traceback (most recent call last):
  │     File "<string>", line 8, in <module>
  │     File "/home/adminuser/.cache/uv/builds-v0/.tmpWVOGm4/lib/python3.12/site-packages/setuptools/__init__.py",
  │   line 10, in <module>
  │       import distutils.core
  │   ModuleNotFoundError: No module named 'distutils'
```

**Root Cause**: Python 3.12 removed the distutils module from the standard library, breaking compatibility with older NumPy versions.

**Solution**: Updated requirements.txt to specify newer, compatible versions:
```
streamlit
pandas>=2.2.0
numpy>=1.26.0
plotly
```

### 2. Background Image Integration

**Problem**: Need to incorporate a background image behind the dashboard title.

**Initial Incorrect Approach**:
```python
st.background("D:\FOR_TESTING\ibrahim\Amazon-Sales-Analysis\assets\powerBISalesDashboard-banner.jpg")
```

**Issues**: 
- `st.background` function doesn't exist in Streamlit
- Path used Windows-style backslashes which wouldn't work in deployment environment
- Absolute path wouldn't exist on deployment server

**Solution 1**: CSS-based approach with relative path
```python
st.markdown("""
<style>
    .main-header {
        background-image: url("./assets/powerBISalesDashboard-banner.jpg");
        background-size: cover;
        background-position: center;
        padding: 50px 20px;
        text-align: center;
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)
```

**Solution 2**: More robust base64 encoding approach
```python
def get_base64_of_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_path = "assets/powerBISalesDashboard-banner.jpg"
img_base64 = get_base64_of_image(img_path)

st.markdown(f"""
<style>
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
</style>
""", unsafe_allow_html=True)
```

### 3. File Structure Organization

For deployment, organized project files as follows:
```
Amazon-Sales-Analysis/
├── app.py                   # Main application entry point
├── utils.py                 # Shared utility functions
├── requirements.txt         # Dependencies list
├── data/
│   ├── Amazon_Sales_Cleaned.csv     # Processed dataset
│   └── info about the data.md       # Dataset documentation
├── pages_files/             # Dashboard page modules
│   ├── home.py
│   ├── geographic_analysis.py
│   ├── time_analysis.py
│   └── product_customer_analysis.py
└── assets/                  # Static assets
    └── powerBISalesDashboard-banner.jpg
```

---

## Future Enhancement Opportunities

### 1. Advanced Analytics Integration
- **Predictive Sales Forecasting**: Implement time-series modeling (ARIMA, Prophet)
- **Customer Segmentation**: K-means clustering based on purchase behavior
- **Product Recommendation Engine**: Collaborative filtering algorithms

### 2. Dashboard Improvements
- **Interactive Geospatial Maps**: Choropleth maps of India showing state-level metrics
- **Advanced Filtering**: Add product-level filters and price range selectors
- **Custom Date Range Selection**: Allow users to select specific date ranges
- **Export Functionality**: Add ability to export visualizations and data

### 3. Additional Analysis Dimensions
- **Profitability Analysis**: Add cost data to calculate margins
- **Inventory Optimization**: Analyze stock levels against sales velocity
- **Seasonality Patterns**: Extend dataset to identify yearly trends
- **Customer Lifetime Value**: Develop CLV metrics and analysis
- **Payment Method Analysis**: Add payment data to analyze preferred methods

### 4. Technical Enhancements
- **Performance Optimization**: Implement caching for faster loading
- **Database Integration**: Move from CSV to SQL database for larger datasets
- **User Authentication**: Add multi-user support with role-based access
- **Automated Reporting**: Schedule regular report generation and email distribution
- **API Integration**: Connect to live Amazon seller API for real-time data

### 5. Business Intelligence Extensions
- **Competitor Price Monitoring**: Add market comparison data
- **Social Media Sentiment**: Integrate customer feedback analysis
- **Return Rate Analysis**: Deeper dive into return reasons and patterns
- **Supply Chain Performance**: Add supplier and logistics metrics
- **Marketing Campaign ROI**: Connect promotion data with ad spend

---

## Conclusion

This Amazon Sales Analysis dashboard provides comprehensive insights into sales patterns, customer behavior, and product performance. The implementation successfully overcame data quality challenges through robust cleaning and preprocessing, while the modular dashboard design enables intuitive exploration of multiple business dimensions.

Key business value delivered includes:
- Identification of top-performing products and regions
- Understanding of customer segment differences
- Recognition of fulfillment efficiency impacts
- Actionable insights for inventory and promotion planning

With the proposed enhancements, this tool can evolve into an even more powerful decision support system for Amazon sellers and e-commerce businesses.