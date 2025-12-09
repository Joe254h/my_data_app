import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="Motorcycle Market Analytics",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem !important;
        color: #1E3A8A !important;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
    }
    
    .sub-header {
        color: #374151 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 0.5rem;
        margin-top: 2rem !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(45deg, #1E3A8A, #3B82F6) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem !important;
        border-radius: 10px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    .dataframe {
        border-radius: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    .info-box {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-header'>🏍️ Motorcycle Market Analytics Dashboard</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2849/2849734.png", width=100)
    st.markdown("### 📊 Dashboard Controls")
    
    # Data source selection
    st.markdown("#### 📂 Select Data Files")
    selected_files = st.multiselect(
        "Choose motorcycle datasets to analyze:",
        ['Motorcycles 1', 'Motorcycles 2', 'Motorcycles 3', 'Motorcycles 4', 'Motorcycles 5'],
        default=['Motorcycles 1', 'Motorcycles 2']
    )
    
    # Analysis focus
    st.markdown("#### 🔍 Analysis Focus")
    analysis_type = st.selectbox(
        "Select analysis type:",
        ["Price Analysis", "Brand Comparison", "Year Trends", "Location Insights", "Complete Overview"]
    )
    
    # Visualization settings
    st.markdown("#### 🎨 Visualization Settings")
    chart_theme = st.selectbox("Chart Theme", ["plotly", "plotly_white", "plotly_dark", "seaborn"])
    
    # Date range filter (if applicable)
    st.markdown("#### 📅 Filter by Year")
    year_range = st.slider("Select year range:", 2000, 2024, (2015, 2024))
    
    st.markdown("---")
    st.markdown("#### 📈 About")
    st.info("""
    This dashboard analyzes motorcycle market data from Expat-Dakar.
    Explore pricing trends, brand popularity, and market insights.
    """)

# Data loading function with caching
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Basic data cleaning
        # Clean price column if it exists
        if 'price' in df.columns:
            # Handle various price formats
            df['price'] = df['price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Clean year column if it exists
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
        
        # Clean brand column if it exists
        if 'brand' in df.columns:
            df['brand'] = df['brand'].astype(str).str.strip().str.title()
            
        return df
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        return None

# Dictionary of data files
data_files = {
    'Motorcycles 1': '/home/joetech/Documents/Data_Prep/Module_03-20251106T073326Z-1-001/data/motos_scooters1.csv',
    'Motorcycles 2': '/home/joetech/Documents/Data_Prep/Module_03-20251106T073326Z-1-001/data/motos_scooters2.csv',
    'Motorcycles 3': '/home/joetech/Documents/Data_Prep/Module_03-20251106T073326Z-1-001/data/motos_scooters3.csv',
    'Motorcycles 4': '/home/joetech/Documents/Data_Prep/Module_03-20251106T073326Z-1-001/data/motos_scooters4.csv',
    'Motorcycles 5': '/home/joetech/Documents/Data_Prep/Module_03-20251106T073326Z-1-001/data/motos_scooters5.csv'
}

# Load selected data
all_data = []
for file_name in selected_files:
    if file_name in data_files:
        df = load_data(data_files[file_name])
        if df is not None:
            df['dataset'] = file_name
            all_data.append(df)

if not all_data:
    st.warning("⚠️ Please select at least one dataset from the sidebar.")
    st.stop()

# Combine all selected datasets
combined_df = pd.concat(all_data, ignore_index=True)

# Main dashboard layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Listings", f"{len(combined_df):,}", "📊")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if 'price' in combined_df.columns:
        avg_price = combined_df['price'].mean()
        if pd.isna(avg_price):
            avg_price = 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Price", f"${avg_price:,.0f}" if avg_price > 0 else "N/A", "💰")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Price", "N/A", "💰")
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    if 'brand' in combined_df.columns:
        unique_brands = combined_df['brand'].nunique()
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unique Brands", f"{unique_brands}", "🏷️")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unique Brands", "N/A", "🏷️")
        st.markdown('</div>', unsafe_allow_html=True)

with col4:
    if 'year' in combined_df.columns:
        avg_year = combined_df['year'].mean()
        if pd.isna(avg_year):
            avg_year = 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Year", f"{avg_year:.0f}" if avg_year > 0 else "N/A", "📅")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Year", "N/A", "📅")
        st.markdown('</div>', unsafe_allow_html=True)

# Tab layout for different views
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🔍 Detailed Analysis", "📊 Comparisons", "📥 Data Explorer"])

with tab1:
    st.markdown("<h3 class='sub-header'>Market Overview</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'price' in combined_df.columns:
            fig1 = px.histogram(
                combined_df, 
                x='price', 
                nbins=50,
                title='Price Distribution',
                color='dataset',
                template=chart_theme,
                labels={'price': 'Price ($)', 'count': 'Number of Listings'}
            )
            fig1.update_layout(bargap=0.1)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Price data not available for visualization")
    
    with col2:
        if 'brand' in combined_df.columns:
            brand_counts = combined_df['brand'].value_counts().head(10)
            fig2 = px.bar(
                x=brand_counts.index,
                y=brand_counts.values,
                title='Top 10 Brands by Listings',
                color=brand_counts.values,
                color_continuous_scale='Viridis',
                template=chart_theme,
                labels={'x': 'Brand', 'y': 'Number of Listings'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Brand data not available for visualization")

with tab2:
    st.markdown("<h3 class='sub-header'>Detailed Analysis</h3>", unsafe_allow_html=True)
    
    # Initialize filter variables with default values
    selected_brands = []
    year_filter = (2000, 2024)
    price_filter = (0, 100000)
    
    # Interactive filters - only show if columns exist
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'brand' in combined_df.columns:
            brand_options = sorted([str(b) for b in combined_df['brand'].unique() if pd.notna(b)])
            selected_brands = st.multiselect(
                "Filter by Brand:",
                options=brand_options,
                default=brand_options[:3] if len(brand_options) > 3 else brand_options
            )
    
    with col2:
        if 'year' in combined_df.columns:
            # Filter out NaN values
            valid_years = combined_df['year'].dropna()
            if not valid_years.empty:
                min_year = int(valid_years.min())
                max_year = int(valid_years.max())
                year_filter = st.slider(
                    "Filter by Year:",
                    min_value=min_year,
                    max_value=max_year,
                    value=(min_year, max_year)
                )
    
    with col3:
        if 'price' in combined_df.columns:
            # Filter out NaN values
            valid_prices = combined_df['price'].dropna()
            if not valid_prices.empty:
                min_price = int(valid_prices.min())
                max_price = int(valid_prices.max())
                price_filter = st.slider(
                    "Filter by Price ($):",
                    min_value=min_price,
                    max_value=max_price,
                    value=(min_price, max_price)
                )
    
    # Apply filters
    filtered_df = combined_df.copy()
    
    # Apply brand filter if brands are selected
    if 'brand' in filtered_df.columns and selected_brands:
        filtered_df = filtered_df[filtered_df['brand'].isin(selected_brands)]
    
    # Apply year filter if year column exists
    if 'year' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['year'] >= year_filter[0]) & (filtered_df['year'] <= year_filter[1])]
    
    # Apply price filter if price column exists
    if 'price' in filtered_df.columns:
        filtered_df = filtered_df[(filtered_df['price'] >= price_filter[0]) & (filtered_df['price'] <= price_filter[1])]
    
    # Show filtered data metrics
    st.info(f"📊 Showing {len(filtered_df)} listings after applying filters")
    
    # Scatter plot for price vs year
    if 'year' in filtered_df.columns and 'price' in filtered_df.columns:
        # Remove NaN values for plotting
        plot_df = filtered_df.dropna(subset=['year', 'price'])
        if not plot_df.empty:
            fig3 = px.scatter(
                plot_df,
                x='year',
                y='price',
                color='brand' if 'brand' in plot_df.columns else None,
                size='price',
                hover_data=['dataset'] if 'dataset' in plot_df.columns else None,
                title='Price vs Year by Brand',
                template=chart_theme,
                labels={'year': 'Manufacturing Year', 'price': 'Price ($)'}
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("No data available for Price vs Year visualization after filtering")

with tab3:
    st.markdown("<h3 class='sub-header'>Dataset Comparisons</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Compare average prices across datasets
        if 'price' in combined_df.columns and 'dataset' in combined_df.columns:
            dataset_stats = combined_df.groupby('dataset')['price'].agg(['mean', 'count', 'std']).reset_index()
            fig4 = px.bar(
                dataset_stats,
                x='dataset',
                y='mean',
                error_y='std',
                title='Average Price by Dataset',
                color='dataset',
                template=chart_theme,
                labels={'mean': 'Average Price ($)', 'dataset': 'Dataset'}
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Price or dataset information not available for comparison")
    
    with col2:
        # Brand distribution across datasets
        if 'brand' in combined_df.columns and 'dataset' in combined_df.columns:
            brand_dataset = pd.crosstab(combined_df['brand'], combined_df['dataset']).head(10)
            if not brand_dataset.empty:
                fig5 = px.imshow(
                    brand_dataset,
                    title='Top Brands Distribution Across Datasets',
                    labels=dict(x="Dataset", y="Brand", color="Count"),
                    aspect="auto",
                    color_continuous_scale="YlOrRd",
                    template=chart_theme
                )
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.info("No brand distribution data available")
        else:
            st.info("Brand or dataset columns not available")

with tab4:
    st.markdown("<h3 class='sub-header'>Data Explorer</h3>", unsafe_allow_html=True)
    
    # Show raw data with filters
    st.markdown("### 📋 Raw Data Preview")
    
    # Column selector
    if not combined_df.empty:
        available_columns = combined_df.columns.tolist()
        default_columns = available_columns[:min(5, len(available_columns))]
        
        columns = st.multiselect(
            "Select columns to display:",
            options=available_columns,
            default=default_columns
        )
        
        if columns:
            # Pagination
            page_size = st.slider("Rows per page:", 10, 100, 20)
            total_pages = max(1, len(combined_df) // page_size + 1)
            page_number = st.number_input("Page:", min_value=1, max_value=total_pages, value=1)
            
            start_idx = (page_number - 1) * page_size
            end_idx = min(start_idx + page_size, len(combined_df))
            
            st.dataframe(
                combined_df[columns].iloc[start_idx:end_idx],
                use_container_width=True,
                height=400
            )
            
            # Data download
            csv = combined_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="motorcycle_data.csv">💾 Download Full Dataset as CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("No data available to display")

# Additional insights
st.markdown("---")
st.markdown("<h3 class='sub-header'>💡 Key Insights</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 📈 Market Trends")
    if 'year' in combined_df.columns and 'price' in combined_df.columns:
        # Group by year and calculate average price
        yearly_trend = combined_df.groupby('year')['price'].mean().sort_index()
        if len(yearly_trend) > 1:
            latest_trend = "📈 Increasing" if yearly_trend.iloc[-1] > yearly_trend.iloc[-2] else "📉 Decreasing"
            st.markdown(f"**Price Trend:** {latest_trend}")
        else:
            st.markdown("**Price Trend:** Insufficient data")
    else:
        st.markdown("**Price Trend:** Data not available")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 🏆 Top Brands")
    if 'brand' in combined_df.columns:
        brand_counts = combined_df['brand'].value_counts()
        if not brand_counts.empty:
            top_brand = brand_counts.index[0]
            top_count = brand_counts.iloc[0]
            st.markdown(f"**Most Listed:** {top_brand}")
            st.markdown(f"**Listings:** {top_count}")
        else:
            st.markdown("**Most Listed:** No data")
    else:
        st.markdown("**Most Listed:** Brand data not available")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### 💰 Price Range")
    if 'price' in combined_df.columns:
        valid_prices = combined_df['price'].dropna()
        if not valid_prices.empty:
            price_range = f"${valid_prices.min():,.0f} - ${valid_prices.max():,.0f}"
            st.markdown(f"**Range:** {price_range}")
            st.markdown(f"**Median:** ${valid_prices.median():,.0f}")
        else:
            st.markdown("**Range:** No price data")
    else:
        st.markdown("**Range:** Price data not available")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 1rem;'>
    <p>Dashboard created with ❤️ using Streamlit • Data sourced from <a href="https://www.expat-dakar.com/" target="_blank">Expat-Dakar</a></p>
    <p>Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)