import streamlit as st
import pandas as pd
import numpy as np


def page2():
    st.title("Second page")

pg = st.navigation([
    st.Page("get_started.py", title="Trước khi bắt đầu", icon="🚀"),
    st.Page("product_information.py", title="Thông tin sản phẩm", icon="💬"),
st.Page("market_overview.py", title="Tổng quan thị trường Robot hút bụi", icon="📊"),
st.Page("compare_product.py", title="So sánh 2 sản phẩm", icon="🔍"),
st.Page("page1.py", title="Tổng quan thị trường Robot hút bụi", icon="📈"),
st.Page("best_product.py", title="Sản phẩm đề xuất", icon="🌟"),
st.Page("test_code.py", title="test_code")

])


pg.run()