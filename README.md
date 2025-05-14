# Amazon Sales Analysis

## Deployment :-  

https://amazon-sales-analysis-in-india.streamlit.app/

## Presentation :-
https://www.canva.com/design/DAGnb7QmU-Y/gFd26tSPQlzGFGrGJ2kFmw/edit?utm_content=DAGnb7QmU-Y&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Project Overview
This project analyzes Amazon India's sales data to uncover insights about order patterns, customer behavior, product performance, and geographic trends. The analysis covers data from April to June 2022, containing 128,975 order records.

## Dataset Information
- **Source**: Amazon India Sales Report from Kaggle
- **Time Period**: April - June 2022
- **Records**: 128,975 orders
- **Key Features**: Order details, product information, shipping data, customer type, and financial metrics

## Data Cleaning Process

### 1. Column Name Standardization
**What**: Converted all column names to lowercase and replaced spaces/hyphens with underscores
**Why**: Ensures consistent naming convention and easier programmatic access
```python
df.columns = df.columns.str.strip()
df.columns = df.columns.str.lower().str.replace(' ', '_')
df.columns = df.columns.str.lower().str.replace('-', '_')
```

### 2. Handling Missing Addresses
**What**: Dropped 33 rows with completely missing address information
**Why**: These represented only 0.026% of data and couldn't be imputed meaningfully
**Result**: Maintained 99.97% of the original data

### 3. Removing Unnecessary Columns
**What**: Dropped 'unnamed:_22' and 'fulfilled_by' columns
**Why**: These columns contained no useful information for analysis

### 4. Data Type Corrections
**What**: 
- Converted 'date' to datetime format
- Changed 'ship_postal_code' to integer
- Renamed 'qty' to 'Quantity' for consistency
**Why**: Proper data types enable time-series analysis and consistent naming improves code readability

### 5. Location Data Standardization
**What**: Cleaned and standardized state and city names
**Why**: Different spellings and variations of the same locations were creating artificial duplicates
**Result**: 
- States reduced from 69 to 47 unique values
- Cities reduced from 8,955 to a more manageable number
**Examples**:
- 'delhi', 'new delhi', 'Delhi' → 'delhi'
- 'rajasthan', 'rajshthan', 'RJ' → 'rajasthan'

### 6. Currency Standardization
**What**: Filled missing currency values with 'INR'
**Why**: All transactions were in Indian Rupees; missing values were data entry errors

### 7. Promotion and Status Handling
**What**: 
- Replaced missing promotion IDs with 'No Promotion'
- Set courier status to 'Cancelled' when order status was 'Cancelled'
**Why**: Creates clear categories for analysis and ensures data consistency

### 8. Amount Value Imputation
**What**: Filled missing amount values using median unit price by product style
**Why**: Preserves pricing patterns while handling missing financial data
**Method**: Calculated median unit price per style, then multiplied by quantity

## Feature Engineering

### Time-Based Features
1. **month**: Numerical month (4-6)
2. **month_name**: Full month name (April, May, June)
3. **day_of_week**: Day name (Monday-Sunday)
4. **day_of_month**: Day number (1-31)
5. **week_of_year**: Week number

### Business Features
1. **has_promotion**: Boolean indicating promotion usage
2. **price_tier**: Categorized prices into Budget (<₹300), Mid-range (₹300-600), Premium (₹600-900), Luxury (>₹900)
3. **unit_price**: Calculated as amount/quantity
4. **customer_type**: Converted B2B boolean to 'B2B'/'B2C' text
5. **total_revenue**: Calculated as amount × quantity

## Key Findings from Analysis

### 1. Top Product Categories
- **Set** items are the best-selling category with highest quantity sold
- **kurta** follows as the second most popular category
- Women's ethnic wear dominates the sales

### 2. Cancellation Insights
- Overall cancellation rate varies by category
- Higher-priced items tend to have lower cancellation rates
- Categories with size issues show higher cancellations

### 3. Geographic Performance
- **Maharashtra** generates the highest revenue
- **Karnataka** follows as second-highest revenue state
- Top 5 states account for majority of total revenue

### 4. Promotion Impact
- Orders with promotions have higher average order values
- Promotion usage varies by customer type
- B2B customers use promotions less frequently than B2C

### 5. Size Preferences
- **M (Medium)** is the most popular size across categories
- **L (Large)** and **XL** follow in popularity
- Size preferences vary significantly by product category

### 6. Revenue Trends
- May shows peak revenue among the three months
- Weekend sales are generally lower than weekdays
- End-of-month periods show increased order volumes

### 7. Customer Segmentation
- B2B customers have higher average order values (AOV)
- B2C customers represent the majority of orders
- B2B proportion varies significantly by state

### 8. Pricing Analysis
- Kurtas have highest average unit prices
- Budget tier represents largest order volume
- Premium and luxury tiers have better completion rates

### 9. Operational Insights
- Standard shipping is preferred over expedited
- Amazon fulfillment shows lower cancellation rates than merchant
- Delivery success rate is higher for expedited shipping

### 10. City Performance
- Mumbai leads in both order volume and revenue
- Bangalore shows highest average order values
- Metro cities dominate the top 10 revenue generators

## Technical Implementation

### Dashboard Architecture
- **Framework**: Streamlit for interactive web application
- **Visualization**: Plotly for dynamic charts
- **State Management**: Session state for global filters
- **Modular Design**: Separate pages for different analysis aspects

### Dashboard Features
1. **Global Filters**: State, Month, and Day filters applied across all pages
2. **Geographic Analysis**: State and city performance metrics
3. **Time Analysis**: Monthly, weekly, and daily patterns
4. **Product Analysis**: Category, size, and price tier insights
5. **Customer Analysis**: B2B vs B2C segmentation

## Business Recommendations

1. **Inventory Management**: Focus on medium and large sizes for ethnic wear
2. **Marketing Strategy**: Target promotions during weekdays for better conversion
3. **Geographic Expansion**: Leverage success in Maharashtra model for other states
4. **Customer Retention**: Address high cancellation categories with better product descriptions
5. **Pricing Strategy**: Maintain focus on budget and mid-range tiers while improving premium tier services

## Conclusion
The analysis reveals strong geographic concentration, clear customer segmentation patterns, and seasonal trends. The insights provide actionable recommendations for inventory, marketing, and operational improvements.
