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
# Đọc dữ liệu từ file CSV
data = pd.read_csv('../getData/data/top5_product.csv')

# Thêm cột 'Top' với số thứ tự cho mỗi sản phẩm
data['Ranked_Product'] = ['Top ' + str(i+1) + ': ' + row['ASIN'] + ' - ' + row['Title'] for i, row in data.iterrows()]

# Tạo selectbox với danh sách sản phẩm đã được xếp hạng
selected_product = st.selectbox(
    "Chọn sản phẩm theo ASIN hoặc tên:",
    data["Ranked_Product"]
)

# Lấy ASIN từ chuỗi chọn
selected_asin = selected_product.split(':')[1].split(' - ')[0].strip()

# Đọc dữ liệu sản phẩm
data = pd.read_csv('../getData/data/product_data.csv')

# Lọc dữ liệu sản phẩm với ASIN tương ứng
selected_product = data[data['ASIN'] == selected_asin]
selected_product
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
# Phân tích đánh giá
st.title("Phân Tích Đánh Giá")
df = pd.read_csv('../getData/data/amazon_reviews_top_products.csv')
df = df[df['ASIN']==selected_asin]
df
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
