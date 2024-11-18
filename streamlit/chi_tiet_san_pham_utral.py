import streamlit as st
import pandas as pd
# Tiêu đề trang
st.title("Chi tiết sản phẩm: Shark AI Ultra Robot Vacuum")
st.subheader("ASIN: B09T4YZGQR")
data = pd.read_csv('../getData/product_data.csv')
history_price= pd.read_csv('../getData/price_history.csv')
history_price

data_utral=data[data['ASIN']=='B09T4YZGQR']

# Phần mô tả sản phẩm
st.header("1. Giới thiệu sản phẩm")
last_price = history_price['price'].iloc[-1]
st.markdown(
    f"""
    ### Tiêu đề sản phẩm: {data_utral['Title'].values[0]}
     ### Hãng: {data_utral['Brand'].values[0]}
          ### Hãng: {data_utral['Brand'].values[0]}

    - **Hệ thống điều hướng thông minh (AI Navigation)**: Robot tự động lên lịch và dọn dẹp mọi ngóc ngách trong ngôi nhà.
    """)

# Lịch sử giá
st.header("Lịch sử giá sản phẩm")
import pandas as pd
import matplotlib.pyplot as plt

# Dữ liệu lịch sử giá
data = {
    "year": [2022, 2022, 2022, 2022, 2022, 2023, 2023, 2024, 2024],
    "month": [5, 6, 10, 12, 12, 2, 7, 5, 11],
    "day": [8, 6, 25, 7, 21, 20, 13, 15, 18],
    "price": [581.47, 599.00, 599.99, 499.00, 298.00, 299.00, 599.99, 679.99, 349.99],
}
df = pd.DataFrame(data)

# Tạo cột thời gian
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Biểu đồ giá
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df["date"], df["price"], marker="o", linestyle="-", label="Giá Shark AI Ultra")
ax.set_title("Lịch sử giá Shark AI Ultra Robot Vacuum", fontsize=16)
ax.set_xlabel("Thời gian", fontsize=12)
ax.set_ylabel("Giá (USD)", fontsize=12)
ax.grid(True)
ax.legend()

st.pyplot(fig)

# Phân tích giá
st.markdown(
    f"""
    - **Giá thấp nhất**: ${df['price'].min():,.2f}
    - **Giá cao nhất**: ${df['price'].max():,.2f}
    - **Khoảng giá hiện tại**: ${df['price'].iloc[-1]:,.2f}
    """
)

# Phần đánh giá khách hàng
st.header("Đánh giá khách hàng")
st.markdown(
    """
    ### Tổng quan đánh giá:
    - **Điểm trung bình**: ⭐ 4.3/5
    - **Số lượng đánh giá**: 3,372 đánh giá
    - **Tích cực**:
      - "Sản phẩm tuyệt vời, hút bụi sạch và rất tiện lợi."
      - "Điều hướng thông minh, hỗ trợ Alexa rất tiện dụng."
    - **Tiêu cực**:
      - "Giá hơi cao, nhưng chất lượng xứng đáng."
    """
)

# Gợi ý mua hàng
st.header("Gợi ý mua hàng")
st.markdown(
    """
    ### Lời khuyên
    - Nên mua vào các dịp giảm giá lớn như **Black Friday** hoặc **Cyber Monday**.
    - Thường xuyên theo dõi giá, mức giá tốt nhất ghi nhận là $298.
    """
)

# Liên hệ
st.header("Liên hệ")
st.markdown(
    """
    - **Xem sản phẩm trên Amazon**: [Shark AI Ultra Robot Vacuum](https://www.amazon.com/dp/B09T4YZGQR)
    - **Liên hệ hỗ trợ**: support@sharkclean.com
    """
)
