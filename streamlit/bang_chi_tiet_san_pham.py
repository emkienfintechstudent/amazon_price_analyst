import streamlit as st
import pandas as pd

# Load dữ liệu
data = pd.read_csv('../getData/data/product_data.csv')

# Set title
st.title("Bảng chi tiết sản phẩm Robot hút bụi")

# 1. Tùy chỉnh cột hiển thị
st.sidebar.header("Tùy chỉnh hiển thị")
columns = st.sidebar.multiselect(
    "Chọn các cột muốn hiển thị:",
    options=data.columns,
    default=['ASIN', 'Title', 'Brand', 'Price', 'Rating Average', 'Annual Unit Sales']
)

# 2. Tìm kiếm từ khóa
st.sidebar.header("Tìm kiếm sản phẩm")
search_keyword = st.sidebar.text_input("Tìm kiếm theo tên sản phẩm hoặc thương hiệu:")

# 3. Lọc dữ liệu
st.sidebar.header("Lọc dữ liệu")
brands = st.sidebar.multiselect("Chọn thương hiệu:", options=data['Brand'].unique(), default=data['Brand'].unique())
price_min, price_max = st.sidebar.slider("Khoảng giá:", float(data['Price'].min()), float(data['Price'].max()), (100.0, 500.0))
rating_min, rating_max = st.sidebar.slider("Khoảng xếp hạng:", 0.0, 5.0, (3.0, 5.0))
sales_min, sales_max = st.sidebar.slider("Doanh số hàng năm:", float(data['Annual Unit Sales'].min()), float(data['Annual Unit Sales'].max()), (0.0, 50000.0))

# Áp dụng bộ lọc
filtered_data = data[
    (data['Brand'].isin(brands)) &
    (data['Price'] >= price_min) &
    (data['Price'] <= price_max) &
    (data['Rating Average'] >= rating_min) &
    (data['Rating Average'] <= rating_max) &
    (data['Annual Unit Sales'] >= sales_min) &
    (data['Annual Unit Sales'] <= sales_max)
]

if search_keyword:
    filtered_data = filtered_data[filtered_data['Title'].str.contains(search_keyword, case=False) | 
                                  filtered_data['Brand'].str.contains(search_keyword, case=False)]

# Hiển thị bảng
st.header("Bảng chi tiết sản phẩm")
st.dataframe(filtered_data[columns])

# 4. Sắp xếp dữ liệu (tùy chỉnh)
st.header("Sắp xếp dữ liệu")
sort_by = st.selectbox("Sắp xếp theo cột:", options=columns)
ascending = st.radio("Thứ tự:", options=["Tăng dần", "Giảm dần"])
filtered_data = filtered_data.sort_values(by=sort_by, ascending=(ascending == "Tăng dần"))

# Hiển thị bảng đã sắp xếp
st.subheader("Bảng sau khi sắp xếp")
st.dataframe(filtered_data[columns])

# 5. Xuất dữ liệu (Tùy chọn)
if st.button("Xuất dữ liệu"):
    filtered_data.to_csv("filtered_data.csv", index=False)
    st.success("Dữ liệu đã được xuất ra file CSV: filtered_data.csv")
