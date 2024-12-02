import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tiêu đề trang
st.title("Chi tiết sản phẩm Amazon")
st.subheader("Chọn sản phẩm để xem chi tiết")

# Đọc dữ liệu sản phẩm và lịch sử giá
data = pd.read_csv('../getData/data/product_data.csv')
history_price = pd.read_csv('../getData/data/price_history.csv')

# Thêm thanh chọn sản phẩm (ASIN hoặc tên sản phẩm)
selected_asin = st.selectbox(
    "Chọn sản phẩm theo ASIN hoặc tên:",
    data["ASIN"] + " - " + data["Title"]
)

# Tách ASIN từ chuỗi đã chọn
asin = selected_asin.split(" - ")[0]

# Lọc dữ liệu sản phẩm
selected_product = data[data['ASIN'] == asin]
selected_product
if not selected_product.empty:
    # Thông tin cơ bản của sản phẩm
    st.header("Giới thiệu sản phẩm")
    # st.image("../getData/utral.jpg", width=300)  # Thay đổi ảnh sản phẩm nếu cần

    # Lấy lịch sử giá của sản phẩm
    # product_price_history = history_price[history_price['ASIN'] == asin]
    # last_price = product_price_history['price'].iloc[-1] if not product_price_history.empty else "N/A"
    last_price  = selected_product['Price'].values[0]
    st.markdown(
        f"""
        **Tiêu đề sản phẩm**: {selected_product['Title'].values[0]}  
        **Hãng**: {selected_product['Brand'].values[0]}  
        **Danh mục**: {selected_product['Categories'].values[0]}  
        **Giá hiện tại**: {last_price}  

        **Đặc điểm nổi bật:**  
        """
    )

    # Hiển thị các đặc điểm nổi bật
    features = selected_product['Feature Bullets'].values[0].split(";")
    for feature in features:
        st.markdown(f"- {feature.strip()}")

    # Thông tin kỹ thuật
    st.markdown("**Tính năng đặc biệt:**")
    technical_specs = selected_product['Technical Specifications'].values[0].split(";")
    for spec in technical_specs:
        st.markdown(f"- {spec.strip()}")

    # Phân tích đánh giá sản phẩm
    st.header("Tổng quan về đánh giá sản phẩm")
    col1, col2 = st.columns(2)
    col1.metric("Số lượng đánh giá", selected_product['Ratings Total'].values[0])
    col2.metric("Đánh giá trung bình", selected_product['Rating Average'].values[0])

    one_star = selected_product['One Star Ratings Count'].values[0]
    two_star = selected_product['Two Star Ratings Count'].values[0]
    three_star = selected_product['Three Star Ratings Count'].values[0]
    four_star = selected_product['Four Star Ratings Count'].values[0]
    five_star = selected_product['Five Star Ratings Count'].values[0]
    total_rating = selected_product['Ratings Total'].values[0]

    # Tính phần trăm từng loại đánh giá
    one_star_rate = round(one_star / total_rating * 100, 2)
    two_star_rate = round(two_star / total_rating * 100, 2)
    three_star_rate = round(three_star / total_rating * 100, 2)
    four_star_rate = round(four_star / total_rating * 100, 2)
    five_star_rate = 100 - one_star_rate - two_star_rate - three_star_rate - four_star_rate

    # Biểu đồ tròn
    labels = ['1 sao', '2 sao', '3 sao', '4 sao', '5 sao']
    sizes = [one_star_rate, two_star_rate, three_star_rate, four_star_rate, five_star_rate]
    max_index = sizes.index(max(sizes))
    explode = [0.1 if i == max_index else 0 for i in range(len(sizes))]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    ax1.set_title("Phân bố đánh giá sản phẩm")
    st.pyplot(fig1)
    st.header("Tổng quan về doanh số bán hàng ")
   # Kiểm tra và hiển thị từng metric nếu có
    if (
        not pd.isna(selected_product['Weekly Unit Sales'].values[0])
        and not pd.isna(selected_product['Monthly Unit Sales'].values[0])
        and not pd.isna(selected_product['Annual Unit Sales'].values[0])
    ):
        # Nếu tất cả đều tồn tại, sắp xếp trong các cột
        col1, col2= st.columns(2)
        col1.metric("Doanh số bán hàng ước tính hàng tuần", selected_product['Weekly Unit Sales'].values[0])
        col2.metric("Doanh số bán hàng ước tính hàng tháng", selected_product['Monthly Unit Sales'].values[0])
        st.metric("Doanh số bán hàng ước tính hàng năm", selected_product['Annual Unit Sales'].values[0])
    else:
        # Hiển thị từng metric nếu thông tin không đủ
        if not pd.isna(selected_product['Weekly Unit Sales'].values[0]):
            st.metric("Doanh số bán hàng ước tính hàng tuần", selected_product['Weekly Unit Sales'].values[0])

        if not pd.isna(selected_product['Monthly Unit Sales'].values[0]):
            st.metric("Doanh số bán hàng ước tính hàng tháng", selected_product['Monthly Unit Sales'].values[0])

        if not pd.isna(selected_product['Annual Unit Sales'].values[0]):
            st.metric("Doanh số bán hàng ước tính hàng năm", selected_product['Annual Unit Sales'].values[0])



    

    # Lịch sử giá
    # st.header("Lịch sử giá của sản phẩm")
    # if not product_price_history.empty:
    #     product_price_history["date"] = pd.to_datetime(product_price_history[["year", "month", "day"]])
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(product_price_history['date'], product_price_history['price'], linestyle='-', marker='o', label="Price")
    #     plt.title("Lịch sử giá sản phẩm")
    #     plt.xlabel("Ngày")
    #     plt.ylabel("Giá (USD)")
    #     plt.grid(True)
    #     plt.legend()
    #     st.pyplot(plt)

    #     # Hiển thị thông tin thêm
    #     min_price = product_price_history['price'].min()
    #     average_price = product_price_history['price'].mean()
    #     max_price = product_price_history['price'].max()
    #     st.markdown(
    #         f"""
    #         - **Giá trung bình:** ${average_price:,.2f}  
    #         - **Giá thấp nhất:** ${min_price:,.2f}  
    #         - **Giá cao nhất:** ${max_price:,.2f}  
    #         - **Giá hiện tại:** ${last_price:,.2f}  
    #         """
    #     )
    # else:
    #     st.warning("Không có dữ liệu lịch sử giá cho sản phẩm này.")
else:
    st.warning("Sản phẩm không tồn tại hoặc không có dữ liệu chi tiết.")
