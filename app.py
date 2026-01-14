from flask import Flask, render_template, request
from blog_data import blogs
from recommender import rank_blogs

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = None

    if request.method == "POST":
        query = request.form.get("query")
        results = rank_blogs(query, blogs)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

