import { create } from 'zustand';
import { challengeService } from '../services/challenges';
import { progressService } from '../services/progress';

const useChallengeStore = create((set, get) => ({
  challenge: null,
  dashboard: null,
  todayLog: null,
  history: [],
  loading: false,
  error: null,

  fetchActive: async () => {
    set({ loading: true, error: null });
    try {
      const res = await challengeService.getActive();
      set({ challenge: res.data, loading: false });
    } catch (err) {
      if (err.response?.status === 404) {
        set({ challenge: null, loading: false });
      } else {
        set({ error: err.response?.data?.error, loading: false });
      }
    }
  },

  fetchDashboard: async () => {
    try {
      const res = await progressService.getDashboard();
      set({ dashboard: res.data });
    } catch {
      // no active challenge
    }
  },

  fetchToday: async () => {
    try {
      const res = await progressService.getToday();
      set({ todayLog: res.data });
    } catch {
      set({ todayLog: null });
    }
  },

  createChallenge: async (data) => {
    set({ loading: true, error: null });
    try {
      const res = await challengeService.create(data);
      set({ challenge: res.data, loading: false });
      return res.data;
    } catch (err) {
      set({ error: err.response?.data?.error, loading: false });
      throw err;
    }
  },

  completeTask: async (taskCompletionId) => {
    try {
      const res = await progressService.completeTask(taskCompletionId);
      set({ todayLog: res.data });
      get().fetchDashboard();
    } catch (err) {
      set({ error: err.response?.data?.error });
      throw err;
    }
  },

  skipDay: async () => {
    try {
      const res = await progressService.skipDay();
      set({ todayLog: res.data });
      get().fetchDashboard();
    } catch (err) {
      set({ error: err.response?.data?.error });
      throw err;
    }
  },

  fetchHistory: async () => {
    try {
      const res = await challengeService.getHistory();
      set({ history: res.data });
    } catch {
      set({ history: [] });
    }
  },

  clearError: () => set({ error: null }),
}));

export default useChallengeStore;
