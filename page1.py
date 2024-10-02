import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tiêu đề chính của dashboard
st.title("Pricing Strategy Dashboard")

# Tải dữ liệu (bạn có thể thay thế bằng dữ liệu thực tế)
# Dữ liệu bao gồm các cột: 'Product Name', 'Date', 'Price', 'Competitor Price'
data = {
    'Product Name': ['Product A', 'Product A', 'Product B', 'Product B'],
    'Date': ['2024-01-01', '2024-01-02', '2024-01-01', '2024-01-02'],
    'Price': [100, 105, 200, 210],
    'Competitor Price': [110, 108, 195, 205]
}
df = pd.DataFrame(data)

# Sidebar cho phép chọn sản phẩm
st.sidebar.header("Chọn sản phẩm")
selected_product = st.sidebar.selectbox("Chọn sản phẩm", df['Product Name'].unique())

# Hiển thị dữ liệu của sản phẩm được chọn
st.header(f"Chi tiết sản phẩm: {selected_product}")
product_data = df[df['Product Name'] == selected_product]
st.write(product_data)

# Hiển thị biểu đồ giá theo thời gian
st.header("Xu hướng giá theo thời gian")
plt.figure(figsize=(10, 4))
plt.plot(product_data['Date'], product_data['Price'], label="Giá sản phẩm")
plt.plot(product_data['Date'], product_data['Competitor Price'], label="Giá đối thủ", linestyle="--")
plt.xlabel("Ngày")
plt.ylabel("Giá")
plt.legend()
st.pyplot(plt)

# Phân tích chiến lược giá
st.header("Phân tích chiến lược giá")
avg_competitor_price = product_data['Competitor Price'].mean()
st.write(f"Giá trung bình của đối thủ: {avg_competitor_price}")

# Gợi ý chiến lược giá
suggested_price = avg_competitor_price * 0.95  # Giảm giá 5% so với đối thủ
st.write(f"Giá gợi ý cho {selected_product}: {suggested_price}")
