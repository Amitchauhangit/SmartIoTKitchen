import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import BASE_URL from './config.js'


const App = () => {

  const [imageList, setImageList] = useState([]);
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [registrationMode, setRegistrationMode] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  
  useEffect(() => {

    if (loggedIn) {
      fetchData();
      const interval = setInterval(fetchData, 5000);
      return () => clearInterval(interval);
    }
   
  }, [loggedIn]);


  const handleLogin = async (e) => {
      e.preventDefault();
      try {
        const response = await axios.post(`${BASE_URL}/login`, {
            username,
            password
        });

        if(response.data.success)
        {
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        
        setLoggedIn(true);
      }
      else
      {
        setErrorMessage("Invalid user or password!")
      }
      } catch (error) {
        console.error(error);
      }
    
  };

  const fetchData = async () => {
    try {

      const access_token = localStorage.getItem('access_token');
      const response = await axios.get(`${BASE_URL}/index`, {
            headers: {
                Authorization: `Bearer ${access_token}`
            }
        });
      setImageList(response.data);
      } catch (error) {
      console.error(error);
    }
  };

  const handleRemoveImage = async (imageURL) => {
    try {
      const access_token = localStorage.getItem('access_token');
      await axios.post(`${BASE_URL}/remove`, {
        image_url: imageURL,
      },{
        headers: {
            Authorization: `Bearer ${access_token}`
        }
    }
      );

      setImageList((prevImageList) =>
        prevImageList.filter((item) => item.image_url !== imageURL)
      );
    } catch (error) {
      console.error(error);
    }
  };

  const handleRegistration = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(`${BASE_URL}/register`, {
        username,
        password,
      });

      if (response.data.success) {
        setErrorMessage('');
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        setLoggedIn(true);
      } else {
        setErrorMessage(response.data.message);
      }
    } catch (error) {
      console.error(error);
    }
  };


  const handleLogout = async () => {
    try {
      await axios.post(`${BASE_URL}/logout`);
      setLoggedIn(false);
      setUsername('');
      setPassword('');
      localStorage.removeItem('access_token')
    } catch (error) {
      console.error(error);
    }
  };

  const handleToggleMode = () => {
    setRegistrationMode(!registrationMode);
    setErrorMessage('');
    setUsername('');
    setPassword('');
  };

  if (!loggedIn) {
    return (
      <div>
        <h1 className="heading">SmartIotKitchen Login</h1>
        <form className="login-form" onSubmit={registrationMode ? handleRegistration : handleLogin}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">{registrationMode ? 'Register' : 'Login'}</button>
        </form>
        <div className="toggle-mode">
          {registrationMode ? (
            <p>Already have an account? <span onClick={handleToggleMode}>Login</span></p>
          ) : (
            <p>Don't have an account? <span onClick={handleToggleMode}>Register</span></p>
          )}
        </div>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
      </div>
    );
  };
  

  return (
    <div>
      <header>
        <div className="user-info">
          <span>Welcome, {username}!</span>
        </div>
     

      <h1 className="heading">SmartIotKitchen List</h1>
      </header>
      <ul className="image-list">
        {
        (imageList != null) &&
        imageList.map((item) => (
          <li key={item.image_url} className="image-item">
            <div className="card">
              <img src={item.auth_image_url} alt="list-item" className="image" />
              <label className="toggle-switch">
              <div class="sliderop">Remove</div>
                <input
                  type="checkbox"
                  onChange={() => handleRemoveImage(item.image_url)}
                />
                <span className="slider"></span>
              </label>
            </div>
          </li>
        ))}
      </ul>
      <button className="logout-button" onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default App;



