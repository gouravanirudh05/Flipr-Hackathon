from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
from bson import ObjectId
import os
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(app)

# MongoDB Configuration from .env
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

def serialize_article(article):
    """Converts MongoDB ObjectId to a string and formats the date."""
    article["_id"] = str(article["_id"])  # Convert ObjectId to string
    if "date" in article:
        article["date"] = article["date"].strftime("%Y-%m-%d")  # Format date
    return article

@app.route('/articles', methods=['GET'])
def get_articles():
    articles = mongo.db.articles.find()
    
    categorized_articles = {
        "State News": [],
        "Local News": [],
        "Sports News": [],
        "Economic News": []
    }

    for article in articles:
        article["_id"] = str(article["_id"])  # Convert ObjectId to string
        category = article.get("category", "").lower()

        if category == "l1":
            categorized_articles["State News"].append(article)
        elif category == "l2":
            categorized_articles["Local News"].append(article)
        elif category == "sp":
            categorized_articles["Sports News"].append(article)
        elif category == "ec":
            categorized_articles["Economic News"].append(article)

    return jsonify(categorized_articles)


@app.route('/article/<oid>', methods=['GET'])
def get_article_by_id(oid):
    """Fetch a single article by its ObjectId."""
    try:
        article = mongo.db.articles.find_one({"_id": ObjectId(oid)})
        if not article:
            return jsonify({"error": "Article not found"}), 404
        
        return jsonify(serialize_article(article))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
