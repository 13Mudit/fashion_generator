import React, { useEffect, useState } from 'react';
import './SearchBar.css'; // Import your CSS file for styling
import { AiOutlineSend } from 'react-icons/ai';

function SearchBar() {
  const [imageData, setImageData] = useState(null);
  const [postData, setPostData] = useState({ user: '', query: '' });

  // Function to handle the POST request
  const handlePost = async () => {
    try {
      const response = await fetch('http://localhost:8000/query/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
      });
      if (response.ok) {
        console.log('POST request successful');
        // Trigger a GET request after successful POST
        fetchImage();
      } else {
        console.error('POST request failed');
      }
    } catch (error) {
      console.error('Error sending POST request:', error);
    }
  };

  // Function to handle the GET request for image
  const fetchImage = async () => {
    try {
      const response = await fetch('http://localhost:8000/image/', {
        method: 'GET',
        headers: {
          'Content-Type': 'image/png', // Set the content type
        },
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setImageData(url);
      } else {
        console.error('GET request for image failed');
      }
    } catch (error) {
      console.error('Error fetching image:', error);
    }
  };

  useEffect(() => {
    if (imageData) {
      // Cleanup when component unmounts or when imageData changes
      return () => {
        URL.revokeObjectURL(imageData);
      };
    }
  }, [imageData]);

  return (
    <div>
      <div className="prompt-container">
        <div className="prompt-box">
          <div className="input-container">
            <input
              type="text"
              value={postData.query}
              onChange={e => setPostData({ ...postData, query: e.target.value })}
              placeholder='define your fashion'
            />
          </div>
        </div>
        <button className="send-button" onClick={handlePost}>
            <AiOutlineSend />
          </button>
        <div className="user-input">
        <input
            type="text"
            value={postData.user}
            onChange={e => setPostData({ ...postData, user: e.target.value })}
            placeholder='user id'
          />
        </div>
      </div>
      {imageData && <img src={imageData} alt="Fetched Image" />}
    </div>
  );
}

export default SearchBar;