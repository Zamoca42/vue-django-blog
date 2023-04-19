import axios from 'axios';

let baseURL = '';

if (process.env.NODE_ENV === 'development') {
    baseURL = 'http://127.0.0.1:8000';
  } else {
    baseURL = 'https://server.zamoca.space';
  }

const instance = axios.create({
  baseURL: baseURL,
  timeout: 10000 
});

export default instance;