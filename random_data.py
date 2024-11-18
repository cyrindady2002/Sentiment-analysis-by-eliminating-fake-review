import pandas as pd
import plotly.express as px
import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['E-commerce']
collection = db['comments']

# Generate random timestamps for the comments
def generate_random_timestamp():
    start_date = datetime(2020, 1, 1)
    end_date = datetime.now()
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    random_hours = random.randrange(24)
    random_minutes = random.randrange(60)
    random_seconds = random.randrange(60)
    random_timestamp = start_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes, seconds=random_seconds)
    return random_timestamp

# Generate some random comments, ratings, and categories
comments = ["Great product!", "Not satisfied with the quality.", "Fast delivery.", "Excellent customer service."]
ratings = [5, 2, 4, 5]
categories = ["Electronics", "Clothing", "Home & Kitchen", "Books"]

# Insert data into MongoDB collection
for i in range(len(comments)):
    comment = {
        'text_': comments[i],
        'rating': ratings[i],
        'category': categories[i],
        'timestamp': generate_random_timestamp()  # Generate random timestamp
    }
    collection.insert_one(comment)

# Query MongoDB to retrieve comments
cursor = collection.find({})
data = [(comment['text_'], comment['rating'], comment['category'], comment['timestamp']) for comment in cursor]
comments, ratings, categories, timestamps = zip(*data)

# Create a DataFrame from comments, ratings, and categories
df = pd.DataFrame({'text_': comments, 'rating': ratings, 'category': categories, 'timestamp': timestamps})

# Now you can continue with the rest of your code
