# 📊 Sales Analysis Dashboard

A comprehensive sales analytics dashboard built with Streamlit and Plotly for visualizing Acme Corporation's performance, trends, and revenue insights.

## 🌐 Live Demo

Access the dashboard at: [https://sales-analysis-dashboard-acme-iki.streamlit.app](https://sales-analysis-dashboard-acme-iki.streamlit.app)

## 🚀 Features

### Interactive Filters

- **Year**: Filter data by specific year or view all years
- **Month**: Analyze monthly performance or aggregate view
- **US Region**: Regional analysis (East, West, Central, South)
- **Channel**: Channel-specific insights (Distributor, Online, Wholesale)

### Key Performance Indicators (KPIs)

The dashboard displays five essential metrics:

- 💰 **Total Revenue**: Aggregate sales revenue
- 📈 **Total Profit**: Total profit generated
- 📊 **Profit Margin**: Percentage profit margin
- 🛒 **Total Orders**: Number of orders processed
- 🤑 **Revenue per Order**: Average order value

## 📈 Visualizations

### 1. Executive Overview & Trends

#### Monthly Revenue Rhythm

- **Type**: Line chart with spline interpolation
- **Purpose**: Uncover seasonality peaks and revenue patterns
- **Features**: Month-over-month revenue tracking with markers

#### Profit Pulse

- **Type**: Line chart with spline interpolation
- **Purpose**: Track monthly earnings momentum
- **Features**: Visualizes profit trends across months

#### Order Value Spectrum

- **Type**: Histogram (50 bins)
- **Purpose**: Map customer spending tiers
- **Features**: Distribution of order values to identify spending patterns

#### High-Margin Price Bands

- **Type**: Scatter plot (WebGL optimized)
- **Purpose**: Product positioning analysis
- **Features**:
  - Price vs. Profit Margin visualization
  - Interactive hover showing product details
  - Lasso selection enabled for detailed analysis

### 2. Product & Channel Performance

#### Revenue Champions

- **Type**: Horizontal bar chart
- **Purpose**: Identify best-selling products driving growth
- **Features**: Top 10 products by revenue with formatted values

#### High-Margin Heroes

- **Type**: Horizontal bar chart
- **Purpose**: Highlight most efficient products to sell
- **Features**: Top 10 products by profit margin percentage

#### Strategic Product Position

- **Type**: Scatter plot
- **Purpose**: Revenue vs. Profit Margin analysis
- **Features**:
  - Customer-level analysis
  - Interactive lasso selection
  - Identifies high-value, high-margin opportunities

#### Channel Analysis (3 Donut Charts)

1. **Channel Revenue Play**: Revenue distribution by channel
2. **Profit Pipeline**: Profit distribution by channel
3. **Channel Efficiency Score**: Margin per sale by channel

**Features**:

- 70% hole (donut style)
- Custom color palette
- Percentage and value labels
- Horizontal legend positioning

### 3. Geographic & Customer Insights

#### US Revenue Map

- **Type**: Choropleth map
- **Purpose**: State-level revenue visualization
- **Features**:
  - Inferno color scale
  - Theme-aware (dark/light mode)
  - Interactive state-level details
  - Custom color bar positioning

#### Top 5 Analysis

Three horizontal bar charts showing:

1. **Top Customers by Revenue**: Highest revenue-generating customers
2. **Top Customers by Profit Margin**: Most profitable customer relationships
3. **Top States by Revenue**: Highest-performing states

#### Bottom 5 Analysis

Three horizontal bar charts showing:

1. **Bottom Customers by Revenue**: Lowest revenue customers
2. **Bottom Customers by Margin**: Least profitable relationships
3. **Bottom States by Revenue**: Underperforming states

#### Regional Performance (2 Donut Charts)

1. **Total Revenue by Region**: Revenue split across US regions
2. **Profit Margin by Region**: Regional profitability comparison

## 🛠️ Technical Stack

### Core Libraries

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations (Graph Objects & Express)
- **streamlit-extras**: Enhanced metric card styling

### File Structure

```
.
├── app.py                 # Main Streamlit application
├── components.py          # Chart class with all visualization methods
├── data/
│   └── sales_data.csv    # Sales data source
└── README.md             # This file
```

## 📊 Data Schema

The application expects a CSV file with the following columns:

- `order_date`: Order timestamp
- `order_month_name`: Month name (e.g., "January")
- `order_month_num`: Month number (1-12)
- `order_number`: Unique order identifier
- `revenue`: Order revenue
- `profit`: Order profit
- `profit_margin_pct`: Profit margin percentage
- `unit_price`: Product unit price
- `product_name`: Product name
- `customer_name`: Customer name
- `state_name`: Full state name
- `state`: State abbreviation (for choropleth map)
- `us_region`: US region (East, West, Central, South)
- `channel`: Sales channel (Distributor, Online, Wholesale)

## 🎨 Design System

### Color Palette

- Primary: `#7161EF` (Purple)
- Secondary: `#12239e` (Dark Blue)
- Accent: `#ccff33` (Lime)
- Neutral: `#f5f5f5` (Light Gray)

### Chart Styling

- **Height**: Standardized at 300px (trends), 450px (donuts), 500px (comparisons)
- **Opacity**: 0.6-0.85 for markers and fills
- **Line Shape**: Spline for smooth trend lines
- **Text Templates**: Formatted currency and percentages
- **Bar Gap**: 0.2 for histogram spacing

## 📝 Class Methods Reference

### Chart Class

#### Data Management

- `__init__(csv_file)`: Initialize with CSV data
- `data_preprocessing()`: Convert order_date to datetime
- `filter_data(year, month, us_region, channel)`: Apply filters

#### Filter Options

- `year()`: Get available years
- `month()`: Get available months
- `us_region()`: Get available regions
- `channel()`: Get available channels

#### KPI Calculations

- `compute_kpis()`: Calculate all five KPI metrics

#### Visualization Methods

- `monthy_revenue_rhythm()`: Monthly revenue line chart
- `profit_pulse()`: Monthly profit line chart
- `order_value_spectrum()`: Order value histogram
- `high_margin_price_bands()`: Price vs. margin scatter
- `revenue_chamption()`: Top 10 products by revenue
- `high_margin_heros()`: Top 10 products by margin
- `stratetic_profit()`: Customer revenue vs. margin scatter
- `channel_df()`: Channel aggregation data
- `channel_chart()`: Generic donut chart for channels
- `top_customer_revenue()`: Top 5 customers by revenue
- `top_customer_profit_margin()`: Top 5 customers by margin
- `top_state_revenue()`: Top 5 states by revenue
- `bottom_customer_revenue()`: Bottom 5 customers by revenue
- `bottom_customer_profit_margin()`: Bottom 5 customers by margin
- `bottom_state_revenue()`: Bottom 5 states by revenue
- `revenue_region()`: Revenue by region donut chart
- `profit_region()`: Profit margin by region donut chart
- `us_map_reveue()`: US choropleth revenue map

## 🎯 Use Cases

1. **Executive Reporting**: High-level KPIs and trend analysis
2. **Product Strategy**: Identify revenue champions and margin leaders
3. **Channel Optimization**: Understand channel efficiency and profitability
4. **Geographic Expansion**: Identify growth opportunities by state/region
5. **Customer Management**: Prioritize high-value relationships

## 🔧 Customization

### Adding New Visualizations

1. Add a new method to the `Chart` class in `components.py`
2. Follow the existing pattern: filter data → aggregate → create figure
3. Use consistent styling (colors, fonts, heights)
4. Add to `app.py` in the appropriate tab

### Modifying Filters

Update the filter methods in the `Chart` class and add corresponding selectbox in the sidebar.

### Changing Theme

Streamlit automatically adapts to light/dark themes. The US map includes theme detection:

```python
st.get_option("theme.base")
```

## 📄 License

This project is provided as-is for internal use at Acme Corporation.

## 🤝 Contributing

For questions or improvements, please contact the development team.

---

**Built with ❤️ using Streamlit and Plotly**
