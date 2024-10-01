import streamlit as st
import pandas as pd
import numpy as np
# Sidebar sections
st.sidebar.header("Chiến lược giá sản phẩm")
product_name = st.sidebar.text_input("Tên sản ", "Sản phẩm mẫu")
category = st.sidebar.selectbox("Danh mục sản phẩm", ["Điện tử", "Thực phẩm", "Thời trang", "Khác"])
base_cost = st.sidebar.number_input("Chi phí cơ bản (USD)", min_value=0.0, step=0.1)
desired_profit_margin = st.sidebar.slider("Biên lợi nhuận mong muốn (%)", 0, 100, 20)
market_price = st.sidebar.number_input("Giá thị trường tham khảo (USD)", min_value=0.0, step=0.1)
competitor_price = st.sidebar.number_input("Giá của đối thủ (USD)", min_value=0.0, step=0.1)

# Pricing strategy
st.title("Xây dựng chiến lược giá cho sản phẩm")

st.write(f"Tên sản phẩm: **{product_name}**")
st.write(f"Danh mục sản phẩm: **{category}**")

# Price calculation
final_price = base_cost * (1 + desired_profit_margin / 100)
st.write(f"Giá dự kiến dựa trên chi phí cơ bản và biên lợi nhuận mong muốn: **${final_price:.2f}**")

# Market and competitor analysis
if market_price > 0:
    st.write(f"Giá thị trường hiện tại: **${market_price:.2f}**")
    if final_price < market_price:
        st.success("Giá của bạn đang thấp hơn giá thị trường.")
    else:
        st.warning("Giá của bạn đang cao hơn giá thị trường.")

if competitor_price > 0:
    st.write(f"Giá của đối thủ: **${competitor_price:.2f}**")
    if final_price < competitor_price:
        st.success("Giá của bạn thấp hơn đối thủ.")
    else:
        st.warning("Giá của bạn cao hơn đối thủ.")

# Price suggestions
st.subheader("Khuyến nghị giá")
if final_price < market_price and final_price < competitor_price:
    st.write("Bạn có thể đặt mức giá hiện tại vì đang cạnh tranh.")
elif final_price > market_price and final_price > competitor_price:
    st.write("Xem xét điều chỉnh chiến lược giá để không mất cạnh tranh.")
else:
    st.write("Bạn có thể xem xét thêm các yếu tố khác như giá trị sản phẩm, chất lượng để đưa ra quyết định.")

# Market segmentation
st.subheader("Phân đoạn thị trường")
customer_segment = st.multiselect(
    "Chọn phân đoạn khách hàng mục tiêu",
    ["Khách hàng phổ thông", "Khách hàng cao cấp", "Khách hàng doanh nghiệp", "Khách hàng trẻ"]
)
if customer_segment:
    st.write(f"Phân đoạn khách hàng mục tiêu: **{', '.join(customer_segment)}**")

# Additional analysis
st.subheader("Phân tích bổ sung")
cost_variation = st.checkbox("Có muốn mô phỏng biến động chi phí không?")
if cost_variation:
    st.write("Mô phỏng biến động chi phí cho các kịch bản khác nhau:")
    cost_range = st.slider("Phạm vi biến động chi phí (%)", -50, 50, (-10, 10))
    varied_prices = [base_cost * (1 + margin / 100) for margin in np.arange(cost_range[0], cost_range[1], 1)]
    varied_df = pd.DataFrame(varied_prices, columns=["Giá dự kiến"])
    st.line_chart(varied_df)

# Conclusion
st.subheader("Tóm tắt chiến lược giá")
st.write(f"Giá sản phẩm đề xuất: **${final_price:.2f}**")

st.write("Bạn có thể điều chỉnh lại chiến lược giá dựa trên chi phí cơ bản, giá trị thị trường và tình hình cạnh tranh.")
