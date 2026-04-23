import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  withCredentials: true,  // Vigtig for sessions
});

// Health check
export const healthCheck = () => api.get('/health');

// Auth endpoints
export const signup = (username, password) => api.post('/signup', { username, password });
export const login = (username, password) => api.post('/login', { username, password });
export const logout = () => api.post('/logout');
export const getMe = () => api.get('/me');

export default api;