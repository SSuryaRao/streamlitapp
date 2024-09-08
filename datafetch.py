from pymongo import MongoClient

# MongoDB Atlas connection string (replace with your credentials)
MONGO_URI = 'mongodb+srv://surya:mongo1234@cluster0.686u6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client['news_db']
collection = db['google_news_articles']

# Function to fetch all documents
def fetch_data():
    try:
        documents = collection.find()
        for document in documents:
            print(document)
    except Exception as e:
        print(f"An error occurred: {e}")

# Fetch and print data
fetch_data()

# Optional: Close the connection
client.close()
