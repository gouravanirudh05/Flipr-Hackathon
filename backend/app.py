from flask import Flask, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Set MongoDB URI from .env file
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Initialize PyMongo
mongo = PyMongo(app)

@app.route('/articles', methods=['GET'])
def get_articles():
    articles = list(mongo.db.articles.find({}, {"_id": 0}))  # Fetch all articles
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
