import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/layout/Layout';
import ProtectedRoute from './components/common/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import NewChallenge from './pages/NewChallenge';
import AICoach from './pages/AICoach';
import Feed from './pages/Feed';
import Profile from './pages/Profile';

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile/:username" element={<Profile />} />
            <Route
              path="/dashboard"
              element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
            />
            <Route
              path="/challenge/new"
              element={<ProtectedRoute><NewChallenge /></ProtectedRoute>}
            />
            <Route
              path="/ai"
              element={<ProtectedRoute><AICoach /></ProtectedRoute>}
            />
            <Route
              path="/feed"
              element={<ProtectedRoute><Feed /></ProtectedRoute>}
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
