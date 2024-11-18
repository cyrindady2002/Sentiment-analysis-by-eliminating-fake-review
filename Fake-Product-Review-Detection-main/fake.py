import streamlit as st
import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import plotly.graph_objs as go

# Load the dataset
df = pd.read_csv('DatasetIntel.csv')

# Handle missing values in the label column and convert to int
df['label'] = df['label'].fillna(0)
df['label'] = df['label'].astype(int)

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
def predict_authenticity(review_index):
    # Retrieve the review text using the index
    review = df.loc[review_index, 'text_']

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

    # Create a slider for selecting review index
    review_index = st.slider("Select Review Index", 0, len(df) - 1, 1)

    # Call the predict_authenticity function and unpack the outputs
    review, authenticity_label, pie_chart = predict_authenticity(review_index)

    # Display the review text, predicted authenticity label, and pie chart
    st.write("Review:", review)
    st.write("Predicted Authenticity:", authenticity_label)
    st.plotly_chart(pie_chart)

if __name__ == "__main__":
    main()

