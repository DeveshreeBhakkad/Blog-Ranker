from sentence_transformers import SentenceTransformer, util
from urllib.parse import urlparse

# Load AI model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Domain popularity scores (editable anytime)
DOMAIN_SCORES = {
    "medium.com": 0.9,
    "towardsdatascience.com": 0.85,
    "geeksforgeeks.org": 0.8,
    "wikipedia.org": 0.95
}

def get_domain_score(url):
    domain = urlparse(url).netloc.replace("www.", "")
    return DOMAIN_SCORES.get(domain, 0.4)  # default score

def rank_blogs(query, blogs):
    query_embedding = model.encode(query, convert_to_tensor=True)
    ranked_results = []

    for blog in blogs:
        content_embedding = model.encode(blog["snippet"], convert_to_tensor=True)
        relevance = util.cos_sim(query_embedding, content_embedding).item()

        popularity = get_domain_score(blog["link"])

        final_score = (0.7 * relevance) + (0.3 * popularity)

        ranked_results.append({
            "title": blog["title"],
            "link": blog["link"],
            "snippet": blog["snippet"],
            "relevance": round(relevance, 3),
            "popularity": popularity,
            "final_score": round(final_score, 3)
        })

    ranked_results.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked_results
