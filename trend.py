import pandas as pd
import plotly.express as px
import streamlit as st

# Load the dataset
df = pd.read_csv('DatasetIntel.csv')

# Replace 'time' with the actual column name containing timestamps in your dataset
timestamp_column = 'random_timestamp'

# Convert the timestamp column to datetime
df[timestamp_column] = pd.to_datetime(df[timestamp_column])

# Extract year and month from the timestamp column
df['year_month'] = df[timestamp_column].dt.to_period('M').astype(str)

# Add a placeholder product column since your dataset has only one product
df['product'] = 'Product 1'

# Group by product and year-month and count the number of reviews
product_monthly_reviews = df.groupby(['product', 'year_month']).size().reset_index(name='count')

# Create a dropdown to select the product
selected_product = st.selectbox("Select Product", ['Product 1'])

# Filter the data for the selected product (although there is only one product)
selected_product_reviews = product_monthly_reviews[product_monthly_reviews['product'] == selected_product]

# Create an animated line chart for the selected product
fig = px.line(selected_product_reviews, x='year_month', y='count', title=f'Monthly Review Trend for {selected_product}',
              animation_frame='year_month', range_y=[0, selected_product_reviews['count'].max() + 10],
              color_discrete_sequence=['blue'], render_mode='svg')

# Add labels and customizations
fig.update_layout(
    xaxis_title='Year-Month',
    yaxis_title='Number of Reviews',
    margin=dict(l=50, r=50, t=50, b=50),
    height=500,
    xaxis=dict(type='category', categoryorder='category ascending')
)

# Display the animated chart
st.plotly_chart(fig)