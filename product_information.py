import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import json
# Sidebar sections
st.sidebar.header("Nhận xét và đánh giá ")
product_name = st.sidebar.text_input("Tên sản phẩm ")
product_ASIN = st.sidebar.text_input("ASIN")
 #read file 
with open('rating.json', 'r') as f:
    data_rating = json.load(f)
with open('product_information.json', 'r') as f:
    data_product_information = json.load(f)

# Tiêu đề và liên kết
st.title("eufy Robot Vacuum 11S MAX")
st.markdown("[Xem trên Amazon](https://www.amazon.com/eufy-Super-Thin-Super-Strong-Self-Charging-Medium-Pile/dp/B07R295MLS)")
st.subheader("Thương hiệu: eufy")

# Giá sản phẩm
st.write("**Giá:** $249.99 USD")

# Đặc điểm nổi bật
st.subheader("Đặc điểm nổi bật của sản phẩm")
features = [
    "Compact and Quiet Operation: Thiết kế siêu mỏng, hoạt động êm ái, có thể sử dụng mọi lúc mà không gây ồn.",
    "Extended Cleaning Performance: Khả năng làm sạch liên tục trong 100 phút trên sàn gỗ và thảm.",
    "Intelligent Cleaning Power: Công nghệ BoostIQ tự động tăng sức hút khi cần.",
    "Superior Protection and Efficiency: Cảm biến hồng ngoại tránh chướng ngại vật và công nghệ cảm biến chống rơi.",
    "What You Get: Bao gồm máy, điều khiển từ xa, đế sạc, cọ làm sạch, và bảo hành 12 tháng."
]
st.write("\n".join(f"- {feature}" for feature in features))

# Thông số kỹ thuật
st.subheader("Thông số kỹ thuật sản phẩm")
specifications = {
    "Thương hiệu": "eufy",
    "Model": "eufy 11S Max",
    "Màu sắc": "Đen",
    "Kích thước sản phẩm": "12.79\"L x 12.79\"W x 2.85\"H",
    "Nguồn điện": "Pin",
    "Dung tích": "600 ml",
    "Tuổi thọ pin": "100 phút",
    "Loại bề mặt": "Sàn cứng và thảm vừa",
    "Đánh giá của khách hàng": "4.3 trên 5 sao",
    "Xếp hạng bán chạy": "#782 trong Home & Kitchen",
    "ASIN": "B07R295MLS"
}
st.table(specifications.items())

# Đánh giá nổi bật
st.subheader("Đánh giá nổi bật từ khách hàng")
review = {
    "Tiêu đề": "Great and Easy to Use!",
    "Nội dung": "Tôi có một chú chó hay rụng lông, vì vậy tôi mua máy hút này với hy vọng sẽ gom được lông chó trên sàn hàng ngày. Những điểm nổi bật: Rất dễ sử dụng, hướng dẫn đơn giản.",
    "Đánh giá": "5/5",
    "Số lượt bình chọn hữu ích": "5313",
    "Người đánh giá": "CF"
}
st.write(f"**Tiêu đề đánh giá:** {review['Tiêu đề']}")
st.write(f"**Nội dung:** {review['Nội dung']}")
st.write(f"**Đánh giá:** {review['Đánh giá']}")
st.write(f"**Số lượt bình chọn hữu ích:** {review['Số lượt bình chọn hữu ích']}")
st.write(f"**Người đánh giá:** {review['Người đánh giá']}")


reviews_count = data_product_information['data']['amazonProduct']['reviewsTotal']
rating_avg = data_rating['data']['amazonProduct']['rating']
rating_count = data_rating['data']['amazonProduct']['ratingsTotal']
star_1_count = data_rating['data']['amazonProduct']['ratingsBreakdown']['oneStarRatingsCount']
star_2_count= data_rating['data']['amazonProduct']['ratingsBreakdown']['twoStarRatingsCount']
star_3_count= data_rating['data']['amazonProduct']['ratingsBreakdown']['threeStarRatingsCount']
star_4_count= data_rating['data']['amazonProduct']['ratingsBreakdown']['fourStarRatingsCount']
star_5_count= data_rating['data']['amazonProduct']['ratingsBreakdown']['fiveStarRatingsCount']
if product_name : 
    st.header("Tổng quan về đánh giá của ${product_name}")
