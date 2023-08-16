import React, { useState } from 'react';
import './SearchBar.css'; // Import your CSS file for styling
import { AiOutlineSend } from 'react-icons/ai';

function SearchBar() {
  const [searchValue, setSearchValue] = useState('');
  const [userId, setUserId] = useState('');
  
  const handleSubmit = () => {
    const dataToSend = {
      searchValue: searchValue,
      userId: userId,
    };
    
    fetch('https://api.example.com/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dataToSend),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Data successfully sent:', data);
        setSearchValue('');
        setUserId('');
      })
      .catch(error => console.error('Error sending data:', error));
  };

  return (
    <div>
      <div className="prompt-container">
        <div className="prompt-box">
          <div className="input-container">
            <input
              type="text"
              id="searchInput"
              value={searchValue}
              onChange={event => setSearchValue(event.target.value)}
              placeholder='define your fashion'
            />
          </div>
        </div>
        <button className="send-button" onClick={handleSubmit}>
            <AiOutlineSend />
          </button>
        <div className="user-input">
          <input
            type="text"
            id="userIdInput"
            value={userId}
            onChange={event => setUserId(event.target.value)}
            placeholder='user id'
          />
        </div>
      </div>
      
    </div>
  );
}

export default SearchBar;
