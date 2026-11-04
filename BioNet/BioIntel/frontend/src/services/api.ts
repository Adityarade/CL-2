import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
});

export const searchPapers = async (query: string, entityType: string = 'All', ranking: string = 'Hybrid') => {
  const response = await api.get(`/search`, {
    params: { q: query, entity_type: entityType, ranking }
  });
  return response.data;
};

export const getStats = async () => {
  const response = await api.get(`/stats`);
  return response.data;
};

export const getAnalytics = async () => {
  const response = await api.get(`/analytics`);
  return response.data;
};

export const getHistory = async () => {
  const response = await api.get(`/search-history`);
  return response.data;
};

export const getEntities = async (type: 'genes' | 'diseases' | 'proteins' | 'drugs') => {
  const response = await api.get(`/${type}`);
  return response.data;
};
