# -*- coding: utf-8 -*-
# Zomato Restaurant Clustering And Sentiment Analysis.ipynb


import re

import matplotlib.pyplot as plt
import nltk
# Import Libraries
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans, DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from wordcloud import WordCloud

nltk.download('stopwords')
nltk.download('punkt')
import warnings

warnings.filterwarnings('ignore')

# importing the dataset
path1 = '/content/drive/My Drive/Data/Zomato Restaurant reviews.xlsx'
df_reviews = pd.read_excel(path1)
path2 = '/content/drive/My Drive/Data/Zomato Restaurant names and Metadata.xlsx'
df_metadata = pd.read_excel(path2)

### Dataset First View

# Dataset First Look
df_reviews.head()

df_metadata.head()

df_metadata.rename(columns={'Name': 'Restaurant'}, inplace=True)

df = pd.merge(df_reviews, df_metadata, on='Restaurant')

df.head()

### Dataset Rows & Columns count

# Dataset Rows & Columns count
df.shape

"""### Dataset Information"""

# Dataset Info
df.info()

#### Duplicate Values

# Dataset Duplicate Value Count
print("Duplicate values:", df.duplicated().sum())

#### Missing Values/Null Values

# Missing Values/Null Values Count
print("Missing values:", df.isnull().sum())

# Visualizing the missing values
sns.heatmap(df.isnull(), cbar=False)

# Dataset Columns
df.columns

# Dataset Describe
df.describe()

### Check Unique Values for each variable

# Check Unique Values for each variable.
for i in df.columns.tolist():
    print("No. of unique values in ", i, "is", df[i].nunique(), ".")

### Data Wrangling Code

# Convert object column to lower case
for col in ['Restaurant', 'Reviewer', 'Review', 'Collections', 'Cuisines']:
    df[col] = df[col].str.lower()

# Dropping the duplicate values
df.drop_duplicates(inplace=True)

# Dropping the missing values
df.dropna(subset=['Review'], inplace=True)

df['n_review'] = df['Metadata'].apply(lambda x: re.findall(r'\d+', x.split(',')[0])[0])
df['n_follow'] = df['Metadata'].apply(lambda x: re.findall(r'\d+', x.split(',')[1])[0] if len(x.split(',')) > 1 else 0)

df['Cuisines'] = df['Cuisines'].apply(lambda x: x.split(','))
df['Cuisines'] = df['Cuisines'].apply(lambda x: [i.strip() for i in x if i.strip() != 'nan'])
df['Cuisines'] = df['Cuisines'].apply(lambda x: sorted(x))

df['Collections'] = df['Collections'].apply(lambda x: str(x).split(','))
df['Collections'] = df['Collections'].apply(lambda x: [i.strip() for i in x if i.strip() != 'nan'])
df['Collections'] = df['Collections'].apply(lambda x: sorted(x))

df.drop(['Metadata', 'Timings', 'Time', 'Links', 'Reviewer'], axis=1, inplace=True)

df['Rating'] = np.where(df['Rating'] == 'Like', 3.5, df['Rating'])
df['Rating'] = df['Rating'].astype('float')
df['n_review'] = df['n_review'].astype('int')
df['n_follow'] = df['n_follow'].astype('int')

df.head()

# Number of reviewers for each restaurant - bar plot
top_10_restaurants = df.groupby('Restaurant')['n_review'].sum().sort_values(ascending=False).head(10).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(y='n_review', x='Restaurant', data=top_10_restaurants)
plt.title('Number of reviewers for each restaurant')
plt.xticks(rotation=90)
plt.show()

# Number of followers for each restaurant - barh plot
top_10_restaurants = df.groupby('Restaurant')['n_follow'].sum().sort_values(ascending=False).head(10).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(y='n_follow', x='Restaurant', data=top_10_restaurants)
plt.title('Number of followers for each restaurant')
plt.xticks(rotation=90)
plt.show()

# Mean rating for each restaurant
top_10_restaurants = df.groupby('Restaurant')['Rating'].mean().sort_values(ascending=False).head(10).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(y='Rating', x='Restaurant', data=top_10_restaurants)
plt.title('Mean rating for each restaurant')
plt.xticks(rotation=90)
plt.show()

# Top Cuisines
cuisines = {}
for i in df['Cuisines']:
    for j in i:
        if j in cuisines:
            cuisines[j] += 1
        else:
            cuisines[j] = 1
top_cuisines = dict(sorted(cuisines.items(), key=lambda x: x[1], reverse=True)[:5])

plt.figure(figsize=(10, 6))
sns.barplot(x=list(top_cuisines.keys()), y=list(top_cuisines.values()))
plt.title('Top 10 Cuisines')
plt.xticks(rotation=45)
plt.show()

