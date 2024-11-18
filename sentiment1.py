import pandas as pd
from pymongo import MongoClient

# Load the dataset
client = MongoClient('mongodb://localhost:27017/')
db = client['E-commerce']
collection = db['comments']

# Retrieve comments, ratings, and categories from MongoDB
cursor = collection.find({})
data = [(comment['text_'], comment['rating'], comment['category']) for comment in cursor]
comments, ratings, categories = zip(*data)

# Create a DataFrame from comments, ratings, and categories
df = pd.DataFrame({'text_': comments, 'rating': ratings, 'category': categories})


# Filter genuine reviews
genuine_reviews_df = df[df['label'] == 1]

# Save the genuine reviews to a new CSV file
genuine_reviews_df.to_csv('genuine_reviews1.csv', index=False)
