import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import joblib

# Load the pickled file
model = joblib.load(r'C:\Users\CYRUS DADY\Downloads\MiniStore-1.0.0\Fake-Product-Review-Detection-main\vader_sentiment_analyzer.pkl')

# Load the genuine reviews dataset
genuine_reviews_df = pd.read_csv('C:\\Users\\CYRUS DADY\\Downloads\\MiniStore-1.0.0\\Fake-Product-Review-Detection-main\\genuine_reviews.csv')

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
def get_sentiment_distribution_for_category(category):
    category_reviews = genuine_reviews_df[genuine_reviews_df['category'] == category]['text_']
    sentiments = [predict_sentiment_vader(review) for review in category_reviews]
    sentiment_counts = pd.Series(sentiments).value_counts()
    return sentiment_counts

# Streamlit app function
def main():
    # Set the title and page configuration
    st.title("Sentiment Analysis for Genuine Reviews")

    # Display the DataFrame
    st.sidebar.title("Genuine Reviews Dataset")
    st.sidebar.write(genuine_reviews_df)

    # Allow users to select a category
    selected_category = st.sidebar.selectbox("Select a Category", genuine_reviews_df['category'].unique())

    # Perform sentiment analysis on the selected category using VADER
    sentiment_distribution = get_sentiment_distribution_for_category(selected_category)

    # Plot total sentiment distribution for the selected category using VADER
    st.write(f"Total Sentiment Distribution for {selected_category} Category (VADER Model):")
    fig, ax = plt.subplots()
    sentiment_distribution.plot(kind='bar', ax=ax)
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title(f'Total Sentiment Distribution for {selected_category} Category (VADER Model)')
    plt.xticks(rotation=0)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
