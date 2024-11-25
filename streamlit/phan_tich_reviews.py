import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load dữ liệu
st.title("Phân tích review về sản phẩm: Shark AI Ultra Robot Vacuum")
data = pd.read_csv('../getData/unique_reviews.csv')

# Tổng quan
st.header("Tổng quan")
num_reviews = len(data)
average_rating = data['rating'].mean()

col1, col2 = st.columns(2)
col1.metric("Số lượng đánh giá", num_reviews)
col2.metric("Đánh giá trung bình", round(average_rating, 2))

# Biểu đồ tròn tỷ lệ phần trăm đánh giá theo mức rating
rating_counts = data['rating'].value_counts().sort_index()
rating_percentages = (rating_counts / num_reviews) * 100

fig1, ax1 = plt.subplots(figsize=(8, 8))
ax1.pie(
    rating_percentages,
    labels=rating_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.Paired.colors
)
ax1.set_title("Tỷ lệ phần trăm đánh giá", fontsize=16)
st.pyplot(fig1)


st.subheader("Phân tích nội dung đánh giá (Text Analysis")

# Word Cloud từ tiêu đề đánh giá
st.subheader("Word Cloud từ tiêu đề đánh giá")
title_text = " ".join(data['title'].astype(str))
title_wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white"
).generate(title_text)

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.imshow(title_wordcloud, interpolation="bilinear")
ax2.axis("off")
ax2.set_title("Word Cloud từ tiêu đề đánh giá", fontsize=16)
st.pyplot(fig2)

# Phân tích Word Cloud
st.header("Phân tích tần suất các từ trong tiêu đề")

# Lấy tần suất các từ từ WordCloud
word_freq = title_wordcloud.process_text(title_text)

# Chuyển đổi sang DataFrame để phân tích
word_freq_df = pd.DataFrame(list(word_freq.items()), columns=['Từ', 'Tần suất'])
word_freq_df = word_freq_df.sort_values(by='Tần suất', ascending=False).head(10)  # Lấy 10 từ phổ biến nhất

# Hiển thị bảng tần suất
st.subheader("Top 10 từ phổ biến trong tiêu đề đánh giá")
st.dataframe(word_freq_df)

# Vẽ biểu đồ cột tần suất các từ
st.subheader("Biểu đồ tần suất các từ phổ biến")
plt.figure(figsize=(10, 6))
plt.barh(word_freq_df['Từ'], word_freq_df['Tần suất'], color='skyblue')
plt.xlabel('Tần suất')
plt.ylabel('Từ')
plt.title('Tần suất các từ phổ biến trong tiêu đề đánh giá', fontsize=16)
plt.gca().invert_yaxis()  # Đảo ngược trục y để từ có tần suất cao nhất nằm trên cùng
st.pyplot(plt)






























# # Word Cloud từ nội dung đánh giá
# st.subheader("Word Cloud từ nội dung đánh giá")
# body_text = " ".join(data['body'].astype(str))
# body_wordcloud = WordCloud(
#     width=800,
#     height=400,
#     background_color="white",
#     colormap="viridis",
#     max_words=100
# ).generate(body_text)

# fig3, ax3 = plt.subplots(figsize=(10, 6))
# ax3.imshow(body_wordcloud, interpolation="bilinear")
# ax3.axis("off")
# ax3.set_title("Word Cloud từ nội dung đánh giá", fontsize=16)
# st.pyplot(fig3)
