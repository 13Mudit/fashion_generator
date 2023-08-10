import React, { useState } from 'react';
import './SearchBar.css'; // Import your CSS file for styling

import { AiOutlineSend } from 'react-icons/ai';

const SearchBar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [promptValue, setPromptValue] = useState('');
  
  const handleOpen = () => {
    setIsOpen(true);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleConfirm = () => {
    // Do something with the promptValue, e.g., show an alert
    alert(`You entered: ${promptValue}`);

    // SEND TO BACKEND 
    handleClose();
  };

  return (
    <div className="prompt-container">
      <div className="prompt-box">
        <div className="input-container">
          <input
            type="text"
            value={promptValue}
            onChange={(e) => setPromptValue(e.target.value)}
            placeholder="Enter something"
          />
          <button className="send-button" onClick={handleConfirm}>
            <AiOutlineSend />
          </button>
        </div>
      </div>
    </div>

  );
};



export default SearchBar;