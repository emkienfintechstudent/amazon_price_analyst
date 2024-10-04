import streamlit as st
import pandas as pd

# Dữ liệu giả lập cho các sản phẩm
data = {
    'Product': ['Product A', 'Product B', 'Product C'],
    'Avg Rating': [4.5, 4.2, 3.8],
    '5-Star Ratings': [1000, 800, 500],
    'Weekly Sales': [150, 100, 50],
    'Monthly Sales': [600, 400, 200],
    'Yearly Sales': [7200, 4800, 2400],
    'Price': [100, 80, 70]
}

df = pd.DataFrame(data)

# Tính toán phân vị cho các yếu tố
df['Rating Quantile'] = pd.qcut(df['Avg Rating'], 4, labels=False) + 1
df['5-Star Quantile'] = pd.qcut(df['5-Star Ratings'], 4, labels=False) + 1
df['Sales Quantile'] = pd.qcut(df['Yearly Sales'], 4, labels=False) + 1
df['Price Quantile'] = pd.qcut(df['Price'], 4, labels=False) + 1

# Đảo ngược phân vị giá (giá thấp thì tốt hơn)
df['Price Quantile'] = 5 - df['Price Quantile']

# Tính tổng phân vị cho mỗi sản phẩm
df['Total Quantile'] = df['Rating Quantile'] + df['5-Star Quantile'] + df['Sales Quantile'] + df['Price Quantile']

# Sắp xếp sản phẩm dựa trên tổng phân vị
df = df.sort_values(by='Total Quantile', ascending=False)

# Streamlit Dashboard
st.title("Product Optimization Based on Quantiles")

# Hiển thị dữ liệu của các sản phẩm
st.write("Dữ liệu về các sản phẩm:")
st.write(df[['Product', 'Avg Rating', '5-Star Ratings', 'Yearly Sales', 'Price']])

# Hiển thị phân vị và tổng phân vị
st.write("Phân vị của các sản phẩm:")
st.write(df[['Product', 'Rating Quantile', '5-Star Quantile', 'Sales Quantile', 'Price Quantile', 'Total Quantile']])

# Hiển thị sản phẩm tối ưu nhất dựa trên phân vị
optimal_product = df.iloc[0]['Product']
st.write(f"Sản phẩm tối ưu nhất dựa trên phân vị là: {optimal_product}")

# Biểu đồ phân vị
st.write("Biểu đồ phân vị của các sản phẩm:")
st.bar_chart(df.set_index('Product')[['Rating Quantile', '5-Star Quantile', 'Sales Quantile', 'Price Quantile']])
