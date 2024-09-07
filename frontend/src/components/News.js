import React, { useEffect, useState } from 'react';

const News = () => {
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetch('/get_news')
      .then(response => response.json())
      .then(data => setNews(data));
  }, []);

  return (
    <div>
      <h1>Latest News on Blood Sugar</h1>
      {news.length > 0 ? (
        <div>
          {news.map((article, index) => (
            <div key={index} className="article">
              <h2>{article.title}</h2>
              <p>{article.description}</p>
              <a href={article.url} target="_blank" rel="noopener noreferrer">Read more</a>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading news...</p>
      )}
    </div>
  );
};

export default News;