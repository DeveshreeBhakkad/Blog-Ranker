from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_blogs(query, blogs):
    query_embedding = model.encode(query, convert_to_tensor=True)

    ranked_results = []

    for blog in blogs:
        blog_embedding = model.encode(blog["content"], convert_to_tensor=True)
        score = util.cos_sim(query_embedding, blog_embedding).item()

        ranked_results.append({
            "title": blog["title"],
            "score": round(score, 3)
        })

    ranked_results.sort(key=lambda x: x["score"], reverse=True)
    return ranked_results
