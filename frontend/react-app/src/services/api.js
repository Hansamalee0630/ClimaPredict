// import axios from 'axios';

// const client = axios.create({ baseURL: '/' });

// export const getLatest = () => client.get('/api/latest');
// export const getHistory = (hours=72) => client.get(`/api/history?hours=${hours}`);

import axios from 'axios';

// Point the base URL to the Flask Python Backend
const client = axios.create({ baseURL: 'http://127.0.0.1:5000' });

export const getLatest = () => client.get('/api/latest');
export const getHistory = (options = { hours: 72 }) => {
  if (options.start && options.end) {
    return client.get(`/api/history?start=${options.start}&end=${options.end}`);
  }
  return client.get(`/api/history?hours=${options.hours || 72}`);
};