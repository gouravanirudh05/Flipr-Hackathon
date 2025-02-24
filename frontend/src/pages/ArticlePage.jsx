import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";

const ArticlePage = () => {
  const { id } = useParams(); // Get article index from URL
  const [article, setArticle] = useState(null);

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
    <div className="bg-gray-100 min-h-screen p-6">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6">
        <img
          src="https://akm-img-a-in.tosshub.com/businesstoday/images/story/202501/677ca3a1294b4-air-india-flight-emergency-landing-074635764-16x9.png?size=948:533"
          alt={article.title}
          className="w-full h-64 object-cover rounded-lg"
        />
        <h1 className="text-3xl font-bold mt-4">{article.title}</h1>
        <p className="text-gray-600">
          {article.city}, {article.country} - <strong>{article.date}</strong>
        </p>
        <p className="mt-4">{article.description}</p>
      </div>
    </div>
  );
};

export default ArticlePage;
