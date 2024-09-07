import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Upload = () => {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [image3, setImage3] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    const userId = localStorage.getItem('user_id');

    formData.append('user_id', userId);
    formData.append('images', [image1, image2, image3]);

    fetch('/upload_images', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        if (data.recipe_id) {
          navigate(`/results/${data.recipe_id}`);
        } else {
          alert('Failed to recognize ingredients. Please try again.');
        }
      });
  };

  return (
    <div>
      <h1>Upload Images</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={(e) => setImage1(e.target.files[0])} required />
        <input type="file" onChange={(e) => setImage2(e.target.files[0])} required />
        <input type="file" onChange={(e) => setImage3(e.target.files[0])} required />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
};

export default Upload;
