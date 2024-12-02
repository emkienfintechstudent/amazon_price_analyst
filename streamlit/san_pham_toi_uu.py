import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# Load dữ liệu
df = pd.read_csv('../getData/data/product_data_vaccum_ranking.csv')
st.header("Chấm điểm bằng phương pháp quantitile")

# Set title
df=df.drop_duplicates(subset='ASIN', keep='last')
df=df[df['robotic_vacuums_rank'].notna()]
# Giả sử df là DataFrame của bạn
columns_to_check = [
    'One Star Ratings Count', 'Five Star Ratings Count', 'Price', 
    'Rating Average', 'Ratings Total', 'robotic_vacuums_rank'
]

# Lọc bỏ các dòng có NaN trong các cột đã chỉ định
df_top_5 = df.dropna(subset=columns_to_check)
# Hàm tính điểm dựa trên quantiles (gán điểm từ 1 đến 10)
def calculate_quantile_score(df, column, n_quantiles=10, is_inverse=False):
    # Nếu cần tính ngược (ví dụ robotic_vacuums_rank, price, One Star Ratings Count)
    if is_inverse:
        df[column] = -df[column]  # Đảo ngược giá trị của cột
    
    # Tính quantiles cho cột (gán điểm từ 1 đến 10)
    quantiles = pd.qcut(df[column], n_quantiles, labels=False, duplicates='drop') + 1  # labels=False để không có nhãn, rồi +1 để điểm bắt đầu từ 1
    return quantiles

# Giả sử df là DataFrame của bạn
columns_to_check = [
    'One Star Ratings Count', 'Five Star Ratings Count', 'Price', 
    'Rating Average', 'Ratings Total', 'robotic_vacuums_rank'
]

# Lọc bỏ các dòng có NaN trong các cột đã chỉ định
df_top_5 = df.dropna(subset=columns_to_check)
# Tính điểm cho từng cột dựa trên quantile
df_top_5['robotic_vacuums_rank_score'] = calculate_quantile_score(df_top_5, 'robotic_vacuums_rank', is_inverse=True)
df_top_5['price_score'] = calculate_quantile_score(df_top_5, 'Price', is_inverse=True)
df_top_5['one_star_score'] = calculate_quantile_score(df_top_5, 'One Star Ratings Count', is_inverse=True)
df_top_5['five_star_score'] = calculate_quantile_score(df_top_5, 'Five Star Ratings Count', is_inverse=False)
df_top_5['rating_avg_score'] = calculate_quantile_score(df_top_5, 'Rating Average', is_inverse=False)
df_top_5['ratings_total_score'] = calculate_quantile_score(df_top_5, 'Ratings Total', is_inverse=False)
# Thêm cột 'total_score' là tổng các điểm của từng cột
df_top_5['total_score'] = (df_top_5['robotic_vacuums_rank_score'] + 
                            df_top_5['price_score'] + 
                            df_top_5['one_star_score'] + 
                            df_top_5['five_star_score'] + 
                            df_top_5['rating_avg_score'] + 
                            df_top_5['ratings_total_score'])

# Kiểm tra kết quả
df_top_5
st.header("Top 5 sản phẩm tốt nhất trên thị trường")

st.write(df_top_5[['ASIN', 'Title', 'robotic_vacuums_rank_score', 'price_score', 'one_star_score', 'five_star_score', 'rating_avg_score', 'ratings_total_score','total_score']].sort_values(by='total_score', ascending=False).head())

df_top_5_sorted = df_top_5.sort_values(by='total_score', ascending=False)
score_columns = ['robotic_vacuums_rank_score', 'price_score', 'one_star_score', 
                 'five_star_score', 'rating_avg_score', 'ratings_total_score', 'total_score']
top_5_products = df_top_5_sorted.head(5)

# Màu sắc riêng biệt cho từng sản phẩm
colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#8A2BE2']  # Các màu sắc riêng biệt

# Tạo biểu đồ thanh
plt.figure(figsize=(10, 6))

# Vẽ biểu đồ thanh với màu sắc cụ thể cho từng sản phẩm
plt.bar(top_5_products['ASIN'], top_5_products['total_score'], color=colors)

