import api from './api';

export const proofService = {
  upload: (file, taskCompletionId, caption = '') => {
    const formData = new FormData();
    formData.append('image', file);
    if (taskCompletionId) formData.append('task_completion_id', taskCompletionId);
    if (caption) formData.append('caption', caption);
    return api.post('/proofs/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getByDay: (dayNumber) => api.get(`/proofs/day/${dayNumber}`),
};
