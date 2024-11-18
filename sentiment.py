import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import joblib
import pymongo
import webbrowser

# Load the pickled file
model = joblib.load(r'C:\Users\CYRUS DADY\Downloads\MiniStore-1.0.0\Fake-Product-Review-Detection-main\vader_sentiment_analyzer.pkl')

# Connect to MongoDB and select the collection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["E-commerce"]  # Change "your_database_name" to your actual database name
collection = db["genuine"]  # Change "your_collection_name" to your actual collection name

# Function to fetch data from MongoDB
def fetch_data():
    data = collection.find({})  # Retrieve all documents in the collection
    return pd.DataFrame(list(data))

# Load sentiment analysis model (VADER)
sia = SentimentIntensityAnalyzer()

# Define the predict_sentiment function using VADER
def predict_sentiment_vader(review):
    scores = sia.polarity_scores(review)
    compound_score = scores['compound']
    
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function to get sentiment distribution using VADER for a specific category
def get_sentiment_distribution_for_category(category_reviews):
    sentiments = [predict_sentiment_vader(review) for review in category_reviews]
    sentiment_counts = pd.Series(sentiments).value_counts()
    return sentiment_counts

# Streamlit app function
def main():
    # Set the title and page configuration
    st.title("Sentiment Analysis for Genuine Reviews")

    # Fetch data from MongoDB
    data = fetch_data()

    # Display the DataFrame
    st.sidebar.title("Genuine Reviews Dataset")
    st.sidebar.write(data)

    # Allow users to select a category
    selected_category = st.sidebar.selectbox("Select a Category", data['category'].unique())

    # Filter data for the selected category
    category_reviews = data[data['category'] == selected_category]['text_']

    # Perform sentiment analysis on the selected category using VADER
    sentiment_distribution = get_sentiment_distribution_for_category(category_reviews)

    # Plot total sentiment distribution for the selected category using VADER
    st.write(f"Total Sentiment Distribution for {selected_category}")
    fig, ax = plt.subplots()
    sentiment_distribution.plot(kind='bar', ax=ax)
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title(f'Total Sentiment Distribution for {selected_category}  ')
    plt.xticks(rotation=0)
    st.pyplot(fig)

    # Add a button for trend analysis
    if st.button("Trend Analysis"):
       # Open the URL in a new tab
       webbrowser.open_new_tab("http://localhost:8503/")
if __name__ == "__main__":
    main()