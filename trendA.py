import pandas as pd
import plotly.express as px
import streamlit as st
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['E-commerce']
collection = db['comments']

# Retrieve comments, ratings, and categories from MongoDB
cursor = collection.find({})
data = [(comment.get('text_', ''), comment.get('rating', 0), comment.get('category', ''), comment.get('timestamp', None)) for comment in cursor]
comments, ratings, categories, timestamps = zip(*data)

# Create a DataFrame from comments, ratings, and categories
df = pd.DataFrame({'text_': comments, 'rating': ratings, 'category': categories, 'timestamp': timestamps})

# Ensure timestamp column is not None and convert it to datetime
df = df[df['timestamp'].notnull()]
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract year, month, and category from the timestamp column
df['year_month'] = df['timestamp'].dt.to_period('M').astype(str)

# Group by year-month and category, calculate the average rating
category_monthly_avg_rating = df.groupby(['category', 'year_month']).agg({'rating': 'mean'}).reset_index()

# Create a dropdown to select the category
selected_category = st.selectbox("Select Category", df['category'].unique())

# Filter the data for the selected category
selected_category_reviews = category_monthly_avg_rating[category_monthly_avg_rating['category'] == selected_category]

# Create a line chart for the selected category
fig = px.line(selected_category_reviews, x='year_month', y='rating', title=f'Monthly Average Rating Trend for {selected_category}',
              color_discrete_sequence=['blue'])

# Add labels and customizations
fig.update_layout(
    xaxis_title='Year-Month',
    yaxis_title='Average Rating',
    margin=dict(l=50, r=50, t=50, b=50),
    height=500,
    xaxis=dict(type='category', categoryorder='category ascending')
)

# Display the chart
st.plotly_chart(fig)
