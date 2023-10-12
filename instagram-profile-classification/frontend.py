
import streamlit as st
import requests

# Define the API endpoint
api_endpoint = 'http://localhost:5000/get_category'  # Change this to your Flask server address

st.title('Instagram Page Category Finder')

# Input field for Instagram link
instagram_link = st.text_input('Enter Instagram Page Link', '')

if st.button('Find Category'):
    # Make a POST request to the Flask backend
    response = requests.post(api_endpoint, json={'instagram_link': instagram_link})

    if response.status_code == 200:
        data = response.json()
        st.success(f'Category: {data["category"]}')
    else:
        st.error('Error: Unable to fetch category.')
