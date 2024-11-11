import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('amazon_robot_vacuum_data.csv')

# Summary Statistics
st.title("Dashboard - Phân tích chiến lược giá cho Robot hút bụi Shark AI Ultra")

st.header("1. Thống kê Tổng quan")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Giá trung bình", f"${data['price'].mean():.2f}")
col2.metric("Giá thấp nhất", f"${data['price'].min():.2f}")
col3.metric("Giá cao nhất", f"${data['price'].max():.2f}")
col4.metric("Đánh giá trung bình", f"{data['rating'].mean():.2f}")

# Top Brands
st.header("2. Thương hiệu Phổ biến")
top_brands = data['brand'].value_counts().head(5)
fig, ax = plt.subplots()
sns.barplot(x=top_brands.index, y=top_brands.values, ax=ax)
ax.set_title("Top 5 thương hiệu phổ biến")
st.pyplot(fig)

# Price Distribution
st.header("3. Phân phối Giá")
fig, ax = plt.subplots()
sns.histplot(data['price'], bins=20, kde=True, ax=ax)
ax.set_title("Biểu đồ phân phối giá của các sản phẩm")
st.pyplot(fig)

# Rating Distribution
st.header("4. Phân phối Đánh giá")
fig, ax = plt.subplots()
sns.histplot(data['rating'], bins=10, kde=True, ax=ax)
ax.set_title("Biểu đồ phân phối đánh giá của các sản phẩm")
st.pyplot(fig)

# Price vs Rating
st.header("5. Tương quan giữa Giá và Đánh giá")
fig, ax = plt.subplots()
sns.scatterplot(data=data, x='price', y='rating', hue='brand', ax=ax)
ax.set_title("Tương quan giữa giá và đánh giá")
st.pyplot(fig)
