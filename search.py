import requests

# ⚠️ IMPORTANT:
# Replace this with YOUR SerpAPI key
SERP_API_KEY = "6a96700ac1a9b74eea0defb4bff3fb4f1a297e931e6f42fd30a24e9fb282f268"

def search_blogs(query):
    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google",
        "q": query + " blog",
        "api_key": SERP_API_KEY,
        "num": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    blogs = []

    for result in data.get("organic_results", []):
        blogs.append({
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet", "")
        })

    return blogs
