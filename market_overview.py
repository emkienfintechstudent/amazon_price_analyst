from sklearn.cluster import KMeans
import pandas as pd
# Dữ liệu giả lập
data = {
    'Product': ['Product A', 'Product B', 'Product C'],
    'Avg Rating': [4.5, 4.2, 3.8],
    '5-Star Ratings': [1000, 800, 500],
    'Yearly Sales': [7200, 4800, 2400],
    'Price': [100, 80, 70]
}

df = pd.DataFrame(data)

# Chuẩn hóa dữ liệu
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df[['Avg Rating', '5-Star Ratings', 'Yearly Sales', 'Price']])

# Áp dụng K-means clustering
kmeans = KMeans(n_clusters=2, random_state=0).fit(df_scaled)
df['Cluster'] = kmeans.labels_

print(df)
