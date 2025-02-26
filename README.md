# AI News Aggregator
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

## About The Project

AI News Aggregator is a **Flask-based web application** designed to fetch and display the latest news articles from various sources. The system periodically scrapes news using a **Google Colab Notebook** and stores the articles in a **MongoDB database**. The frontend is built with **React.js**, providing a clean and intuitive interface for users to browse recent news updates.

### Key Features:
- **Automated News Scraping**: Fetches recent articles from multiple sources.
- **Database Storage**: Stores scraped news in MongoDB for easy retrieval.
- **Flask API**: Serves the stored news articles to the frontend.
- **React Frontend**: Displays news articles in an organized format.

## Built With

### **Frontend**
- **React.js**: User-friendly interface for browsing news articles.
- **CSS & TailwindCSS**: Modern styling for a responsive UI.

### **Backend**
- **Flask**: Serves the news articles via RESTful APIs.
- **MongoDB**: Stores scraped news for persistent access.
- **Google Colab**: Runs the web scraper for fetching news articles.

## Getting Started

### Prerequisites
Ensure you have the following installed:
- **Node.js & npm** for the frontend
- **Python & pip** for the backend
- **MongoDB** for database storage

### Installation

#### Clone the Repository:
```sh
   git clone 
   cd Flipr
```

#### Install Backend Dependencies:
```sh
   cd backend
   pip install -r requirements.txt
   python app.py 
```

#### Install Frontend Dependencies:
```sh
   cd ../frontend
   npm install
   npm start  # Start React app
```
#### Run the scraper on the google collab notebook below from where the articles will be put to DB
```sh
https://colab.research.google.com/drive/1YXB4nOwx8SxMLyanc7Ph4rfXsxwEZ6tX?usp=sharing
```
## Usage

1. **Run the Web Scraper**: Execute the **Google Colab Notebook** to scrape and store recent news in MongoDB.
2. **Start the Backend**: Flask serves the stored articles via API.
3. **Launch the Frontend**: React frontend displays the latest news articles.

## Deployment Guidelines

1. **Host the backend**: Deploy the Flask server on AWS/GCP/Azure/Render.
2. **Host the frontend**: Deploy the React app using Vercel or Netlify.
3. **Database**: Use MongoDB Atlas (free-tier recommended).
4. **Run Scraper**: Periodically execute the Google Colab Notebook for fresh news.

## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

[contributors-shield]: https://img.shields.io/github/contributors/gouravanirudh05/Flipr-Hackathon?style=for-the-badge
[contributors-url]: https://github.com/gouravanirudh05/Flipr-Hackathon/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/gouravanirudh05/Flipr-Hackathon.svg?style=for-the-badge
[forks-url]: https://github.com/gouravanirudh05/Flipr-Hackathon/network/members
[stars-shield]: https://img.shields.io/github/stars/gouravanirudh05/Flipr-Hackathon.svg?style=for-the-badge
[stars-url]: https://github.com/gouravanirudh05/Flipr-Hackathon/stargazers
[issues-shield]: https://img.shields.io/github/issues/gouravanirudh05/Flipr-Hackathon.svg?style=for-the-badge
[issues-url]: https://github.com/gouravanirudh05/Flipr-Hackathon/issues
[license-shield]: https://img.shields.io/github/license/gouravanirudh05/Flipr-Hackathon.svg?style=for-the-badge
[license-url]: https://github.com/gouravanirudh05/Flipr-Hackathon/blob/master/LICENSE.txt

