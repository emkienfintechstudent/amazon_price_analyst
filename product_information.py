import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import json
# Sidebar sections
st.sidebar.header("Nhận xét và đánh giá ")
product_name = st.sidebar.text_input("Tên sản phẩm ")
product_name = st.sidebar.text_input("ASIN")

# Rating summary
# star = st.sidebar.selectbox(
#     "Select star",
#     ("ALL",1,2,3,4,5),
# )
with open('rating.json', 'r') as f:
    data_rating = json.load(f)
rating_avg = data_rating['data']['amazonProduct']['rating']
rating_count = data_rating['data']['amazonProduct']['ratingsTotal']
star_1_count = data_rating['data']['amazonProduct']['ratingsBreakdown']['oneStarRatingsCount']
star_2_count= data_rating['data']['amazonProduct']['ratingsBreakdown']['twoStarRatingsCount']
star_3_count= data_rating['data']['amazonProduct']['ratingsBreakdown']['threeStarRatingsCount']
star_4_count= data_rating['data']['amazonProduct']['ratingsBreakdown']['fourStarRatingsCount']
star_5_count= data_rating['data']['amazonProduct']['ratingsBreakdown']['fiveStarRatingsCount']
print(data_rating['data']['amazonProduct'])
if product_name : 
    st.header("Tổng quan về đánh giá của ${product_name}")
else: 
    st.header("Tổng quan về đánh giá của sản phẩm")

rating_count_view, rating_avg_view, reviews_count_view ,star_5_count_view= st.columns(4)
rating_count_view.metric("Số lượng đánh giá ", rating_count)
rating_avg_view.metric("Đánh giá trung bình", rating_avg)
reviews_count_view.metric("Số lượng review sản phẩm", rating_avg)
star_5_count_view.metric("Số lượng đánh giá 5 sao", star_5_count)


star_1_count_view,star_2_count_view,star_3_count_view,star_4_count_view = st.columns(4)
star_1_count_view.metric("Số lượng đánh giá 1 sao", star_1_count)
star_2_count_view.metric("Số lượng đánh giá 2 sao", star_2_count)
star_3_count_view.metric("Số lượng đánh giá 3 sao", star_3_count)
star_4_count_view.metric("Số lượng đánh giá 4 sao", star_4_count)
# Pie chart, where the slices will be ordered and plotted counter-clockwise:


# Labels cho các loại rating
labels = '1 Star', '2 Star', '3 Star', '4 Star', '5 Star'

# Tính phần trăm của mỗi loại rating
star_5_count_percent = 1 - star_1_count/rating_count - star_2_count/rating_count - star_3_count/rating_count - star_4_count/rating_count
sizes = [star_1_count/rating_count*100, star_2_count/rating_count *100, star_3_count/rating_count*100, star_4_count/rating_count*100, star_5_count_percent*100]

# Tìm vị trí của phần trăm lớn nhất trong sizes
max_index = sizes.index(max(sizes))

# Tạo mảng explode với giá trị 0 cho tất cả và chỉ cho vị trí lớn nhất là 0.1
explode = [0] * len(sizes)
explode[max_index] = 0.1  # Đặt explode cho phần tử lớn nhất

# Tạo biểu đồ pie
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Đảm bảo hình tròn

# Hiển thị biểu đồ trên Streamlit
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

st.header("Chi tiết")
# with open('reviews.json', 'r') as f:
#     data = json.load(f)


# # Convert JSON data to a pandas DataFrame
# df_reviews_sumary = pd.DataFrame(data)
# st.write(df_reviews_sumary[['id', 'date', 'author_name', 'rating','review_title','review_text','location']])
# col1, col2= st.columns(2)
# with col1:
#     st.header("A dog")
# with col2:
#     st.header("A dog")

