import streamlit as st
from pymongo import MongoClient
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# MongoDB Atlas connection string (replace <username>, <password>, <cluster> with your own credentials)
MONGO_URI = 'mongodb+srv://surya:mongo1234@cluster0.686u6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client['news_db']
collection = db['google_news_articles']

def fetch_data():
    try:
        # Fetch all documents from the collection
        documents = list(collection.find())
        return documents
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return []

def display_data(documents):
    if documents:
        # Convert documents to a DataFrame for easier manipulation
        df = pd.DataFrame(documents)

        # Display the DataFrame
        st.write("### News Articles")
        st.dataframe(df)

        # Display articles and images
        st.write("### Articles")
        for _, row in df.iterrows():
            st.write(f"**Title:** {row['title']}")
            st.write(f"**Link:** [Read more]({row['link']})")
            st.write(f"**Source:** {row['source']}")
            st.write(f"**Date:** {row['date']}")
            st.write(f"**Snippet:** {row['snippet']}")

            # Display the image
            if 'thumbnail' in row and row['thumbnail']:
                try:
                    response = requests.get(row['thumbnail'])
                    img = Image.open(BytesIO(response.content))
                    st.image(img, caption=row['title'])
                except Exception as e:
                    st.warning(f"Could not load image for article: {row['title']}. Error: {e}")
            st.write("---")

def main():
    st.title("Google News Articles from MongoDB Atlas")

    documents = fetch_data()
    display_data(documents)

if __name__ == "__main__":
    main()
