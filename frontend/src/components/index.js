import axios from 'axios';

let baseURL = '';

if (process.env.NODE_ENV === 'development') {
    // Set base URL for development mode
    baseURL = 'http://127.0.0.1:8000';
  } else {
    // Set base URL for production mode
    baseURL = 'https://server.zamoca.space';
  }

const instance = axios.create({
  baseURL: baseURL, // Replace with your Django server's URL
  timeout: 10000 // Set a timeout if needed
});

export default instance;