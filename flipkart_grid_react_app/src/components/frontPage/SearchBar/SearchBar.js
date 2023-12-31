import React, { useEffect, useState } from 'react';
import './SearchBar.css'; // Import your CSS file for styling
import { AiOutlineSend } from 'react-icons/ai';
import Products from '../Products.js'
// import teamimage from "./PLACEHOLDER.png"
import teamimage from "./logo.png"

let start = 1;
function SearchBar() {
  const [imageData, setImageData] = useState(null);
  const [postData, setPostData] = useState({ user: '', query: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const [messages, setMessages] = useState([]);


  // Function to handle the POST request
  const handlePost = async () => {
    try {
      setIsLoading(true);
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
        getProductsToRender();
        start = 0;
      } else {
        console.error('POST request failed');
      }
      setMessages([...messages, postData.query]);
      console.log(messages);
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
      setIsLoading(false);
      if (response.ok) {
        console.log("Image retrived");
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

  // Function to handle the items returned from the inventory
  const getProductsToRender = () => {
    try {
      const response = fetch('http://localhost:8000/on_sale/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json', // Set the content type
        },
      })
      .then(response => response.json())
      .then(data => {
        // Handle the retrieved JSON data here
        console.log("data is ",  data);
        setProducts(data);

      })
      .catch(error => {
        // Handle errors here
        console.log("Error in getting products list")
      });
    } catch(error) {
      console.error("Error in getting Products data", error);
    }
  }


  useEffect(() => {
    if (imageData) {
      // Cleanup when component unmounts or when imageData changes
      return () => {
        URL.revokeObjectURL(imageData);
      };
    }
  }, [imageData]);
  const messageprint = messages.map((messag) => <p className='single-chat-msg'>{messag}</p>);
  return (
    <div>
      <div className='left'>
      <div><img className = "team-img" src={teamimage} alt = "."></img></div>
        <div className="prompt-container">
          <div className="prompt-box">
          <div className='temp-border'></div>
          <div className='temp-border2'></div>
            <div className="input-container">
              <input
                type="text"
                value={postData.query}
                onChange={e => setPostData({ ...postData, query: e.target.value })}
                placeholder='define your fashion'
                style={{
                  fontFamily: 'Montserrat, sans-serif', // Change the font family
                  fontSize: '13px',               // Change the font size
                  fontWeight: 'bold',            // Change the font weight
                  color: 'black',                 // Change the font color
                  borderRadius: '20px', 
                }}
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
              style={{
              fontFamily: 'Montserrat, sans-serif', // Change the font family
              fontSize: '13px',               // Change the font size
              fontWeight: 'bold',            // Change the font weight
              color: 'black', 
              borderRadius: '20px',                // Change the font color
            }}
            />
          </div>
        </div>
        {isLoading ? (
          <div><img  className='geni-image' src = "https://i.gifer.com/JVX7.gif" alt = "loading"></img></div> 
        ) : (
          imageData && <img  className='geni-image geni-image2' src={imageData} alt="Fetched Image" />
        )}
        <div className="chat-box">
        <h3 className='chat-box-head'>FASHION HISTORY</h3>
        <p className='chat-msg'>{messageprint}</p>
      </div>
      </div>
      <div className='right'>
        <Products ProductsList={products}/>
      </div>
    </div>

  );
}

export default SearchBar;
export let Start = start;






