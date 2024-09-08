import requests

API_KEY = '4f2e701f069c18eb50de29437aab7f3cd83eda48f88c017f2845d692df40d120'
params = {
    'q': 'disaster',  # Search query
    'tbm': 'nws',     # Google News
    'api_key': API_KEY
}

url = 'https://serpapi.com/search.json'

response = requests.get(url, params=params)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    news_articles = data['news_results']
    
    # Loop through news articles and print titles
    for article in news_articles:
        print(article['title'])
else:
    print(f"Failed to fetch Google News. Status code: {response.status_code}")
