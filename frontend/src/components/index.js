import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://server.zamoca.space', // Replace with your Django server's URL
  timeout: 10000 // Set a timeout if needed
});

export default instance;