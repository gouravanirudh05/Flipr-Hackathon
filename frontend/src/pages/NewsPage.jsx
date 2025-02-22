import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
const NewsPage = () => {
  const [articles, setArticles] = useState([]);
  const [filteredArticles, setFilteredArticles] = useState([]);
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [level, setLevel] = useState("");
  const [category, setCategory] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://127.0.0.1:5000/articles") // Replace with your actual Flask API URL
      .then((response) => response.json())
      .then((data) => {
        setArticles(data);
        setFilteredArticles(data); // Default to all articles
      })
      .catch((error) => console.error("Error fetching articles:", error));
  }, []);

  // Function to filter articles
  const filterArticles = () => {
    let filtered = articles;

    if (city)
      filtered = filtered.filter(
        (article) => article.city.toLowerCase() === city.toLowerCase()
      );
    if (country)
      filtered = filtered.filter(
        (article) => article.country.toLowerCase() === country.toLowerCase()
      );
    if (level)
      filtered = filtered.filter(
        (article) => article.level.toLowerCase() === level.toLowerCase()
      );
    if (category)
      filtered = filtered.filter(
        (article) => article.category.toLowerCase() === category.toLowerCase()
      );

    setFilteredArticles(filtered);
  };

  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <h1 className="text-3xl font-bold text-center mb-6">Latest News</h1>

      {/* Filter Options */}
      <div className="flex flex-wrap gap-4 justify-center mb-6">
        <input
          type="text"
          placeholder="Enter City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="text"
          placeholder="Enter Country"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          className="p-2 border border-gray-300 rounded"
        />
        <select
          value={level}
          onChange={(e) => setLevel(e.target.value)}
          className="p-2 border border-gray-300 rounded"
        >
          <option value="">Select Level</option>
          <option value="local">Local</option>
          <option value="national">National</option>
          <option value="global">Global</option>
        </select>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="p-2 border border-gray-300 rounded"
        >
          <option value="">Select Category</option>
          <option value="politics">Politics</option>
          <option value="sports">Sports</option>
          <option value="technology">Technology</option>
        </select>
        <button
          onClick={filterArticles}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Filter
        </button>
      </div>

      {/* Display Articles */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
        {filteredArticles.length > 0 ? (
          filteredArticles.map((article, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-lg overflow-hidden transform transition duration-300 hover:scale-105 hover:shadow-lg hover:cursor-pointer"
            >
              <Link to={`/article/${article._id.$oid}`}>
                <img
                  src={article.image} // Dynamic category-based images
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
          <p className="text-center text-gray-600">No articles found.</p>
        )}
      </div>
    </div>
  );
};

export default NewsPage;
