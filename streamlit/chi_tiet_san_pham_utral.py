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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models

# Tiêu đề trang
st.title("Chi Tiết Sản Phẩm: Shark AI Ultra Robot Vacuum")
st.subheader("ASIN: B09T4YZGQR")

# Đọc dữ liệu
data = pd.read_csv('../getData/data/product_data.csv')
history_price = pd.read_csv('../getData/data/price_history.csv')
data_utral = data[data['ASIN'] == 'B09T4YZGQR']
features = data_utral['Feature Bullets'].values[0].split(";")
Technical_Specifications = data_utral['Technical Specifications'].values[0].split(";")
last_price = history_price['price'].iloc[-1]

# Giới thiệu sản phẩm
st.header("Giới Thiệu Sản Phẩm")
st.image("../getData/utral.jpg", width=300)

st.markdown(f"""
    **Tiêu đề sản phẩm**: {data_utral['Title'].values[0]}  
    **Hãng**: {data_utral['Brand'].values[0]}  
    **Danh mục**: {data_utral['Categories'].values[0]}  
    **Giá hiện tại**: ${last_price}  
""")

st.subheader("Đặc Điểm Nổi Bật")
for feature in features:
    st.markdown(f"- {feature.strip()}")

st.subheader("Tính Năng Đặc Biệt")
for tech_spec in Technical_Specifications:
    st.markdown(f"- {tech_spec.strip()}")

# Xếp hạng sản phẩm
st.markdown(f"**Xếp hạng sản phẩm**: {data_utral['Title'].values[0]}")

# Tổng quan về đánh giá sản phẩm
st.header("Tổng Quan Đánh Giá Sản Phẩm")
col1, col2 = st.columns(2)
col1.metric("Số lượng đánh giá", data_utral['Ratings Total'].values[0])
col2.metric("Đánh giá trung bình", data_utral['Rating Average'].values[0])

# Tính tỷ lệ đánh giá theo sao
ratings = data_utral[['One Star Ratings Count', 'Two Star Ratings Count', 'Three Star Ratings Count', 'Four Star Ratings Count', 'Five Star Ratings Count']].values[0]
total_rating = data_utral['Ratings Total'].values[0]
rating_labels = ['1 sao', '2 sao', '3 sao', '4 sao', '5 sao']
rating_sizes = [round(rating / total_rating * 100, 2) for rating in ratings]
explode = [0.1 if i == rating_sizes.index(max(rating_sizes)) else 0 for i in range(len(rating_sizes))]

