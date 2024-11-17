import streamlit as st

# Thiết lập tiêu đề trang và căn chỉnh
st.set_page_config(page_title="Dữ liệu Sản phẩm trên Amazon", layout="centered")

# CSS tùy chỉnh để làm đẹp trang
st.markdown("""
    <style>
    /* Định dạng cho toàn bộ trang */
    .stApp {
        background-color: #f7f9fc;
        font-family: Arial, sans-serif;
    }

    /* Định dạng tiêu đề */
    .title-container {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #4a6fa5;
        margin-top: 50px;
        padding: 10px;
        border-bottom: 2px solid #4a6fa5;
    }

    /* Định dạng nội dung chính */
    .content-container {
        background-color: #ffffff;
        padding: 20px;
        margin: 20px auto;
        width: 60%;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        font-size: 18px;
        color: #333333;
        line-height: 1.6;
    }

    /* Định dạng đường viền trang trí */
    .divider {
        height: 2px;
        background-color: #4a6fa5;
        margin: 20px 0;
    }

    /* Chữ đậm cho từ khóa */
    .highlight {
        color: #4a6fa5;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Hiển thị tiêu đề trang
st.markdown("<div class='title-container'>Thông tin Dữ liệu Sản phẩm</div>", unsafe_allow_html=True)

# Đường viền trang trí
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Nội dung chính
content = """
Dữ liệu trong bài được thu thập từ các sản phẩm trên Amazon thông qua API của Canopy và Unwrangle, bao gồm các thông tin như mô tả sản phẩm, doanh thu ước tính, hàng tồn kho dự kiến... Dựa trên từ khóa tìm kiếm <span class='highlight'>'robot vacuum cleaner'</span>.
"""
st.markdown(f"<div class='content-container'>{content}</div>", unsafe_allow_html=True)

# Đường viền trang trí
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Phần đệm cuối trang
st.write(" ")
st.write(" ")
