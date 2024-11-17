import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dữ liệu
data = pd.read_csv('../getData/product_data.csv')

st.title("Biểu đồ và Đồ thị - Phân tích Robot hút bụi trên Amazon")

# 1. Phân phối giá
st.header("Phân phối giá của sản phẩm")
fig, ax = plt.subplots()
sns.histplot(data['Price'], bins=30, kde=True, ax=ax)
ax.set_title("Phân phối giá của sản phẩm")
st.pyplot(fig)

# 2. Phân phối xếp hạng
st.header("Phân phối xếp hạng trung bình của sản phẩm")
fig, ax = plt.subplots()
sns.histplot(data['Rating Average'], bins=10, kde=True, ax=ax)
ax.set_title("Phân phối xếp hạng trung bình")
st.pyplot(fig)

# 3. Số lượng sản phẩm theo thương hiệu
st.header("Số lượng sản phẩm theo thương hiệu")
top_brands = data['Brand'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=top_brands.index, y=top_brands.values, ax=ax)
ax.set_title("Số lượng sản phẩm theo thương hiệu")
ax.set_xlabel("Thương hiệu")
ax.set_ylabel("Số lượng sản phẩm")
st.pyplot(fig)

# 4. Tương quan giữa giá và xếp hạng
st.header("Tương quan giữa giá và xếp hạng trung bình")
fig, ax = plt.subplots()
sns.scatterplot(data=data, x='Price', y='Rating Average', hue='Brand', ax=ax)
ax.set_title("Tương quan giữa giá và xếp hạng")
ax.set_xlabel("Giá ($)")
ax.set_ylabel("Xếp hạng trung bình")
st.pyplot(fig)

# 5. Phân tích doanh số bán hàng
st.header("Doanh số bán hàng hàng năm")
fig, ax = plt.subplots()
sns.lineplot(data=data, x='Annual Unit Sales', y='Price', hue='Brand', ax=ax)
ax.set_title("Doanh số bán hàng theo giá")
ax.set_xlabel("Doanh số bán hàng hàng năm")
ax.set_ylabel("Giá ($)")
st.pyplot(fig)
