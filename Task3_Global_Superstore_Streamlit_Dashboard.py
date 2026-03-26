import streamlit as st
import pandas as pd
import plotly.express as px

# Load Dataset with a 'Raw' string to prevent path errors
# Added @st.cache_data so the dashboard loads fast every time you change a filter
@st.cache_data
def load_data():
    path = r"C:/Users/SUPER/OneDrive/Desktop/Jupyter Notebook/Global_Superstore2.csv"
    data = pd.read_csv(path, encoding='latin1')
    data.columns = data.columns.str.strip() # Cleans hidden spaces in column names
    return data

df = load_data()


# Cleaning Data
df.drop_duplicates(inplace=True)


# Dashboard Title
st.set_page_config(page_title="Global Superstore", layout="wide")
st.title("📊 Business Dashboard - Global Superstore")

# SIDEBAR FILTERS (The "Logic Fix")
st.sidebar.header("Dashboard Filters")

region = st.sidebar.selectbox("Select Region", df['Region'].unique())


# Only show Categories available in that Region
cat_options = df[df['Region'] == region]['Category'].unique()
category = st.sidebar.selectbox("Select Category", cat_options)


# ONLY show Sub-Categories that belong to the selected Category
subcat_options = df[(df['Region'] == region) & (df['Category'] == category)]['Sub-Category'].unique()
subcategory = st.sidebar.selectbox("Select Sub-Category", subcat_options)


# Applying Filters
filtered_df = df[
    (df['Region'] == region) &
    (df['Category'] == category) &
    (df['Sub-Category'] == subcategory)
]


# KPIs (Organized in Columns)
col1, col2 = st.columns(2)
with col1:
    st.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
with col2:
    st.metric("📈 Total Profit", f"${filtered_df['Profit'].sum():,.2f}")


# Top 5 Customers (Formatted as a Table)
st.subheader("🏆 Top 5 Customers by Sales")
top_customers = (
    filtered_df.groupby('Customer Name')['Sales']
    .sum()
    .nlargest(5) # Cleaner way to get top 5
    .reset_index()
)
st.table(top_customers)

# Sales by Category
st.subheader("📊 Sales by Category")
sales_chart = filtered_df.groupby('Category')['Sales'].sum().reset_index()
fig_sales = px.bar(sales_chart, x='Category', y='Sales', color='Category', text_auto='.2s')
st.plotly_chart(fig_sales, use_container_width=True)

# Profit by Sub-Category
st.subheader("📈 Profit by Sub-Category")
profit_chart = filtered_df.groupby('Sub-Category')['Profit'].sum().reset_index()
fig_profit = px.bar(profit_chart, x='Sub-Category', y='Profit', color='Sub-Category', text_auto='.2s')
st.plotly_chart(fig_profit, use_container_width=True)


st.markdown("## Conclusion")

st.markdown("""
An interactive dashboard was built using Streamlit to analyze sales and profit data.

### Key Features:
- Dynamic filtering by Region, Category, and Sub-Category
- Real-time KPIs for Sales and Profit
- Identification of top customers
- Visual insights using charts

### Business Impact:
- Helps stakeholders make data-driven decisions
- Identifies high-performing regions and customers
- Improves sales strategy and planning
""")
