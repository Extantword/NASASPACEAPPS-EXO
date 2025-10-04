/**
 * API endpoints for Exoplanet Explorer
 */
import apiClient from './client.js';

// Missions API
export const missionsAPI = {
  getAll: () => apiClient.get('/missions'),
  getById: (missionName) => apiClient.get(`/missions/${missionName}`),
};

// Stars API
export const starsAPI = {
  search: (query, mission = null, limit = 20) => 
    apiClient.get('/stars/search', { 
      params: { query, mission, limit } 
    }),
  getById: (starId) => apiClient.get(`/stars/${starId}`),
};

// Planets API
export const planetsAPI = {
  getAll: (filters = {}) => 
    apiClient.get('/planets', { params: filters }),
  getById: (planetId) => apiClient.get(`/planets/${planetId}`),
  getStats: () => apiClient.get('/planets/stats/overview'),
};

// Light Curves API
export const lightCurvesAPI = {
  get: (starId, mission = 'TESS', options = {}) => 
    apiClient.get(`/lightcurves/${starId}`, { 
      params: { mission, ...options } 
    }),
  download: (starId, mission = 'TESS') => 
    apiClient.get(`/lightcurves/${starId}/download`, { 
      params: { mission },
      responseType: 'blob'
    }),
  getMetadata: (starId, mission = 'TESS') => 
    apiClient.get(`/lightcurves/${starId}/metadata`, { 
      params: { mission } 
    }),
};

// Machine Learning API
export const mlAPI = {
  classify: (features, modelType = 'random_forest') => 
    apiClient.post('/ml/classify', { features, model_type: modelType }),
  getModels: () => apiClient.get('/ml/models'),
  batchPredict: (candidates) => 
    apiClient.post('/ml/predict_batch', candidates),
  getFeatureImportance: (modelType = 'random_forest') => 
    apiClient.get('/ml/feature_importance', { params: { model_type: modelType } }),
  getMetrics: (modelType) => apiClient.get(`/ml/metrics/${modelType}`),
};

// Health check
export const healthAPI = {
  check: () => apiClient.get('/health'),
  root: () => apiClient.get('/'),
};

// Export all APIs
const api = {
  missions: missionsAPI,
  stars: starsAPI,
  planets: planetsAPI,
  lightCurves: lightCurvesAPI,
  ml: mlAPI,
  health: healthAPI,
};

export default api;