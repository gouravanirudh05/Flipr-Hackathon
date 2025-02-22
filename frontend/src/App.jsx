import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NewsPage from "./pages/NewsPage";
import ArticlePage from "./pages/ArticlePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<NewsPage />} />
        <Route path="/article/:id" element={<ArticlePage />} />
      </Routes>
    </Router>
  );
}

export default App;
