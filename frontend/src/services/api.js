import axios from 'axios';

// Use VITE_API_BASE_URL if set, otherwise default to localhost for local dev
const api = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000',
  headers: {
    // Authorization header is not needed for local dev with auth disabled
  }
});

// Predict failure
export const predictFailure = (alarmLog) => api.post('/api/predict', alarmLog);
// Get LLM explanation for a prediction
export const explainPrediction = (explainIn) => api.post('/api/explain', explainIn);
// Get logs
export const getLogs = () => api.get('/api/logs');

export default api; 