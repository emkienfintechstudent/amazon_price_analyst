import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Tiêu đề trang
st.title("Chi tiết sản phẩm: Shark AI Ultra Robot Vacuum")
st.subheader("ASIN: B09T4YZGQR")
data = pd.read_csv('../getData/data/product_data.csv')
history_price= pd.read_csv('../getData/data/price_history.csv')
data_utral=data[data['ASIN']=='B09T4YZGQR']
# Tách chuỗi dựa trên ký tự phân cách ";"
features = data_utral['Feature Bullets'].values[0].split(";")


# Phần mô tả sản phẩm
st.header("Giới thiệu sản phẩm")
last_price = history_price['price'].iloc[-1]
st.image("../getData/utral.jpg",width = 300)

# Hiển thị Markdown
st.markdown(
    f"""
    **Tiêu đề sản phẩm**: {data_utral['Title'].values[0]}  
    **Hãng**: {data_utral['Brand'].values[0]}    
    **Danh mục**: {data_utral['Categories'].values[0]}  
    **Giá hiện tại**: {last_price}  

    **Đặc điểm nổi bật:**  
    """
)
# Duyệt qua các features và hiển thị từng dòng
for feature in features:
    st.markdown(f"- {feature.strip()}")  # Hiển thị từng feature và loại bỏ khoảng trắng thừa
features = data_utral['Feature Bullets'].values[0].split(";")
Technical_Specifications = data_utral['Technical Specifications'].values[0].split(";")
st.markdown(
        """
**Tính năng đặc biệt:**
            """)
for Technical_Specification in Technical_Specifications:
    st.markdown(f"- {Technical_Specification.strip()}") 
st.markdown(
       f"""
**Xếp hạng của sản phẩm:** {data_utral['Title'].values[0]} 
            """)
st.header("Tổng quan về đánh giá sản phẩm")

col1, col2 = st.columns(2)
col1.metric("Số lượng đánh giá", data_utral['Ratings Total'].values[0])
col2.metric("Đánh giá trung bình", data_utral['Rating Average'].values[0])

one_star = data_utral['One Star Ratings Count'].values[0]
two_star = data_utral['Two Star Ratings Count'].values[0]
three_star = data_utral['Three Star Ratings Count'].values[0]
four_star = data_utral['Four Star Ratings Count'].values[0]
five_star = data_utral['Five Star Ratings Count'].values[0]
total_rating = data_utral['Ratings Total'].values[0]
# Calculate percentages for each star rating
one_star_rate = round(one_star / total_rating * 100, 2)
two_star_rate = round(two_star / total_rating * 100, 2)
three_star_rate = round(three_star / total_rating * 100, 2)
four_star_rate = round(four_star / total_rating * 100, 2)
five_star_rate = 100 - one_star_rate - two_star_rate - three_star_rate - four_star_rate
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = '1 sao', '2 sao', '3 sao', '4 sao','5 sao'
sizes = [one_star_rate, two_star_rate, three_star_rate, four_star_rate, five_star_rate]

# Find the index of the largest slice
max_index = sizes.index(max(sizes))

# Dynamically set the explode value: 0.1 for the largest, 0 for others
explode = [0.1 if i == max_index else 0 for i in range(len(sizes))]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Add a title to the pie chart
ax1.set_title("Phân bố đánh giá sản phẩm")

# Display the pie chart in Streamlit
st.pyplot(fig1)

st.header("Lịch sử giá của sản phẩm")

# Tạo cột thời gian
history_price["date"] = pd.to_datetime(history_price[["year", "month", "day"]])

# Vẽ biểu đồ lịch sử giá
plt.figure(figsize=(10, 6))
plt.plot(history_price['date'], history_price['price'], linestyle='-', label="Price")
plt.title("Lịch sử giá sản phẩm")
plt.xlabel("Ngày")
plt.ylabel("Giá (USD)")
plt.grid(True)
plt.legend()
st.pyplot(plt)


min_price = history_price['price'].min()
average_price = history_price['price'].mean()
max_price = history_price['price'].max()
current_price = last_price

st.markdown(
    f"""
    - **Giá trung bình:** ${average_price:,.2f}   
    - **Giá thấp nhất:** ${min_price:,.2f}  
    - **Giá cao nhất:** ${max_price:,.2f}  
    - **Giá hiện tại:** ${current_price:,.2f}  
    """
)


