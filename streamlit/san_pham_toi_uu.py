import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dữ liệu
data = pd.read_csv('../getData/product_data.csv')

# Set title
st.title("Tổng quan thị trường Robot hút bụi")
data

st.header("Top 5 sản phẩm tốt nhất trên thị trường")
st.header("Top 5 sản phẩm tệ nhất trên thị trường")
st.header("Top 5 sản phẩm bán chạy nhất")
st.header("Top 5 sản phẩm được nhiều review nhất")
st.header("Top 5 sản phẩm có nhiều đánh giá 1 sao cao nhất")
st.header("Top 5 sản phẩm có giá bán cao nhất")
st.header("Top 5 sản phẩm giá bán thấp nhất")
st.header("Top 5 sản phẩm có mức độ phổ biến cao nhất (Best Seller Rankings)")

# tính cả tỉ lệ đánh giá 5 sao của nó 




