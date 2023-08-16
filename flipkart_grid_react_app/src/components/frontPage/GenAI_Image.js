import React, { useState, useEffect } from 'react';

function GenAI_Image() {
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    // Making a GET request to fetch image data
    fetch('http://localhost:8000/image/', {
      method: 'GET',
      headers: {
        'Content-Type': 'image/png', // Set the content type
      },
    })
      .then(response => response.blob()) // Convert response to Blob
      .then(blob => {
        const url = URL.createObjectURL(blob); // Create a URL for the Blob
        setImageData(url);
      })
      .catch(error => console.error('Error fetching image:', error));
  }, []);

  return (
    <div>
      <h1>Image Display Example</h1>
      {imageData && <img src={imageData} alt="Fetched Image" />}
    </div>
  );
}

export default GenAI_Image;