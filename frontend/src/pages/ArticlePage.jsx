import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";

const ArticlePage = () => {
  const { id } = useParams(); // Get article index from URL
  const [article, setArticle] = useState(null);
  const [showTranslation, setShowTranslation] = useState(false);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/article/${id}`)
      .then((response) => response.json())
      .then((data) => {
        setArticle(data);
      })
      .catch((error) => console.error("Error fetching article:", error));
  }, [id]);

  if (!article) return <p className="text-center text-gray-600">Loading...</p>;

  return (
    <div className="bg-gray-100 min-h-screen p-6 relative">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6">
        <button
          className="absolute top-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
          onClick={() => setShowTranslation(!showTranslation)}
        >
          {showTranslation ? "Show Original" : "Translate"}
        </button>
        <img
          src={article.img_url || "https://akm-img-a-in.tosshub.com/businesstoday/images/story/202501/677ca3a1294b4-air-india-flight-emergency-landing-074635764-16x9.png?size=948:533"}
          alt={article.title}
          className="w-2/3 h-74 object-cover rounded-lg mx-auto"
        />
        <h1 className="text-3xl font-bold mt-8 align-middle">{showTranslation ? article.title_translation || "Translation not available" : article.title}</h1>
        <p className="text-gray-600">
          {article.city}, {article.country} - <strong>{article.date}</strong>
        </p>

        <p className="mt-4">
          {showTranslation ? article.translation || "Translation not available" : article.description}
        </p>
      </div>
    </div>
  );
};

export default ArticlePage;
