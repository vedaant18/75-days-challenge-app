import api from './api';

export const challengeService = {
  create: (data) => api.post('/challenges', data),
  getActive: () => api.get('/challenges/active'),
  getById: (id) => api.get(`/challenges/${id}`),
  getHistory: () => api.get('/challenges/history'),
};
