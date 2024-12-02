import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dữ liệu
data = pd.read_csv('../getData/data/product_data.csv')

st.title("Tìm kiếm và Lọc sản phẩm Robot hút bụi")

# Bộ lọc cơ bản
st.sidebar.header("Bộ lọc sản phẩm")

# Thương hiệu
brand_filter = st.sidebar.multiselect("Chọn thương hiệu", options=data['Brand'].unique(), default=data['Brand'].unique())

# Khoảng giá
price_min, price_max = st.sidebar.slider("Chọn khoảng giá", float(data['Price'].min()), float(data['Price'].max()), (100.0, 500.0))

# Xếp hạng
rating_filter = st.sidebar.slider("Chọn mức xếp hạng trung bình", 0.0, 5.0, (3.0, 5.0))

# Tìm kiếm theo từ khóa
keyword = st.text_input("Tìm kiếm sản phẩm theo tên", value="")

# Tính năng
features = st.sidebar.multiselect("Chọn tính năng đặc biệt", options=["Self-Charging", "Smart Mapping", "Mop", "Alexa Compatible", "Edge Cleaning"])

# Lọc dữ liệu
filtered_data = data[
    (data['Brand'].isin(brand_filter)) &
    (data['Price'] >= price_min) &
    (data['Price'] <= price_max) &
    (data['Rating Average'] >= rating_filter[0]) &
    (data['Rating Average'] <= rating_filter[1])
]

if keyword:
    filtered_data = filtered_data[filtered_data['Title'].str.contains(keyword, case=False)]

if features:
    filtered_data = filtered_data[filtered_data['Feature Bullets'].apply(lambda x: any(feature in x for feature in features))]

# Hiển thị kết quả lọc
st.header("Kết quả tìm kiếm")
st.write(filtered_data[['ASIN', 'Title', 'Brand', 'Price', 'Rating Average', 'Feature Bullets']])

# Biểu đồ số lượng sản phẩm theo thương hiệu
st.header("Phân phối số lượng sản phẩm theo thương hiệu")
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='Brand', order=filtered_data['Brand'].value_counts().index, ax=ax)
ax.set_title("Số lượng sản phẩm theo thương hiệu")
st.pyplot(fig)

# Biểu đồ phân phối giá của các sản phẩm được lọc
st.header("Phân phối giá của các sản phẩm được lọc")
fig, ax = plt.subplots()
sns.histplot(filtered_data['Price'], bins=20, kde=True, ax=ax)
ax.set_title("Phân phối giá")
st.pyplot(fig)

# Biểu đồ phân phối xếp hạng trung bình
st.header("Phân phối xếp hạng trung bình của các sản phẩm được lọc")
fig, ax = plt.subplots()
sns.histplot(filtered_data['Rating Average'], bins=10, kde=True, ax=ax)
ax.set_title("Phân phối xếp hạng trung bình")
st.pyplot(fig)
