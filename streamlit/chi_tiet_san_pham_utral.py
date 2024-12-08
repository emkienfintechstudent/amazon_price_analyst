import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models

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


# Tải dữ liệu
st.title("Phân tích review")
df = pd.read_csv('../getData/data/amazon_reviews_remove_space_remove_duplicate.csv')

# Tổng quan về dữ liệu
st.header('Tổng quan dữ liệu reviews')
st.subheader('Tổng quan về số lượng')

# Tổng quan về bộ dữ liệu
st.metric("Số lượng reviews lấy được", f"{df['Rating'].count()}/7630")

# Tính số lượng review cho mỗi Rating
rating_counts = df['Rating'].value_counts().sort_index()

# Vẽ biểu đồ số lượng review theo Rating
plt.figure(figsize=(8, 6))
sns.barplot(x=rating_counts.index, y=rating_counts.values, palette='Blues_d')
plt.title("Số lượng review theo Rating")
plt.xlabel("Rating")
plt.ylabel("Số lượng review")
plt.xticks(rotation=90)

# Thêm chú thích số review vào mỗi cột
for i in range(len(rating_counts)):
    plt.text(i, rating_counts.values[i] + 0.5, str(rating_counts.values[i]), ha='center', va='bottom')

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)

# Phân tích từ khóa và cảm nhận (Sentiment Analysis)
st.header('Phân tích từ khóa và cảm nhận (Sentiment Analysis)')

## TEXTBLOB
st.subheader('Dựa theo thư viện textblob')
# Tạo bản sao của DataFrame gốc
df_textblob = df.copy()

# Phân tích cảm xúc với TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return polarity, subjectivity

# Áp dụng TextBlob lên cột 'Body' của dữ liệu
df_textblob['polarity'], df_textblob['subjectivity'] = zip(*df_textblob['Body'].apply(get_sentiment))

# Phân loại cảm xúc dựa trên polarity
df_textblob['sentiment_textblob'] = df_textblob['polarity'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

# Hiển thị bảng kết quả phân tích cảm xúc từ TextBlob
st.subheader('Kết quả phân tích cảm xúc từ TextBlob')
st.write(df_textblob[['Rating', 'Body', 'polarity', 'subjectivity', 'sentiment_textblob']].head(10))  # Hiển thị 10 dòng đầu tiên

# Tính trung bình độ phân cực (polarity)
average_polarity = df_textblob['polarity'].mean()
# Tính trung bình độ chủ quan 
average_subjectivity = df_textblob['subjectivity'].mean()

# Áp dụng if-else để phân loại cảm xúc trung bình
if average_polarity > 0.1:
    overall_sentiment = 'Tích cực'
elif average_polarity < -0.1:
    overall_sentiment = 'Tiêu cực'
else:
    overall_sentiment = 'Bình thường'
# Áp dụng if-else để phân loại tính chủ quan trung bình
if average_subjectivity > 0.5:
    overall_subjectivity = 'Chủ quan'
elif average_subjectivity > 0.4:
        overall_subjectivity = 'Mức độ chủ quan ở mức trung bình'

else:
    overall_subjectivity = 'Khách quan'
# Hiển thị kết quả độ phân cực trung bình và phân loại cảm xúc
st.subheader('Tóm tắt cảm xúc trung bình của các bài đánh giá')
st.write(f"Trung bình độ phân cực cảm xúc: {average_polarity:.2f}")
st.write(f"Cảm xúc trung bình: {overall_sentiment}")
st.write(f"Trung bình mức độ chủ quan: {average_subjectivity:.2f}")
st.write(f"Cảm xúc trung bình: {overall_subjectivity}")

# Vẽ biểu đồ phân bố cảm xúc (TextBlob)
st.subheader('Biểu đồ phân bố cảm xúc (TextBlob)')
sentiment_counts = df_textblob['sentiment_textblob'].value_counts()

plt.figure(figsize=(8, 6))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='coolwarm')
plt.title('Phân bố cảm xúc trong các bài đánh giá (TextBlob)')
plt.xlabel('Cảm xúc')
plt.ylabel('Số lượng review')

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)

# Tóm tắt tổng quan về tỷ lệ cảm xúc từ TextBlob
# Vẽ biểu đồ phân bố cảm xúc (TextBlob)
st.subheader('Biểu đồ phân bố cảm xúc (TextBlob)')
sentiment_counts = df_textblob['sentiment_textblob'].value_counts()

# Sử dụng palette 'muted' từ seaborn
colors = sns.color_palette("muted", n_colors=len(sentiment_counts))

# Vẽ biểu đồ tròn với màu sắc hài hòa
plt.figure(figsize=(7, 7))
plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title('Tỷ lệ phân bố cảm xúc trong các bài đánh giá')
plt.axis('equal')  # Đảm bảo biểu đồ tròn là hình tròn
plt.show()


# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)



st.header('Tạo các phân nhóm dựa trên các yếu tố quan trọng')

st.markdown('# Word cloud dựa trên title và body')

# Lấy dữ liệu từ cột 'Title'
title_text = " ".join(df['Title'].astype(str))  # Kết hợp tất cả tiêu đề lại thành chuỗi

# Tạo WordCloud từ tiêu đề
title_wordcloud = WordCloud(
    width=800, height=400, 
    background_color="white", 
    stopwords=stopwords.words('english'),  # Loại bỏ stopwords tiếng Anh
    colormap="Blues", max_words=100
).generate(title_text)
st.subheader("Word Cloud từ Tiêu đề Đánh giá")

# Hiển thị WordCloud cho tiêu đề
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(title_wordcloud, interpolation="bilinear")
ax.axis("off")
ax.set_title("Word Cloud từ Tiêu đề Đánh giá", fontsize=16)
st.pyplot(fig)

# Tạo WordCloud từ Body
st.subheader("Word Cloud từ nội dung đánh giá")

# Lấy dữ liệu từ cột 'Body'
body_text = " ".join(df['Body'].astype(str))  # Kết hợp tất cả nội dung lại thành chuỗi

# Tạo WordCloud từ nội dung đánh giá
body_wordcloud = WordCloud(
    width=800, height=400, 
    background_color="white", 
    stopwords=stopwords.words('english'),  # Loại bỏ stopwords tiếng Anh
    colormap="viridis", max_words=100
).generate(body_text)

# Hiển thị WordCloud cho nội dung
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.imshow(body_wordcloud, interpolation="bilinear")
ax2.axis("off")
ax2.set_title("Word Cloud từ Nội dung Đánh giá", fontsize=16)
st.pyplot(fig2)
