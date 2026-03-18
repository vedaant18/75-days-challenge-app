import { Link } from 'react-router-dom';
import useAuthStore from '../store/authStore';

export default function Home() {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="text-center py-20">
      <h1 className="text-5xl font-bold text-white mb-6 leading-tight">
        75 Days.<br />No Excuses.
      </h1>
      <p className="text-xl text-gray-400 max-w-lg mx-auto mb-10">
        A discipline system that transforms your life through structured, time-bound challenges.
        Consistency + Accountability = Transformation.
      </p>

      <div className="flex justify-center gap-4">
        {isAuthenticated ? (
          <Link
            to="/dashboard"
            className="bg-indigo-600 text-white px-8 py-4 rounded-xl text-lg font-medium hover:bg-indigo-500"
          >
            Go to Dashboard
          </Link>
        ) : (
          <>
            <Link
              to="/register"
              className="bg-indigo-600 text-white px-8 py-4 rounded-xl text-lg font-medium hover:bg-indigo-500"
            >
              Get Started
            </Link>
            <Link
              to="/login"
              className="border border-gray-700 text-gray-300 px-8 py-4 rounded-xl text-lg font-medium hover:bg-gray-800"
            >
              Sign In
            </Link>
          </>
        )}
      </div>

      {/* Feature cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 text-left">
        {[
          { title: 'Strict Accountability', desc: 'No edits. No restarts. Miss too many days and your challenge ends.' },
          { title: 'AI Coach', desc: 'Get personalized task suggestions, progress analysis, and motivation from your AI coach.' },
          { title: 'Proof-Based', desc: 'Upload proof for your daily tasks. Hard mode requires proof for every single task.' },
        ].map((f) => (
          <div key={f.title} className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-white mb-2">{f.title}</h3>
            <p className="text-gray-400 text-sm">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