# Thêm tiêu đề và các nhãn
plt.title('Top 5 Products by Total Score', fontsize=16)
plt.xlabel('ASIN', fontsize=12)
plt.ylabel('Total Score', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x cho dễ đọc

# Thêm số điểm vào mỗi thanh
for i, value in enumerate(top_5_products['total_score']):
    plt.text(i, value + 0.1, f'{value:.2f}', ha='center', va='bottom', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)

st.header("Top 5 sản phẩm tệ nhất trên thị trường")
# Chọn 5 sản phẩm có tổng điểm thấp nhất
top_5_worst_products = df_top_5_sorted.tail(5)
top_5_worst_products
# Màu sắc riêng biệt cho từng sản phẩm
colors = ['#FF6347', '#4682B4', '#32CD32', '#FFD700', '#8A2BE2']  # Các màu sắc riêng biệt

# Tạo biểu đồ thanh
plt.figure(figsize=(10, 6))

# Vẽ biểu đồ thanh với màu sắc cụ thể cho từng sản phẩm
plt.bar(top_5_worst_products['ASIN'], top_5_worst_products['total_score'], color=colors)

# Thêm tiêu đề và các nhãn
plt.title('Top 5 Products with Lowest Total Score', fontsize=16)
plt.xlabel('ASIN', fontsize=12)
plt.ylabel('Total Score', fontsize=12)
plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x cho dễ đọc

# Thêm số điểm vào mỗi thanh
for i, value in enumerate(top_5_worst_products['total_score']):
    plt.text(i, value + 0.1, f'{value:.2f}', ha='center', va='bottom', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)


st.header("Top 5 sản phẩm bán chạy nhất")

# Đảm bảo 'Annual Unit Sales' là kiểu số
df['Annual Unit Sales'] = pd.to_numeric(df['Annual Unit Sales'], errors='coerce')

# Lọc ra top 5 sản phẩm bán chạy nhất theo Annual Unit Sales
top_5_best_selling = df.nlargest(5, 'Annual Unit Sales')

# Tạo biểu đồ bar ngang
plt.figure(figsize=(10, 6))
sns.barplot(data=top_5_best_selling, y='ASIN', x='Annual Unit Sales', palette='viridis')

# Thêm tiêu đề và các nhãn
plt.title('Top 5 Best Selling Products by Annual Unit Sales', fontsize=16)
plt.xlabel('Annual Unit Sales', fontsize=12)
plt.ylabel('ASIN', fontsize=12)

# Thêm số lượng sản phẩm vào mỗi thanh (tương tự như bạn làm với top 5 worst products)
for i, value in enumerate(top_5_best_selling['Annual Unit Sales']):
    plt.text(value, i, f'{value:.0f}', va='center', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
plt.tight_layout()
st.pyplot(plt)
st.header("Top 5 sản phẩm được nhiều đánh giá nhất")
# Đảm bảo 'Ratings Total' là kiểu số
df['Ratings Total'] = pd.to_numeric(df['Ratings Total'], errors='coerce')

# Lọc ra top 5 sản phẩm được đánh giá nhiều nhất theo Ratings Total
top_5_most_reviewed = df.nlargest(5, 'Ratings Total')

# Tạo biểu đồ cột
plt.figure(figsize=(10, 6))
sns.barplot(data=top_5_most_reviewed, x='ASIN', y='Ratings Total', palette='viridis')

# Thêm tiêu đề và các nhãn
plt.title('Top 5 Products with the Most Reviews by Ratings Total', fontsize=16)
plt.xlabel('ASIN', fontsize=12)
plt.ylabel('Ratings Total', fontsize=12)

# Thêm số lượng đánh giá vào mỗi thanh
for i, value in enumerate(top_5_most_reviewed['Ratings Total']):
    plt.text(i, value + 50, f'{value:.0f}', ha='center', va='bottom', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
plt.tight_layout()
st.pyplot(plt)
st.header("Top 5 sản phẩm có nhiều đánh giá 1 sao nhất")
# Đảm bảo 'One Star Ratings Count' là kiểu số
df['One Star Ratings Count'] = pd.to_numeric(df['One Star Ratings Count'], errors='coerce')

# Lọc ra top 5 sản phẩm có nhiều đánh giá 1 sao nhất
top_5_one_star = df.nlargest(5, 'One Star Ratings Count')

# Tạo biểu đồ cột
plt.figure(figsize=(10, 6))
sns.barplot(data=top_5_one_star, x='ASIN', y='One Star Ratings Count', palette='coolwarm')

# Thêm tiêu đề và các nhãn
plt.title('Top 5 Products with the Most 1-Star Reviews', fontsize=16)
plt.xlabel('ASIN', fontsize=12)
plt.ylabel('One Star Ratings Count', fontsize=12)

# Thêm số lượng đánh giá 1 sao vào mỗi thanh
for i, value in enumerate(top_5_one_star['One Star Ratings Count']):
    plt.text(i, value + 10, f'{value:.0f}', ha='center', va='bottom', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
plt.tight_layout()
st.pyplot(plt)
st.header("Top 5 sản phẩm có nhiều đánh giá 5 sao nhất")
# Đảm bảo 'Five Star Ratings Count' là kiểu số
df['Five Star Ratings Count'] = pd.to_numeric(df['Five Star Ratings Count'], errors='coerce')

# Lọc ra top 5 sản phẩm có nhiều đánh giá 5 sao nhất
top_5_five_star = df.nlargest(5, 'Five Star Ratings Count')

# Tạo biểu đồ cột
plt.figure(figsize=(10, 6))
sns.barplot(data=top_5_five_star, x='ASIN', y='Five Star Ratings Count', palette='coolwarm')

# Thêm tiêu đề và các nhãn
plt.title('Top 5 Products with the Most 5-Star Reviews', fontsize=16)
plt.xlabel('ASIN', fontsize=12)
plt.ylabel('Five Star Ratings Count', fontsize=12)

# Thêm số lượng đánh giá 5 sao vào mỗi thanh
for i, value in enumerate(top_5_five_star['Five Star Ratings Count']):
    plt.text(i, value + 10, f'{value:.0f}', ha='center', va='bottom', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
plt.tight_layout()
st.pyplot(plt)

st.header("Top 5 sản phẩm có giá bán cao nhất")
# Đảm bảo 'Price' là kiểu số
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Lọc ra top 5 sản phẩm có giá bán cao nhất
top_5_expensive_products = df.nlargest(5, 'Price')

# Tạo biểu đồ cột
plt.figure(figsize=(10, 6))
sns.barplot(data=top_5_expensive_products, x='ASIN', y='Price', palette='magma')

# Thêm tiêu đề và các nhãn
plt.title('Top 5 Most Expensive Products', fontsize=16)
plt.xlabel('ASIN', fontsize=12)
plt.ylabel('Price', fontsize=12)

# Thêm giá bán vào mỗi thanh
for i, value in enumerate(top_5_expensive_products['Price']):
    plt.text(i, value + 10, f'${value:.2f}', ha='center', va='bottom', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
plt.tight_layout()
st.pyplot(plt)

st.header("Top 5 sản phẩm giá bán thấp nhất")

# Đảm bảo 'Price' là kiểu số
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Lọc ra top 5 sản phẩm có giá bán thấp nhất
top_5_cheapest_products = df.nsmallest(5, 'Price')

# Tạo biểu đồ cột
plt.figure(figsize=(10, 6))
sns.barplot(data=top_5_cheapest_products, x='ASIN', y='Price', palette='coolwarm')

# Thêm tiêu đề và các nhãn
plt.title('Top 5 Cheapest Products', fontsize=16)
plt.xlabel('ASIN', fontsize=12)
plt.ylabel('Price', fontsize=12)

# Thêm giá bán vào mỗi thanh
for i, value in enumerate(top_5_cheapest_products['Price']):
    plt.text(i, value + 0.1, f'${value:.2f}', ha='center', va='bottom', fontsize=12)

# Hiển thị biểu đồ trong Streamlit
plt.tight_layout()
st.pyplot(plt)

st.header("Top 5 sản phẩm có mức độ phổ biến nhất trong danh mục Vaccum cleaner")
# Lọc các dòng có robotic_vacuums_rank không phải NaN
df_filtered = df[df['robotic_vacuums_rank'].notna()]

# Sắp xếp DataFrame theo 'robotic_vacuums_rank' và lấy top 5 sản phẩm với rank thấp nhất
top_5_robotic_vacuums = df_filtered.sort_values(by='robotic_vacuums_rank').head(5)

# Hiển thị top 5 sản phẩm
st.write(top_5_robotic_vacuums[['ASIN', 'Title', 'robotic_vacuums_rank']])




