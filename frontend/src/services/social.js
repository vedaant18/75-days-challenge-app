import api from './api';

export const socialService = {
  getProfile: (username) => api.get(`/social/profile/${username}`),
  share: (data) => api.post('/social/share', data),
  getFeed: (page = 1) => api.get(`/social/feed?page=${page}`),
  follow: (userId) => api.post(`/social/follow/${userId}`),
  unfollow: (userId) => api.post(`/social/unfollow/${userId}`),
};
