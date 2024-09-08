import requests
from pymongo import MongoClient

# MongoDB Atlas connection string (replace <username>, <password>, <cluster> with your own credentials)
MONGO_URI = 'mongodb+srv://surya:mongo1234@cluster0.686u6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)

# Select the database and collection in MongoDB
db = client['news_db']  # Database name
collection = db['google_news_articles']  # Collection name

# SerpApi parameters
API_KEY = '4f2e701f069c18eb50de29437aab7f3cd83eda48f88c017f2845d692df40d120'  # Replace with your actual SerpApi key
params = {
    'q': 'flood',  # Search query (e.g., disaster-related news)
    'tbm': 'nws',     # Google News search
    'api_key': API_KEY
}

url = 'https://serpapi.com/search.json'

# Make the request to SerpApi
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    news_articles = data.get('news_results', [])  # Get the news results
    
    # Loop through the articles and insert them into MongoDB
    for article in news_articles:
        try:
            # Prepare the document for MongoDB
            document = {
                'title': article['title'],  # Title of the article
                'link': article['link'],    # Link to the article
                'source': article.get('source', ''),  # News source (if available)
                'date': article.get('date', ''),  # Publication date (if available)
                'snippet': article.get('snippet', ''),  # Snippet/summary of the article
                'thumbnail': article.get('thumbnail', ''),  # Thumbnail image URL (if available)
            }
            
            # Insert the document into MongoDB
            result = collection.insert_one(document)
            print(f"Inserted article with ID: {result.inserted_id}")
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
else:
    print(f"Failed to fetch Google News. Status code: {response.status_code}")