# Biểu đồ phân bổ đánh giá
fig1, ax1 = plt.subplots()
ax1.pie(rating_sizes, explode=explode, labels=rating_labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
ax1.set_title("Phân Bố Đánh Giá Sản Phẩm")
st.pyplot(fig1)

# Lịch sử giá sản phẩm
st.header("Lịch Sử Giá Sản Phẩm")
history_price["date"] = pd.to_datetime(history_price[["year", "month", "day"]])
plt.figure(figsize=(10, 6))
plt.plot(history_price['date'], history_price['price'], linestyle='-', label="Price")
plt.title("Lịch Sử Giá Sản Phẩm")
plt.xlabel("Ngày")
plt.ylabel("Giá (USD)")
plt.grid(True)
plt.legend()
st.pyplot(plt)

# Thống kê giá
min_price = history_price['price'].min()
average_price = history_price['price'].mean()
max_price = history_price['price'].max()
st.markdown(f"""
    - **Giá trung bình**: ${average_price:,.2f}  
    - **Giá thấp nhất**: ${min_price:,.2f}  
    - **Giá cao nhất**: ${max_price:,.2f}  
    - **Giá hiện tại**: ${last_price:,.2f}  
""")

# Phân tích đánh giá
st.title("Phân Tích Đánh Giá")

# Đọc dữ liệu reviews
df = pd.read_csv('../getData/data/amazon_reviews_remove_space_remove_duplicate.csv')

# Tổng quan về số lượng review
st.header("Tổng Quan Số Lượng Đánh Giá")
st.metric("Số lượng review", f"{df['Rating'].count()}/7630")

# Biểu đồ số lượng review theo rating
rating_counts = df['Rating'].value_counts().sort_index()
plt.figure(figsize=(8, 6))
sns.barplot(x=rating_counts.index, y=rating_counts.values, palette='Blues_d')
plt.title("Số Lượng Đánh Giá Theo Rating")
plt.xlabel("Rating")
plt.ylabel("Số lượng đánh giá")
plt.xticks(rotation=90)
for i in range(len(rating_counts)):
    plt.text(i, rating_counts.values[i] + 0.5, str(rating_counts.values[i]), ha='center', va='bottom')
st.pyplot(plt)

# Phân tích cảm xúc với TextBlob
st.header("Phân Tích Cảm Xúc (Sentiment Analysis)")
df_textblob = df.copy()

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

df_textblob['polarity'], df_textblob['subjectivity'] = zip(*df_textblob['Body'].apply(get_sentiment))
df_textblob['sentiment'] = df_textblob['polarity'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

# Tóm tắt cảm xúc
average_polarity = df_textblob['polarity'].mean()
average_subjectivity = df_textblob['subjectivity'].mean()

if average_polarity > 0.1:
    overall_sentiment = 'Tích cực'
elif average_polarity < -0.1:
    overall_sentiment = 'Tiêu cực'
else:
    overall_sentiment = 'Bình thường'

if average_subjectivity > 0.5:
    overall_subjectivity = 'Chủ quan'
elif average_subjectivity > 0.4:
    overall_subjectivity = 'Mức độ chủ quan'
else:
    overall_subjectivity = 'Khách quan'

st.markdown(f"""
    **Trung bình độ phân cực**: {average_polarity:.2f}  
    **Cảm xúc trung bình**: {overall_sentiment}  
    **Trung bình mức độ chủ quan**: {average_subjectivity:.2f}  
    **Tính chất chủ quan**: {overall_subjectivity}  
""")

# Biểu đồ phân bố cảm xúc
sentiment_counts = df_textblob['sentiment'].value_counts()
plt.figure(figsize=(8, 6))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='coolwarm')
plt.title('Phân Bố Cảm Xúc Các Đánh Giá')
plt.xlabel('Cảm xúc')
plt.ylabel('Số lượng')
st.pyplot(plt)

# Phân tích từ khóa với TF-IDF
st.header("Phân Tích Từ Khóa Với TF-IDF")

# Tiền xử lý văn bản và tính toán TF-IDF
reviews_cleaned = df['Body'].str.lower().str.replace(r'[^\w\s]', '', regex=True)
vectorizer = TfidfVectorizer(stop_words='english', max_features=20)
X_tfidf = vectorizer.fit_transform(reviews_cleaned)

# Lấy từ khóa TF-IDF
words_tfidf = vectorizer.get_feature_names_out()
tfidf_scores = X_tfidf.sum(axis=0).A1
tfidf_word_freq = pd.DataFrame(list(zip(words_tfidf, tfidf_scores)), columns=['word', 'tfidf_score'])
tfidf_word_freq = tfidf_word_freq.sort_values(by='tfidf_score', ascending=False)

# Vẽ biểu đồ cột ngang
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(tfidf_word_freq['word'].head(20), tfidf_word_freq['tfidf_score'].head(20), color='lightcoral')

# Thêm nhãn dữ liệu
for index, value in enumerate(tfidf_word_freq['tfidf_score'].head(20)):
    ax.text(value, index, f'{value:.3f}', va='center', ha='left', fontsize=10)

ax.set_xlabel('TF-IDF Score')
ax.set_ylabel('Words')
ax.set_title('Top 20 Từ Khóa Dựa Trên TF-IDF')
ax.invert_yaxis()

st.pyplot(fig)

# Phân tích chủ đề với LDA
st.header("Phân Tích Chủ Đề với LDA")

lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X_tfidf)

# Hiển thị kết quả LDA
n_top_words = 10
words = vectorizer.get_feature_names_out()
lda_results = ""
for topic_idx, topic in enumerate(lda.components_):
    lda_results += f"**Chủ đề #{topic_idx + 1}:**\n"
    topic_words = " ".join([words[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
    lda_results += f"{topic_words}\n\n"

st.text(lda_results)

# Tạo WordCloud từ Tiêu Đề và Nội Dung
st.header("Word Cloud Phân Tích Tiêu Đề và Nội Dung")

# Từ khóa từ Tiêu đề
title_text = " ".join(df['Title'].astype(str))
title_wordcloud = WordCloud(width=800, height=400, background_color="white", stopwords=stopwords.words('english'), colormap="Blues", max_words=100).generate(title_text)

fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(title_wordcloud, interpolation="bilinear")
ax.axis("off")
ax.set_title("Word Cloud từ Tiêu Đề Đánh Giá")
st.pyplot(fig)

# Từ khóa từ Nội dung
body_text = " ".join(df['Body'].astype(str))
body_wordcloud = WordCloud(width=800, height=400, background_color="white", stopwords=stopwords.words('english'), colormap="viridis", max_words=100).generate(body_text)

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.imshow(body_wordcloud, interpolation="bilinear")
ax2.axis("off")
ax2.set_title("Word Cloud từ Nội Dung Đánh Giá")
st.pyplot(fig2)
