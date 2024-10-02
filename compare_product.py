import streamlit as st
import pandas as pd

# Giả sử bạn có một hàm để lấy thông tin sản phẩm từ ASIN hoặc tên
def get_product_info(query):
    # Thay thế bằng API thực tế của bạn, ví dụ Amazon Product API
    # Ví dụ chỉ sử dụng dữ liệu mẫu để minh họa
    products = {
        'B08N5WRWNW': {'name': 'Product 1', 'price': 500, 'rating': 4.5, 'category': 'Electronics'},
        'B08X4W6C2V': {'name': 'Product 2', 'price': 450, 'rating': 4.2, 'category': 'Electronics'},
        'Phone A': {'name': 'Phone A', 'price': 300, 'rating': 4.3, 'category': 'Mobile Phones'},
        'Laptop B': {'name': 'Laptop B', 'price': 1000, 'rating': 4.8, 'category': 'Laptops'}
    }
    
    return products.get(query, None)

# Tạo 2 cột cho việc so sánh sản phẩm
col1, col2 = st.columns(2)

with col1:
    st.header("Sản phẩm 1")
    query1 = st.text_input("Nhập ASIN hoặc tên sản phẩm cho cột 1")
    product1 = None
    if query1:
        product1 = get_product_info(query1)
        if product1:
            st.write(f"Tên: {product1['name']}")
            st.write(f"Giá: {product1['price']}$")
            st.write(f"Đánh giá: {product1['rating']}⭐")
            st.write(f"Loại sản phẩm: {product1['category']}")
        else:
            st.warning("Không tìm thấy sản phẩm cho cột 1!")

with col2:
    st.header("Sản phẩm 2")
    query2 = st.text_input("Nhập ASIN hoặc tên sản phẩm cho cột 2")
    product2 = None
    if query2:
        product2 = get_product_info(query2)
        if product2:
            st.write(f"Tên: {product2['name']}")
            st.write(f"Giá: {product2['price']}$")
            st.write(f"Đánh giá: {product2['rating']}⭐")
            st.write(f"Loại sản phẩm: {product2['category']}")
        else:
            st.warning("Không tìm thấy sản phẩm cho cột 2!")

# Thực hiện so sánh khi cả hai sản phẩm đã được nhập
if product1 and product2:
    st.subheader("So sánh sản phẩm:")
    comparison_data = {
        "Thuộc tính": ["Tên", "Giá ($)", "Đánh giá", "Loại sản phẩm"],
        "Sản phẩm 1": [product1['name'], product1['price'], product1['rating'], product1['category']],
        "Sản phẩm 2": [product2['name'], product2['price'], product2['rating'], product2['category']],
    }
    df_comparison = pd.DataFrame(comparison_data)
    st.table(df_comparison)
