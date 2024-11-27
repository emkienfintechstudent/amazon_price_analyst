import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dữ liệu
data = pd.read_csv('../getData/product_data.csv')

# Set title
st.title("Tổng quan thị trường Robot hút bụi")

# 1. Tổng quan

st.header("Tóm tắt thống kê")
st.subheader("Tổng quan")
total_products = len(data)
avg_price = data['Price'].mean()
min_price = data['Price'].min()
max_price = data['Price'].max()
avg_rating = data['Rating Average'].mean()
total_ratings = data['Ratings Total'].sum()
total_sales_weekly = data['Weekly Unit Sales'].sum()
total_sales_monthly = data['Monthly Unit Sales'].sum()
total_sales_annual = data['Annual Unit Sales'].sum()
most_popular_brand = data['Brand'].value_counts().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("Tổng sản phẩm", total_products)
col2.metric("Giá trung bình", f"${avg_price:.2f}")
col3.metric("Đánh giá trung bình", f"{avg_rating:.1f} ⭐")

col4, col5 = st.columns(2)
col4.metric("Giá thấp nhất", f"${min_price:.2f}")
col5.metric("Giá cao nhất", f"${max_price:.2f}")

st.subheader("Doanh số ước tính")
col6, col7= st.columns(2)  # Cột rộng hơn, cân đối

col6.metric("Doanh số tuần", f"{total_sales_weekly:,.0f} sản phẩm")
col7.metric("Doanh số tháng", f"{total_sales_monthly:,.0f} sản phẩm")
st.metric("Doanh số năm", f"{total_sales_annual:,.0f} sản phẩm")
st.subheader("Tổng quan giá")

# Top thương hiệu phổ biến
st.header("Top thương hiệu phổ biến")
print(data.columns)

# 1. Danh sách thương hiệu phổ biến nhất
st.subheader("Danh sách thương hiệu phổ biến nhất")
top_brands_count = data['Brand'].value_counts().head(10)  # Top 10 thương hiệu
st.write("**Top 10 thương hiệu có nhiều sản phẩm máy hút bụi nhất:**")
st.write(pd.DataFrame({
    "Thương hiệu": top_brands_count.index,
    "Số lượng sản phẩm": top_brands_count.values
}))

# 2. Biểu đồ Top 5 thương hiệu
st.subheader("Biểu đồ Top 5 thương hiệu")
top_5_brands = data['Brand'].value_counts().head(5)
fig, ax = plt.subplots()
sns.barplot(x=top_5_brands.index, y=top_5_brands.values, ax=ax, palette="viridis")
ax.set_title("Top 5 thương hiệu phổ biến nhất")
ax.set_ylabel("Số lượng sản phẩm")
ax.set_xlabel("Thương hiệu")
st.pyplot(fig)

# 3.Chi tiết về thương hiệu phổ biến nhất
st.subheader(f"Chi tiết thương hiệu phổ biến nhất: {top_brands_count.index[0]}")
most_popular_brand_data = data[data['Brand'] == top_brands_count.index[0]]
avg_price = most_popular_brand_data['Price'].mean()
avg_rating = most_popular_brand_data['Rating Average'].mean()
total_sales = most_popular_brand_data['Annual Unit Sales'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Giá trung bình", f"${avg_price:.2f}")
col2.metric("Xếp hạng trung bình", f"{avg_rating:.1f} ⭐")
col3.metric("Tổng doanh số", f"{total_sales:,} sản phẩm")


# 5. So sánh xếp hạng trung bình giữa các thương hiệu Top 5
st.subheader("So sánh xếp hạng trung bình của Top 5 thương hiệu")
avg_ratings_top_5 = data[data['Brand'].isin(top_5_brands.index)].groupby('Brand')['Rating Average'].mean().sort_values(ascending=False)
fig, ax = plt.subplots()
sns.barplot(x=avg_ratings_top_5.index, y=avg_ratings_top_5.values, ax=ax, palette="coolwarm")
ax.set_title("Xếp hạng trung bình của Top 5 thương hiệu")
ax.set_ylabel("Xếp hạng trung bình")
ax.set_xlabel("Thương hiệu")
st.pyplot(fig)


# 2. Phân phối giá
st.header("Phân phối giá của Robot hút bụi")
fig, ax = plt.subplots()
sns.histplot(data['Price'], bins=30, kde=True, ax=ax)
ax.set_title("Phân phối giá các sản phẩm")
st.pyplot(fig)

# 3. Phân phối đánh giá
st.header("Phân phối đánh giá và xếp hạng")
fig, ax = plt.subplots()
sns.histplot(data['Rating Average'], bins=10, kde=True, ax=ax)
ax.set_title("Phân phối xếp hạng trung bình của sản phẩm")
st.pyplot(fig)

# 4. Thương hiệu phổ biến
st.header("Thương hiệu phổ biến")
top_brands = data['Brand'].value_counts().head(5)
fig, ax = plt.subplots()
sns.barplot(x=top_brands.index, y=top_brands.values, ax=ax)
ax.set_title("Top 5 thương hiệu phổ biến")
ax.set_ylabel("Số lượng sản phẩm")
st.pyplot(fig)

# 5. Phân khúc giá sản phẩm
st.header("Phân khúc giá sản phẩm")
low_price = data[data['Price'] < 100].shape[0]
mid_price = data[(data['Price'] >= 100) & (data['Price'] <= 500)].shape[0]
high_price = data[data['Price'] > 500].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("Sản phẩm giá thấp (<$100)", low_price)
col2.metric("Sản phẩm giá trung bình ($100-$500)", mid_price)
col3.metric("Sản phẩm giá cao (>$500)", high_price)

# 6. Sản phẩm bán chạy nhất
st.header("Sản phẩm bán chạy nhất")
top_selling = data.sort_values(by="Annual Unit Sales", ascending=False).head(10)
st.write(top_selling[['Title', 'Brand', 'Price', 'Annual Unit Sales']])

# 7. Mối quan hệ giữa giá và đánh giá
st.header("Mối quan hệ giữa Giá và Xếp hạng")
fig, ax = plt.subplots()
sns.scatterplot(data=data, x='Price', y='Rating Average', ax=ax)
ax.set_title("Mối quan hệ giữa giá và xếp hạng")
st.pyplot(fig)

# 8. Bộ lọc tìm kiếm
st.header("Tìm kiếm sản phẩm")
brand_filter = st.selectbox("Chọn thương hiệu", options=data['Brand'].unique())
price_min, price_max = st.slider("Chọn khoảng giá", float(data['Price'].min()), float(data['Price'].max()), (100.0, 500.0))
rating_filter = st.slider("Chọn mức xếp hạng", 0.0, 5.0, (3.0, 5.0))

filtered_data = data[
    (data['Brand'] == brand_filter) &
    (data['Price'] >= price_min) &
    (data['Price'] <= price_max) &
    (data['Rating Average'] >= rating_filter[0]) &
    (data['Rating Average'] <= rating_filter[1])
]

st.write(filtered_data[['Title', 'Brand', 'Price', 'Rating Average', 'Annual Unit Sales']])









