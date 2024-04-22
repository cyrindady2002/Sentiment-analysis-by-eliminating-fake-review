import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px
from pymongo import MongoClient

def get_sentiment(sentiment_score):
    if sentiment_score > 0.2:
        return 'Positive'
    elif sentiment_score < -0.2:
        return 'Negative'
    else:
        return 'Neutral'

def detect_fake_review(sentiment_label):
    if sentiment_label == 'Negative':
        return True
    else:
        return False

def main():
    st.title('Reviews Sentiment Analysis Dashboard')

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['E-commerce']  # Replace 'your_database_name' with your actual database name
    collection = db['comments']  # Replace 'your_collection_name' with your actual collection name

    # Retrieve data from MongoDB collection
    cursor = collection.find({})

    # Convert MongoDB cursor to DataFrame
    df = pd.DataFrame(list(cursor))

    # Rename columns for consistency
    df.rename(columns={'_id': 'ID', 'name': 'Name', 'email': 'Email', '__v': 'V', 'category': 'Product Name', 'text_': 'Body', 'rating':'Rating'}, inplace=True)

    # Perform sentiment analysis
    df['Sentiment'] = df['Body'].apply(lambda x: get_sentiment(TextBlob(str(x)).sentiment.polarity))

    # Detect fake reviews
    df['Fake Review'] = df['Sentiment'].apply(lambda x: detect_fake_review(x))

    # Display overall sentiment distribution
    st.subheader('Overall Sentiment Distribution')
    sentiment_counts = df['Sentiment'].value_counts()
    st.bar_chart(sentiment_counts)

    # Display distribution of fake and real reviews
    st.subheader('Distribution of Fake and Real Reviews')
    fake_review_count = df['Fake Review'].sum()
    real_review_count = len(df) - fake_review_count
    st.write("Fake Reviews:", fake_review_count)
    st.write("Real Reviews:", real_review_count)

    # Display pie chart
    st.subheader('Pie chart:')
    chart_data = pd.DataFrame({'Review Type': ['Fake', 'Real'], 'Count': [fake_review_count, real_review_count]})
    fig = px.pie(chart_data, names='Review Type', values='Count', hole=0.3)
    st.plotly_chart(fig)

    # Display product name selection dropdown
    product_names = df['Product Name'].unique()
    selected_product = st.selectbox('Select a Product Name', product_names)

    # Filter dataframe based on selected product
    selected_product_df = df[df['Product Name'] == selected_product]

    # Display sentiment distribution for the selected product
    st.subheader(f'Sentiment Distribution for {selected_product}')
    sentiment_counts_selected = selected_product_df['Sentiment'].value_counts()
    st.bar_chart(sentiment_counts_selected)

    # Display individual reviews for the selected product
    st.subheader(f'Individual Reviews for {selected_product}')
    st.dataframe(selected_product_df)

if __name__ == "__main__":
    main()
