import pandas as pd

# Load the dataset
df = pd.read_csv('C:\Users\CYRUS DADY\Downloads\MiniStore-1.0.0\Fake-Product-Review-Detection-main\DatasetIntel.csv')

# Filter genuine reviews
genuine_reviews_df = df[df['label'] == 1]

# Save the genuine reviews to a new CSV file
genuine_reviews_df.to_csv('genuine_reviews.csv', index=False)
