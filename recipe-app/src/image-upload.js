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
      // Django의 recognize-ingredients API를 호출합니다.
      const response = await axios.post('/api/recognize-ingredients/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.ingredients) {
        // 식재료 정보가 성공적으로 응답되면 다음 페이지로 이동하며 데이터를 전달합니다.
        navigate('/ingredients', { state: { ingredients: response.data.ingredients } });
      }
    } catch (error) {
      console.error('Error uploading image:', error);
      // 에러 페이지로 이동
      navigate('/error');
    }
  };

  return (
    <div className="upload-container">
      <h1>이미지 업로드</h1>
      <div className="image-preview" id="imagePreview">
        {selectedImage ? (
          <img src={URL.createObjectURL(selectedImage)} alt="Selected" id="previewImage" />
        ) : (
          <p>이미지를 업로드 해주세요</p>
        )}
      </div>
      <form onSubmit={handleSubmit}>
        <input type="file" className="upload-btn" id="imageUpload" name="image" accept="image/*" onChange={handleImageChange} required />
        <button type="submit" className="submit-btn">이미지 인식</button>
      </form>
    </div>
  );
};

export default ImageUpload;
