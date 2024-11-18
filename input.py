import streamlit as st
import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import plotly.graph_objs as go
from pymongo import MongoClient
import webbrowser
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['E-commerce']
collection = db['comments']
genuine_collection = db['genuine']  # Collection to store genuine reviews

# Retrieve comments, ratings, and categories from MongoDB
cursor = collection.find({})
data = [(comment['text_'], comment['rating'], comment['category'], comment['timestamp']) for comment in cursor]
comments, ratings, categories, timestamps = zip(*data)

# Create a DataFrame from comments, ratings, categories, and timestamps
df = pd.DataFrame({'text_': comments, 'rating': ratings, 'category': categories, 'timestamp': timestamps})

# Fake label generation
# Since we're not using the label column from the CSV, generate fake labels for demonstration
import random
df['label'] = [random.randint(0, 1) for _ in range(len(df))]

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(df['text_'], df['label'], test_size=0.25)

# Vectorize the text data
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Create an SVM classifier
classifier = SVC()
classifier.fit(X_train, y_train)

# Define the predict_authenticity function
def predict_authenticity(review):
    # Convert the review to a vector of features
    review_vector = vectorizer.transform([review])

    # Make a prediction using the SVM classifier
    prediction = classifier.predict(review_vector)

    # Determine the authenticity label
    authenticity_label = "Genuine Review" if prediction[0] == 1 else "Fake Review"

    # Calculate the distribution of fake and genuine reviews
    fake_reviews = (df['label'] == 0).sum()
    genuine_reviews = (df['label'] == 1).sum()

    # Create a pie chart to display the distribution
    pie_chart = go.Figure(data=[go.Pie(labels=['Fake', 'Genuine'], values=[fake_reviews, genuine_reviews])])

    # Return the review text, predicted authenticity label, authenticity HTML, and pie chart
    return review, authenticity_label, pie_chart

def main():
    # Set the title and page configuration
    st.title("Review Authenticity Dashboard")
    st.markdown(
        """
        <style>
            .fullScreenFrame {
                background-color: #1a1a2e;
                color: white;
                font-family: 'Arial', sans-serif;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display the DataFrame
    st.write("Dataset:", df)

    # Allow users to select fake or genuine reviews
    authenticity_options = st.sidebar.radio("Select Review Type", ["All", "Fake", "Genuine"])

    # Allow users to select category
    selected_category = st.sidebar.selectbox("Select Category", df['category'].unique())

    # Filter the dataset based on user selections
    filtered_df = df.copy()  # Make a copy to avoid modifying the original DataFrame
    if authenticity_options == "Fake":
        filtered_df = filtered_df[filtered_df['label'] == 0]
    elif authenticity_options == "Genuine":
        filtered_df = filtered_df[filtered_df['label'] == 1]
    if selected_category:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    # Display the filtered DataFrame
    st.write("Filtered Dataset:", filtered_df)

    # Create a slider for selecting review index
    review_index = st.slider("Select Review Index", 0, len(filtered_df) - 1, 1)

    # Call the predict_authenticity function and unpack the outputs
    review, authenticity_label, pie_chart = predict_authenticity(filtered_df.iloc[review_index]['text_'])

    # Display the review text, predicted authenticity label, and pie chart
    st.write("Review:", review)
    st.write("Predicted Authenticity:", authenticity_label)
    st.plotly_chart(pie_chart)

    # Add a button for sentiment analysis
if st.button("Sentiment Analysis"):
    # Open the URL in a new tab
    webbrowser.open_new_tab("http://localhost:8502/")

    # Store all genuine reviews in the "genuine" collection
    genuine_reviews_data = df[df['label'] == 1].to_dict(orient='records')
    for review_data in genuine_reviews_data:
        review_data['timestamp'] = datetime.now()
        genuine_collection.insert_one(review_data)
    st.success("All genuine reviews stored successfully!")


if __name__ == "__main__":
    main()