else: 
    st.header("Tổng quan về đánh giá của sản phẩm")

rating_count_view, rating_avg_view, reviews_count_view ,star_5_count_view= st.columns(4)
rating_count_view.metric("Số lượng đánh giá ", rating_count)
rating_avg_view.metric("Đánh giá trung bình", rating_avg)
reviews_count_view.metric("Số lượng review sản phẩm",reviews_count)
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
ax1.set_title('So sánh giữa Số lượng đánh giá và Số lượng review sản phẩm')
# tạo biểu đồ bar chart
# Data values
labels = ['Số lượng đánh giá', 'Số lượng review sản phẩm']
values = [rating_count, reviews_count]

# Create bar chart
fig, ax = plt.subplots()
ax.bar(labels, values, color=['#1f77b4', '#ff7f0e'])

# Add titles and labels
ax.set_ylabel('Số lượng')
ax.set_title('Phân bố các mức đánh giá sản phẩm')
rating_pie_chart, rating_review_bar_chart =  st.columns(2)
# Hiển thị biểu đồ trên Streamlit
with rating_pie_chart:
 st.pyplot(fig1)
with rating_review_bar_chart:
    st.pyplot(fig)




if product_name : 
    st.header(f"Ước tính số lượng sản phẩm bán ra hàng tháng và doanh thu sản phẩm của {product_name}")
else: 
    st.header(f"Ước tính doanh số bán ra hàng tháng và doanh thu sản phẩm của {product_name}")
sales_estimate= data_product_information['data']['amazonProduct']['salesEstimate']
weekly_unit_sales = sales_estimate['weeklyUnitSales']
monthly_unit_sales = sales_estimate['monthlyUnitSales']
annual_unit_sales = sales_estimate['annualUnitSales']
price = data_product_information['data']['amazonProduct']['price']['value']
weekly_revenue_estimate = weekly_unit_sales*price
monthly_revenue_estimate = monthly_unit_sales*price
annual_revenue_estimate = annual_unit_sales*price
# Dòng 1: Doanh số sản phẩm
weekly_unit_sales = sales_estimate['weeklyUnitSales']
monthly_unit_sales = sales_estimate['monthlyUnitSales']
annual_unit_sales = sales_estimate['annualUnitSales']
price = data_product_information['data']['amazonProduct']['price']['value']

# Tính toán doanh thu
weekly_revenue_estimate = weekly_unit_sales * price
monthly_revenue_estimate = monthly_unit_sales * price
annual_revenue_estimate = annual_unit_sales * price

# Dòng 1: Doanh số
weekly_unit_sales_view, monthly_unit_sales_view, annual_unit_sales_view = st.columns(3)
weekly_unit_sales_view.metric(label="Doanh số ước tính hàng tuần", value=weekly_unit_sales)
monthly_unit_sales_view.metric(label="Doanh số ước tính hàng tháng", value=monthly_unit_sales)
annual_unit_sales_view.metric(label="Doanh số ước tính hàng năm", value=annual_unit_sales)

# Dòng 2: Doanh thu
weekly_revenue_view, monthly_revenue_view, annual_revenue_view = st.columns(3)
weekly_revenue_view.metric(label="Doanh thu ước tính hàng tuần", value=f"${weekly_revenue_estimate:,.2f}")
monthly_revenue_view.metric(label="Doanh thu ước tính hàng tháng", value=f"${monthly_revenue_estimate:,.2f}")
annual_revenue_view.metric(label="Doanh thu ước tính hàng năm", value=f"${annual_revenue_estimate:,.2f}")


import matplotlib.pyplot as plt

# Dữ liệu doanh số và doanh thu
labels = ['Hàng tuần', 'Hàng tháng', 'Hàng năm']
sales_data = [weekly_unit_sales, monthly_unit_sales, annual_unit_sales]
revenue_data = [weekly_revenue_estimate, monthly_revenue_estimate, annual_revenue_estimate]







