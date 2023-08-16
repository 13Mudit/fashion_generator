import React, { useState } from "react";
import "./Userid.css";
function UserId() {
  // State to store the user ID input
  const [userId, setUserId] = useState("");

  // Function to handle changes in the input
  const handleInputChange = (event) => {
    setUserId(event.target.value);
  };

  return (
    <div>
      <div className="user-input">
        <input
          type="text"
          id="userIdInput"
          value={userId}
          onChange={handleInputChange}
          placeholder="Enter your UserId"
        />
         <p>You entered: {userId}</p>
      </div>
    </div>
  );
}

export default UserId;
