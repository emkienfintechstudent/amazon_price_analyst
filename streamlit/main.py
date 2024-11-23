import streamlit as st
import pandas as pd
import numpy as np


def page2():
    st.title("Second page")

pg = st.navigation([
st.Page("get_started.py", title="Trước khi bắt đầu", icon="🚀"),  # "Trước khi bắt đầu" - Icon 🚀 (bắt đầu hành trình)
st.Page("tong_quan.py", title="Tổng quan thị trường Robot hút bụi", icon="🌍"),  # "Tổng quan thị trường" - Icon 🌍 (toàn cảnh thị trường)
st.Page("san_pham_toi_uu.py", title="Sản phẩm tối ưu", icon="🌍"),  # "Tổng quan thị trường" - Icon 🌍 (toàn cảnh thị trường)
st.Page("chi_tiet_san_pham_utral.py", title="Chi tiết sản phẩm Shark AI Ultra ", icon="🔍"),  # "Tìm kiếm và Lọc" - Icon 🔍 (tìm kiếm)
st.Page("chi_tiet_san_pham_khac.py", title="Chi tiết sản phẩm khác ", icon="🔍"),  # "Tìm kiếm và Lọc" - Icon 🔍 (tìm kiếm)

st.Page("tim_kiem_sp.py", title="Tìm kiếm và Lọc", icon="🔍"),  # "Tìm kiếm và Lọc" - Icon 🔍 (tìm kiếm)
st.Page("bieu_do_va_do_thi.py", title="Biểu đồ và Đồ thị", icon="📈"),  # "Biểu đồ và Đồ thị" - Icon 📈 (thống kê, phân tích)
st.Page("bang_chi_tiet_san_pham.py", title="Bảng chi tiết sản phẩm", icon="📋")  # "Bảng chi tiết sản phẩm" - Icon 📋 (danh sách, bảng biểu)

])


pg.run()