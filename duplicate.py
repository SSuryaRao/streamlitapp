from pymongo import MongoClient

# MongoDB Atlas connection string (replace with your credentials)
MONGO_URI = 'mongodb+srv://surya:mongo1234@cluster0.686u6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client['news_db']
collection = db['google_news_articles']

def remove_duplicates():
    try:
        # Create an index on the field that you want to use to identify duplicates
        collection.create_index([('title', 1)], unique=False)
        
        # Aggregate documents to identify duplicates
        pipeline = [
            {
                '$group': {
                    '_id': '$title',
                    'count': {'$sum': 1},
                    'docs': {'$push': '$_id'}
                }
            },
            {
                '$match': {
                    'count': {'$gt': 1}
                }
            }
        ]
        
        duplicates = list(collection.aggregate(pipeline))
        
        # Loop through duplicates and remove all but the first document for each duplicate group
        for duplicate in duplicates:
            # Get all document IDs in this duplicate group, except the first one
            ids_to_remove = duplicate['docs'][1:]
            
            # Remove duplicates
            result = collection.delete_many({'_id': {'$in': ids_to_remove}})
            print(f"Removed {result.deleted_count} duplicate documents with title '{duplicate['_id']}'")

    except Exception as e:
        print(f"An error occurred while removing duplicates: {e}")

# Call the function to remove duplicates
remove_duplicates()

# Optional: Close the connection
client.close()
