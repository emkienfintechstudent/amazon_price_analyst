import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
from textblob import TextBlob

# Load dữ liệu
st.title("Phân tích review về sản phẩm: Shark AI Ultra Robot Vacuum")
df = pd.read_csv('../getData/data/amazon_reviews_remove_space_remove_duplicate.csv')
df



# Tính số lượng review cho mỗi Rating
rating_counts = df['Rating'].value_counts().sort_index()
st.header('Tổng quan dữ liệu reviews')

st.subheader('Tổng quan về số lượng')
### Tổng quan về bộ dữ liệu 
st.metric("Số lượng reviews lấy được", f"{df['Rating'].count()}/7630")
# Vẽ biểu đồ
plt.figure(figsize=(8, 6))
sns.barplot(x=rating_counts.index, y=rating_counts.values, palette='Blues_d')

# Đặt tiêu đề và nhãn trục
plt.title("Số lượng review theo Rating")
plt.xlabel("Rating")
plt.ylabel("Số lượng review")

# Đặt nhãn trục x thẳng đứng
plt.xticks(rotation=90)

# Thêm chú thích số review vào mỗi cột
for i in range(len(rating_counts)):
    plt.text(i, rating_counts.values[i] + 0.5, str(rating_counts.values[i]), ha='center', va='bottom')

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)


st.subheader('Tổng quan về từ khóa')
st.header('Phân tích từ khóa và cảm nhận (Sentiment Analysis)')
st.subheader('thêm bộ lọc ở đây')

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return polarity, subjectivity

# Sử dụng trên cột "Body" của dữ liệu review
df['polarity'], df['subjectivity'] = zip(*df['Body'].apply(get_sentiment))

# Phân loại cảm xúc dựa trên polarity
df['sentiment_textblob'] = df['polarity'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
df
# st.subheader("Phân tích nội dung đánh giá (Text Analysis")

# # Word Cloud từ tiêu đề đánh giá
# st.subheader("Word Cloud từ tiêu đề đánh giá")
# title_text = " ".join(data['title'].astype(str))
# title_wordcloud = WordCloud(
#     width=800,
#     height=400,
#     background_color="white"
# ).generate(title_text)

# fig2, ax2 = plt.subplots(figsize=(10, 6))
# ax2.imshow(title_wordcloud, interpolation="bilinear")
# ax2.axis("off")
# ax2.set_title("Word Cloud từ tiêu đề đánh giá", fontsize=16)
# st.pyplot(fig2)

# # Phân tích Word Cloud
# st.header("Phân tích tần suất các từ trong tiêu đề")

# # Lấy tần suất các từ từ WordCloud
# word_freq = title_wordcloud.process_text(title_text)

# # Chuyển đổi sang DataFrame để phân tích
# word_freq_df = pd.DataFrame(list(word_freq.items()), columns=['Từ', 'Tần suất'])
# word_freq_df = word_freq_df.sort_values(by='Tần suất', ascending=False).head(10)  # Lấy 10 từ phổ biến nhất

# # Hiển thị bảng tần suất
# st.subheader("Top 10 từ phổ biến trong tiêu đề đánh giá")
# st.dataframe(word_freq_df)

# # Vẽ biểu đồ cột tần suất các từ
# st.subheader("Biểu đồ tần suất các từ phổ biến")
# plt.figure(figsize=(10, 6))
# plt.barh(word_freq_df['Từ'], word_freq_df['Tần suất'], color='skyblue')
# plt.xlabel('Tần suất')
# plt.ylabel('Từ')
# plt.title('Tần suất các từ phổ biến trong tiêu đề đánh giá', fontsize=16)
# plt.gca().invert_yaxis()  # Đảo ngược trục y để từ có tần suất cao nhất nằm trên cùng
# st.pyplot(plt)






























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
