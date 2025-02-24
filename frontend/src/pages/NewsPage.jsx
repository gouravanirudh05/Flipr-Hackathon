import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const NewsPage = () => {
  const [articles, setArticles] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/articles") // Flask API endpoint
      .then((response) => response.json())
      .then((data) => {
        setArticles(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching articles:", error);
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="text-center text-gray-600">Loading articles...</p>;
  }

  if (error) {
    return <p className="text-center text-red-500">Error loading articles.</p>;
  }

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <h1 className="text-3xl font-bold text-center mb-6">Latest News</h1>

      {Object.entries(articles).map(([category, categoryArticles]) => (
        <div key={category} className="mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">{category}</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {categoryArticles.length > 0 ? (
              categoryArticles.map((article, index) => (
                <div
                  key={index}
                  className="bg-white rounded-lg shadow-lg overflow-hidden transform transition duration-300 hover:scale-105 hover:shadow-lg hover:cursor-pointer"
                >
                  <Link to={`/article/${article._id}`}>
                    <img
                      src={article.image || "https://akm-img-a-in.tosshub.com/businesstoday/images/story/202501/677ca3a1294b4-air-india-flight-emergency-landing-074635764-16x9.png?size=948:533"}
                      alt={article.title}
                      className="w-full h-48 object-cover"
                    />
                    <div className="p-4">
                      <h2 className="text-xl font-semibold">{article.title}</h2>
                      <p className="text-gray-600">
                        {article.city}, {article.country}
                      </p>
                    </div>
                  </Link>
                </div>
              ))
            ) : (
              <p className="text-gray-600">No articles found.</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default NewsPage;
