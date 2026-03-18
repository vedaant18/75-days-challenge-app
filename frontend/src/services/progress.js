import api from './api';

export const progressService = {
  getToday: () => api.get('/progress/today'),
  completeTask: (taskCompletionId) =>
    api.post('/progress/complete-task', { task_completion_id: taskCompletionId }),
  skipDay: () => api.post('/progress/skip'),
  getDashboard: () => api.get('/progress/dashboard'),
  getHistory: () => api.get('/progress/history'),
};
