import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ImageUpload = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const navigate = useNavigate();

  const handleImageChange = (e) => {
    setSelectedImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedImage) return;

    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post('/api/recognize-ingredients/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.ingredients) {
        navigate('/ingredients', { state: { ingredients: response.data.ingredients } });
      }
    } catch (error) {
      console.error('Error uploading image:', error);
      navigate('/error');
    }
  };

  return (
    <div className="upload-container">
      <div className="image-preview">
        {selectedImage ? (
          <img src={URL.createObjectURL(selectedImage)} alt="Selected" />
        ) : (
          <p>이미지를 업로드 해주세요</p>
        )}
      </div>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleImageChange} required />
        <button type="submit">Upload and Detect</button>
      </form>
    </div>
  );
};

export default ImageUpload;
