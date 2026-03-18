import api from './api';

export const aiService = {
  chat: (message, conversationId = null, challengeId = null) =>
    api.post('/ai/chat', {
      message,
      conversation_id: conversationId,
      challenge_id: challengeId,
    }),
  getConversations: () => api.get('/ai/conversations'),
  getConversation: (id) => api.get(`/ai/conversations/${id}`),
};