# Top Collections
collections = {}
for i in df['Collections']:
    for j in i:
        if j in collections:
            collections[j] += 1
        else:
            collections[j] = 1
top_collections = dict(sorted(collections.items(), key=lambda x: x[1], reverse=True)[:5])

plt.figure(figsize=(10, 6))
sns.barplot(x=list(top_collections.keys()), y=list(top_collections.values()))
plt.title('Top 5 Collections')
plt.xticks(rotation=45)
plt.show()

# Correlation Matrix
plt.figure(figsize=(12, 8))
sns.heatmap(df[['Rating', 'n_review', 'n_follow', 'Pictures', 'Cost']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Scatter plot of Number of Followers vs Number of Reviews
plt.figure(figsize=(10, 6))
sns.scatterplot(x='n_follow', y='n_review', data=df)
plt.title('Number of Followers vs Number of Reviews')
plt.show()

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['Review']))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud)
plt.axis('off')
plt.title('Word Cloud of Reviews')
plt.show()

#### Data Preprocessing

df['Collections'] = df['Collections'].apply(lambda x: ', '.join(x))
df['Cuisines'] = df['Cuisines'].apply(lambda x: ', '.join(x))

df_cuisines = df['Cuisines'].str.get_dummies(', ')
df_collections = df['Collections'].str.get_dummies(', ')

df = pd.concat([df, df_cuisines, df_collections], axis=1)
df.drop(['Cuisines', 'Collections'], axis=1, inplace=True)

#### Text Preprocessing

nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = word_tokenize(text)
    text = [lemmatizer.lemmatize(word) for word in text if word not in stop_words]
    text = ' '.join(text)
    return text


df['Review'] = df['Review'].apply(clean_text)

tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df['Review'])
X = pd.DataFrame(X.toarray(), columns=tfidf.get_feature_names_out())

df = pd.concat([df, X], axis=1)

df.drop('Review', axis=1, inplace=True)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

df_features = df.copy()

#### Feature Scaling

scaler = MinMaxScaler()
df_features[['Rating', 'n_review', 'n_follow', 'Pictures', 'Cost']] = scaler.fit_transform(df_features[['Rating', 'n_review', 'n_follow', 'Pictures', 'Cost']])

X = df_features.drop(['Restaurant'], axis=1)

#### Elbow Method

inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=100)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()

### **K-Means**

kmeans = KMeans(n_clusters=6, random_state=100)
kmeans.fit(X)

df = df[['Restaurant', 'Rating', 'n_review', 'n_follow', 'Pictures', 'Cost']]
df['kmeans'] = kmeans.predict(X)

# Plotting number of reviews vs number of followers
plt.figure(figsize=(8, 6))
colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']

for cluster in df['kmeans'].unique():
    cluster_data = df[df['kmeans'] == cluster]
    plt.scatter(cluster_data['n_review'], cluster_data['n_follow'], color=colors[cluster], label=f'Cluster {cluster}')

plt.xlabel('Number of Reviews')
plt.ylabel('Number of Followers')
plt.title('KMeans Clustering of Restaurants')
plt.legend()
plt.grid(True)
plt.show()

# Plotting number of reviews vs rating
plt.figure(figsize=(8, 6))
colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']

for cluster in df['kmeans'].unique():
    cluster_data = df[df['kmeans'] == cluster]
    plt.scatter(cluster_data['n_review'], cluster_data['Rating'], color=colors[cluster], label=f'Cluster {cluster}')

plt.xlabel('Number of Reviews')
plt.ylabel('Number of Rating')
plt.title('KMeans Clustering of Restaurants')
plt.legend()
plt.grid(True)
plt.show()

### **DBSCAN**

dbscan = DBSCAN(eps=0.5, min_samples=10)
dbscan.fit(X)

df = df[['Restaurant', 'Rating', 'n_review', 'n_follow', 'Pictures', 'Cost']]
df['dbscan'] = dbscan.fit_predict(X)

# Plotting dbscan clustering
plt.figure(figsize=(8, 6))
colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']

for cluster in df['dbscan'].unique():
    cluster_data = df[df['dbscan'] == cluster]
    # remove outliers
    if cluster == -1:
        continue
    plt.scatter(cluster_data['n_review'], cluster_data['n_follow'], color=colors[cluster], label=f'Cluster {cluster}')

plt.xlabel('Number of Reviews')
plt.ylabel('Number of Followers')
plt.title('DBSCAN Clustering of Restaurants')
plt.legend()
plt.grid(True)
plt.show()
