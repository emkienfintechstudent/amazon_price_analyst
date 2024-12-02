import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import re
from nltk.corpus import stopwords
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models
from nltk.stem import WordNetLemmatizer

# Tải dữ liệu
st.title("Phân tích review về sản phẩm: Shark AI Ultra Robot Vacuum")
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

# Vẽ biểu đồ tròn cho phân bố cảm xúc
plt.figure(figsize=(7, 7))
plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=['#00FF00', '#FF6347', '#FFD700'])
plt.title('Tỷ lệ phân bố cảm xúc trong các bài đánh giá')
plt.axis('equal')  # Đảm bảo biểu đồ tròn là hình tròn

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)




# THƯ VIỆN VADER
st.markdown('# Dựa theo thư viện VADER')
st.header('Phân tích cảm xúc (Sentiment Analysis) với VADER')

# Khởi tạo analyzer từ VADER
analyzer = SentimentIntensityAnalyzer()

# Tạo DataFrame riêng cho VADER
df_vader = df.copy()  # Copy DataFrame gốc để tránh thay đổi dữ liệu gốc

# Hàm tính toán cảm xúc với VADER
def get_vader_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound']

# Áp dụng hàm VADER vào cột 'Body' để tính cảm xúc
df_vader['vader_sentiment'] = df_vader['Body'].apply(get_vader_sentiment)

# Phân loại cảm xúc dựa trên compound score từ VADER
df_vader['sentiment_vader'] = df_vader['vader_sentiment'].apply(
    lambda x: 'Positive' if x > 0.05 else ('Negative' if x < -0.05 else 'Neutral')
)

# Hiển thị bảng kết quả phân tích cảm xúc từ VADER
st.subheader('Kết quả phân tích cảm xúc từ VADER')
st.write(df_vader[['Rating', 'Body', 'vader_sentiment', 'sentiment_vader']])  # Hiển thị 10 dòng đầu tiên

# Vẽ biểu đồ phân bố cảm xúc

sentiment_counts_vader = df_vader['sentiment_vader'].value_counts()
# Tính toán và hiển thị trung bình cảm xúc từ VADER (compound score)
avg_vader_sentiment = df_vader['vader_sentiment'].mean()
st.subheader('Đánh giá mức độ cảm xúc trung bình (VADER)')
st.write(f"Độ cảm xúc trung bình (compound score) của các bài đánh giá: {avg_vader_sentiment:.3f}")

st.subheader('Biểu đồ phân bố cảm xúc (VADER)')

plt.figure(figsize=(8, 6))
sns.barplot(x=sentiment_counts_vader.index, y=sentiment_counts_vader.values, palette='coolwarm')
plt.title('Phân bố cảm xúc trong các bài đánh giá (VADER)')
plt.xlabel('Cảm xúc')
plt.ylabel('Số lượng review')

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)

# Tóm tắt tỷ lệ cảm xúc
st.subheader('Tóm tắt tỷ lệ cảm xúc')


# Vẽ biểu đồ tròn
plt.figure(figsize=(8, 8))
plt.pie(sentiment_counts_vader, labels=sentiment_counts_vader.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Tỷ lệ phân bố cảm xúc trong các bài đánh giá (VADER)', fontsize=16)

# Hiển thị biểu đồ trong Streamlit
st.pyplot(plt)




st.header('Tạo các phân nhóm dựa trên các yếu tố quan trọng')

st.markdown('# Workcloud dựa trên title và body')

# Lấy dữ liệu từ cột 'Title'
title_text = " ".join(df['Title'].astype(str))  # Kết hợp tất cả tiêu đề lại thành chuỗi

# Tạo WordCloud từ tiêu đề
title_wordcloud = WordCloud(
    width=800, height=400, 
    background_color="white", 
    stopwords=stopwords.words('english'),  # Loại bỏ stopwords tiếng Anh
    colormap="Blues", max_words=100
).generate(title_text)

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






# st.markdown('##  Topic Modeling với LDA (Latent Dirichlet Allocation)')
# st.markdown('''Topic Modeling là một kỹ thuật phân tích văn bản để tự động khám phá các chủ đề (topics) trong một tập hợp tài liệu. Một trong những phương pháp phổ biến nhất để thực hiện topic modeling là LDA (Latent Dirichlet Allocation). LDA có thể giúp bạn tìm ra các chủ đề chính mà khách hàng quan tâm trong các bài đánh giá.
# ''')

# # Tạo bản sao của DataFrame gốc để xử lý
# df_topic = df.copy()

# # Khởi tạo lemmatizer
# lemmatizer = WordNetLemmatizer()

# # Tiền xử lý văn bản: Loại bỏ stopwords, chuyển thành chữ thường, và lemmatize
# def preprocess_text(text):
#     # Chuyển thành chữ thường
#     text = text.lower()
#     # Tokenize văn bản và loại bỏ stopwords
#     tokens = nltk.word_tokenize(text)
#     stop_words = set(stopwords.words('english'))
#     tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words]
#     return ' '.join(tokens)

# # Áp dụng tiền xử lý cho cột 'Title' và 'Body'
# df_topic['processed_body'] = df_topic['Body'].apply(preprocess_text)
# df_topic['processed_title'] = df_topic['Title'].apply(preprocess_text)

# # Kết hợp cả Title và Body để tạo một văn bản chung
# df_topic['processed_text'] = df_topic['processed_title'] + ' ' + df_topic['processed_body']

# # Xem qua dữ liệu sau khi đã được tiền xử lý
# st.write(df_topic[['Title', 'Body', 'processed_text']])

# # Sử dụng TF-IDF Vectorizer để chuyển đổi văn bản thành ma trận số
# vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
# X = vectorizer.fit_transform(df_topic['processed_text'])

# # Xem qua các từ khóa trong dữ liệu
# feature_names = vectorizer.get_feature_names_out()
# st.write("Các từ khóa:", feature_names)  


# # Chuyển ma trận TF-IDF thành định dạng có thể sử dụng cho gensim
# corpus = [corpora.Dictionary([text.split()]).doc2bow(text.split()) for text in df_topic['processed_text']]

# # Tạo từ điển và chuyển dữ liệu vào corpus
# dictionary = corpora.Dictionary(df_topic['processed_text'].apply(str.split))

# # Tạo và huấn luyện mô hình LDA
# lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

# # Hiển thị các chủ đề
# topics = lda_model.print_topics(num_words=5)
# for topic in topics:
#     st.write(topic)

# # Không sử dụng pyLDAvis.enable_notebook() vì nó chỉ hoạt động trong Jupyter Notebook
# vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

# # Hiển thị trực quan hóa trong Streamlit
# st.subheader("Trực quan hóa chủ đề với LDA")
# # Dùng pyLDAvis.show() hoặc st.write() để hiển thị trực quan hóa trong Streamlit
# pyLDAvis.show(vis)