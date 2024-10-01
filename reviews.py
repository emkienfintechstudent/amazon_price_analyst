import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import json
# Sidebar sections
st.sidebar.header("Nhận xét và đánh giá ")
product_name = st.sidebar.text_input("Tên sản phẩm ")
product_name = st.sidebar.text_input("ASIN")
# star = st.sidebar.selectbox(
#     "Select star",
#     ("ALL",1,2,3,4,5),
# )
if product_name : 
    st.header("Tổng quan về đánh giá của ${product_name}")
else: 
    st.header("Tổng quan về đánh giá của sản phẩm")

reviews_summary_col1, reviews_summary_col1_col2,star_5_count = st.columns(3)
reviews_summary_col1.metric("Số lượng đánh giá ", "70 °F")
reviews_summary_col1_col2.metric("Đánh giá trung bình", "9 mph")
star_5_count.metric("Số lượng đánh giá 5 sao", "70 °F")

star_1_count,star_2_count,star_3_count,star_4_count = st.columns(4)
star_1_count.metric("Số lượng đánh giá 1 sao", "70 °F")
star_2_count.metric("Số lượng đánh giá 2 sao", "70 °F")
star_3_count.metric("Số lượng đánh giá 3 sao", "70 °F")
star_4_count.metric("Số lượng đánh giá 4 sao", "70 °F")
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0.1, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)
# with col3:
#     df_product_rating_count = pd.DataFrame({
#     'Số lượng đánh giá 1 sao': 1,
#        'Số lượng đánh giá 1 sao': 2,
#            'Số lượng đánh giá 1 sao': 3,
#     'Số lượng đánh giá 1 sao': 4,
#     'Số lượng đánh giá 1 sao': 5


# })
if product_name : 
    st.header("Tổng quan về nhận xét của ${product_name}")
else: 
    st.header("Tổng quan về Nhận xét của sản phẩm")
# col4, col5, col6= st.columns(3)
# col4.metric("Số lượng Nhận xét ", "70 °F")
# col5.metric("Đánh giá trung bình", "9 mph", )
# with col3:
#     df_product_rating_count = pd.DataFrame({
#     'Số lượng đánh giá 1 sao': 1,
#        'Số lượng đánh giá 1 sao': 2,
#            'Số lượng đánh giá 1 sao': 3,
#     'Số lượng đánh giá 1 sao': 4,
#     'Số lượng đánh giá 1 sao': 5


# })
with open('detail_product.json', 'r') as f:
    data_detail_product = json.load(f)
    rating =  data_detail_product['detail']['rating']
    total_ratings =  data_detail_product['detail']['total_ratings']
    name =  data_detail_product['detail']['name']
df_product_summary = pd.DataFrame({
    'Name': [name],
    'Rating': [rating],
    'Total Ratings': [total_ratings]
})

st.write(df_product_summary)
st.header("Chi tiết")
with open('reviews.json', 'r') as f:
    data = json.load(f)


# Convert JSON data to a pandas DataFrame
df_reviews_sumary = pd.DataFrame(data)
st.write(df_reviews_sumary[['id', 'date', 'author_name', 'rating','review_title','review_text','location']])
# col1, col2= st.columns(2)
# with col1:
#     st.header("A dog")
# with col2:
#     st.header("A dog")

