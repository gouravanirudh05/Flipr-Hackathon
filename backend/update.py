from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv
from bson import ObjectId
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from readability import Document
import time
from transformers import pipeline
import lxml
from newspaper import Article
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import shutil
from keybert import KeyBERT


chrome_driver_path = shutil.which("chromedriver")
# Configure Selenium options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Fix crashes in Docker/Linux
#options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")  # Spoof user-agent
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress logging
options.add_argument("--disable-webgl")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-gpu")

# Initialize WebDriver
service = Service(chrome_driver_path)

# Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(app)

# MongoDB Configuration from .env
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

def insert_articles(articles):
    mongo.db.articles.insert_many(articles)
    print("✅ Sample articles added to MongoDB")

# initialise the summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# extract the SEO tags 
keyword_extractor = pipeline("ner", model="dslim/bert-base-NER")  

#initialise the translator for English to Hindi
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
kw_model = KeyBERT()


def summarizefn(text):
    print("Original Length:", len(text))

    if len(text.split()) < 250:  # If the text is too short, return as-is
        print("Text too short for summarization.")
        return ""

    try:
        summary = summarizer(text, max_length=(250),
                                     min_length=(200),
                                     do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Summarization Error: {e}")
        return text  # Return original text if summarization fails


driver = webdriver.Chrome(service=service, options=options)


API_KEY =  os.getenv("PEXELS_API") 
BASE_URL = "https://api.pexels.com/v1/search"
def get_single_pexels_image(query):
    headers = {"Authorization": API_KEY}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}  # Fetch 1 landscape image
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["landscape"]  # Return landscape image URL
        else:
            return "No images found."
    else:
        print("Error:", response.status_code, response.text)
        return None


def extract_news_links(rss_url):
    response = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, "xml")  # Parse as XML

    links = []
    for item in soup.find_all("item"):
        if(item.find("source") and item.find("source").text.strip()=="Deccan Herald"):
          continue
        title = item.find("title").text.strip()
        link = item.find("link").text.strip()
        links.append({"title": title, "link": link})

    return links


def fetch_article_content(url):
    try:
        # Load website in Selenium
        driver.get(url)

        # Wait for the page to fully load
        time.sleep(2)  # Wait 2 seconds (adjust if needed)

        # Get fully loaded HTML source
        html_source = driver.page_source

        # Use newspaper3k with the fully loaded HTML
        article = Article(url)
        article.set_html(html_source)
        article.parse()

        return article.text if article.text else "No readable content found"

    except Exception as e:
        return f"Error fetching content: {e}"


def start_app():
    mongo.db.articles.delete_many({})
    l1 = ''
    l2 = ''
    print("Locations are required fields.")
    while l1 == '':
        l1 = input('Enter higher level location: ').lower()
    while l2 == '':
        l2 = input('Enter lower level location: ').lower()

    sp = input("Do you want to include sports(Y/N)? ")
    ec = input("Do you want to include economics(Y/N)? ")


    do_stuff("https://news.google.com/rss/search?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11&q=" + l1, [l1, 'l1'])
    do_stuff("https://news.google.com/rss/search?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11&q=" + l2, [l2, 'l2'])
    if sp.lower() == 'y':
        do_stuff('https://www.espncricinfo.com/rss/content/story/feeds/0.xml', ['', 'sp'])
    if ec.lower() == 'y':
        do_stuff('https://economictimes.indiatimes.com/rssfeedsdefault.cms', ['', 'ec'])


def do_stuff(news_link, tags):
    print('-'*100)
    print("Extracting news for ", tags[0]+tags[1])
    news_links = extract_news_links(news_link)
    lim = ''
    category = ''
    if tags[0] == '':
      if tags[1] == 'sp':
        lim = input("Enter the number of articles to be extracted for sports:")
        category = 'sports'
      elif tags[1] == 'ec':
        lim = input("Enter the number of articles to be extracted for economics:")
        category = 'economics'
    else :
        lim = input(f"Enter the number of articles to be extracted for {tags[0]}:")
        category = tags[1]
    
    lim = int(lim)
    i = 0
    articles = []

    for link in news_links:
        if i >= lim:
          break    
        content = fetch_article_content(link["link"])
        keywords = kw_model.extract_keywords(content)
        content = summarizefn(content)
        if content == "":
          continue
        new_article = translator(content, max_length=500)[0]["translation_text"]
        new_title = translator(link['title'], max_length=500)[0]["translation_text"]
        img_url=get_single_pexels_image(link["title"])

        articles.append({ 
            "title": link["title"],
            'title_translation': new_title,
            'link': link['link'],
            'keywords': keywords,
            'description': content,
            'translation': new_article,
            'date': datetime(datetime.today().year, datetime.today().month, datetime.today().day),
            'category': tags[1], 
            'location' : tags[0], 
            'img_url' : img_url
        })
        i = i + 1

    insert_articles(articles)
    print("Published articles for ", category)


start_app()
#close the browser
driver.close()