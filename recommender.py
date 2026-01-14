import os
import requests
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

model = SentenceTransformer("all-MiniLM-L6-v2")


def fetch_blogs_from_web(query):
    params = {
        "engine": "google",
        "q": query + " blog",
        "api_key": SERPAPI_KEY,
        "num": 10
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    blogs = []

    for result in data.get("organic_results", []):
        blogs.append({
            "title": result.get("title"),
            "content": result.get("snippet", ""),
            "link": result.get("link")
        })

    return blogs


def rank_blogs(query, blogs):
    query_embedding = model.encode(query, convert_to_tensor=True)

    ranked = []

    for blog in blogs:
        blog_embedding = model.encode(blog["content"], convert_to_tensor=True)
        score = util.cos_sim(query_embedding, blog_embedding).item()

        ranked.append({
            "title": blog["title"],
            "description": blog["content"],
            "link": blog["link"],
            "score": round(score, 3)
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked
