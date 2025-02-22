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

def insert_articles():
    # Sample Articles
    sample_articles = [
        {
            "title": "Local Cricket Tournament in Bengaluru",
            "description": "A thrilling cricket match was played...",
            "image": "https://daijiworld.ap-south-1.linodeobjects.com/Linode/images3/mini_20022025_2.jpg",
            "date": datetime(2025, 2, 22),
            "category": "sports",
            "level": "local",
            "city": "Bengaluru",
            "country": "India"
        },
        {
            "title": "Global Climate Summit 2025",
            "description": "World leaders gathered to discuss climate change...",
            "image": "https://daijiworld.ap-south-1.linodeobjects.com/Linode/images3/mini_20022025_2.jpg",
            "date": datetime(2025, 3, 1),
            "category": "politics",
            "level": "global",
            "city": "New York",
            "country": "USA"
        },
        {
            "title": "Tech Startup Raises $10M Funding",
            "description": "A Bengaluru-based AI startup secured Series A funding...",
            "image": "https://daijiworld.ap-south-1.linodeobjects.com/Linode/images3/mini_20022025_2.jpg",
            "date": datetime(2025, 2, 20),
            "category": "technology",
            "level": "local",
            "city": "Bengaluru",
            "country": "India"
        }
    ]

    # Insert sample articles if the collection is empty
    if mongo.db.articles.count_documents({}) == 0:
        mongo.db.articles.insert_many(sample_articles)
        print("✅ Sample articles added to MongoDB")

# insert_articles()

def serialize_article(article):
    """Converts MongoDB ObjectId to a string and formats the date."""
    article["_id"] = str(article["_id"])  # Convert ObjectId to string
    if "date" in article:
        article["date"] = article["date"].strftime("%Y-%m-%d")  # Format date
    return article

@app.route('/articles', methods=['GET'])
def get_articles():
    """Fetch all articles from MongoDB."""
    articles = list(mongo.db.articles.find({}))  # Exclude MongoDB _id field
    return jsonify(articles)

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
