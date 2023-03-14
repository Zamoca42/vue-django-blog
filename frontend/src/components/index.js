import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://43.201.163.241', // Replace with your Django server's URL
  timeout: 10000 // Set a timeout if needed
});

export default instance;