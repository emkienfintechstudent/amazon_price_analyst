import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Giả lập dữ liệu từ Canopy API và Unwrangle
# Thay thế bằng các hàm gọi API thực khi bạn có API key và endpoint
def get_financial_data():
    data = {
        "Company": ["iRobot", "Xiaomi", "Ecovacs"],
        "Stock Price": [60.5, 22.3, 30.1],
        "Market Cap (Billion $)": [1.5, 150.2, 5.6],
        "Revenue (Billion $)": [1.2, 100.5, 3.4]
    }
    return pd.DataFrame(data)

def get_product_data():
    data = {
        "Product Name": ["iRobot Roomba S9+", "Xiaomi Mi Robot", "Ecovacs Deebot OZMO"],
        "Brand": ["iRobot", "Xiaomi", "Ecovacs"],
        "Price ($)": [899, 299, 499],
        "Rating": [4.5, 4.3, 4.1],
        "Features": ["Self-emptying, Smart mapping", "Basic navigation", "Mop function, App control"]
    }
    return pd.DataFrame(data)

# Load data
financial_data = get_financial_data()
product_data = get_product_data()

# Streamlit App
st.title("Robot Hút Bụi Dashboard")

# Section 1: Overview
st.header("Tổng Quan")
st.write("Trang tổng quan này cung cấp thông tin chi tiết về các sản phẩm robot hút bụi, bao gồm hiệu suất tài chính của các công ty và các đặc điểm sản phẩm nổi bật.")

# Section 2: Financial Analysis
st.header("Phân Tích Tài Chính - Các Công Ty Sản Xuất Robot Hút Bụi")
st.write("Thông tin tài chính từ Canopy API")
st.dataframe(financial_data)

# Plot financial data (Market Cap vs Revenue)
st.subheader("So Sánh Vốn Hóa Thị Trường và Doanh Thu")
fig, ax = plt.subplots()
ax.bar(financial_data["Company"], financial_data["Market Cap (Billion $)"], color="blue", label="Market Cap")
ax.bar(financial_data["Company"], financial_data["Revenue (Billion $)"], color="orange", label="Revenue")
ax.set_xlabel("Company")
ax.set_ylabel("Billion $")
ax.legend()
st.pyplot(fig)

# Section 3: Product Analysis
st.header("Phân Tích Sản Phẩm - Robot Hút Bụi")
st.write("Thông tin chi tiết về các sản phẩm từ Unwrangle API")
st.dataframe(product_data)

# Filter products
st.subheader("Tìm Kiếm và Lọc Sản Phẩm")
selected_brand = st.selectbox("Chọn Thương Hiệu", options=product_data["Brand"].unique())
filtered_data = product_data[product_data["Brand"] == selected_brand]
st.write(f"Các sản phẩm của thương hiệu {selected_brand}")
st.dataframe(filtered_data)

# Price vs Rating
st.subheader("Biểu Đồ Giá và Đánh Giá")
fig, ax = plt.subplots()
ax.scatter(product_data["Price ($)"], product_data["Rating"], color="green")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Rating")
st.pyplot(fig)

# Section 4: Featured Product Recommendation
st.header("Sản Phẩm Nổi Bật")
best_product = product_data.loc[product_data["Rating"].idxmax()]
st.write(f"**Sản phẩm được đề xuất:** {best_product['Product Name']}")
st.write(f"Giá: ${best_product['Price ($)']}")
st.write(f"Đánh giá: {best_product['Rating']}")
st.write(f"Tính năng: {best_product['Features']}")

# Section 5: Trend Analysis
st.header("Phân Tích Xu Hướng Giá")
st.write("Dự báo giá và xu hướng sản phẩm robot hút bụi.")
# (Mô phỏng dữ liệu dự báo giá hoặc phân tích xu hướng nếu có dữ liệu thực tế)

st.write("Dashboard này cung cấp một cái nhìn tổng quan về các sản phẩm robot hút bụi, bao gồm các phân tích về công ty và sản phẩm.")
