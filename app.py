from flask import Flask, render_template, request
from search import search_blogs

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = None

    if request.method == "POST":
        query = request.form.get("query")
        blogs = search_blogs(query)

        # Group blogs by level
        grouped = {
            "beginner": [],
            "intermediate": [],
            "advanced": []
        }

        for blog in blogs:
            level = blog.get("level", "intermediate")
            grouped[level].append(blog)

        results = grouped

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
