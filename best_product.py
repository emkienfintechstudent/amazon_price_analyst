import streamlit as st
import pandas as pd

# Tạo một số dữ liệu mẫu cho sản phẩm (giá, đánh giá, xếp hạng)
data = {
    "Product Name": ["Product A", "Product B", "Product C", "Product D", "Product E"],
    "Price": [100, 150, 200, 120, 180],
    "Rating": [4.5, 4.0, 3.5, 5.0, 4.2],
    "Reviews": [100, 150, 200, 120, 180]
}

# Chuyển dữ liệu vào DataFrame
df = pd.DataFrame(data)

# Tạo tiêu đề cho trang
st.title("Tìm kiếm sản phẩm tốt nhất")

# Tạo ô nhập từ khóa tìm kiếm
search_term = st.text_input("Nhập từ khóa tìm kiếm sản phẩm")

# Chọn tiêu chí tìm kiếm
criteria = st.selectbox("Chọn tiêu chí xếp hạng sản phẩm", ["Giá", "Đánh giá", "Số lượng đánh giá"])

# Khi người dùng nhấn nút tìm kiếm
if st.button("Tìm kiếm"):
    # Tìm kiếm sản phẩm theo từ khóa (tìm kiếm theo tên sản phẩm)
    filtered_products = df[df["Product Name"].str.contains(search_term, case=False)]
    
    # Sắp xếp theo tiêu chí được chọn
    if criteria == "Giá":
        sorted_products = filtered_products.sort_values(by="Price")
    elif criteria == "Đánh giá":
        sorted_products = filtered_products.sort_values(by="Rating", ascending=False)
    else:  # Số lượng đánh giá
        sorted_products = filtered_products.sort_values(by="Reviews", ascending=False)

    # Kiểm tra xem có sản phẩm nào không
    if not sorted_products.empty:
        # Hiển thị kết quả
        st.subheader(f"Kết quả tìm kiếm cho '{search_term}'")
        st.write(sorted_products)
    else:
        st.warning(f"Không tìm thấy sản phẩm nào cho từ khóa '{search_term}'")

# Tạo footer
st.sidebar.markdown("### Tìm kiếm sản phẩm dễ dàng và nhanh chóng với Streamlit!")
