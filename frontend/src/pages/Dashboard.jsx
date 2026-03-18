import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import useChallengeStore from '../store/challengeStore';
import useAuthStore from '../store/authStore';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ProgressRing from '../components/dashboard/ProgressRing';
import TodayChecklist from '../components/dashboard/TodayChecklist';
import StatsBar from '../components/dashboard/StatsBar';

export default function Dashboard() {
  const { user, fetchUser } = useAuthStore();
  const { challenge, dashboard, todayLog, loading, fetchActive, fetchDashboard, fetchToday } =
    useChallengeStore();

  useEffect(() => {
    fetchUser();
    fetchActive().then(() => {
      fetchDashboard();
      fetchToday();
    }).catch(() => {});
  }, []);

  if (loading) return <LoadingSpinner />;

  // No active challenge — show create prompt
  if (!challenge) {
    return (
      <div className="text-center py-20">
        <h1 className="text-4xl font-bold text-white mb-4">Ready to Transform?</h1>
        <p className="text-gray-400 mb-8 max-w-md mx-auto">
          Start your 75-day discipline challenge. Define your tasks, pick your difficulty, and commit.
        </p>
        <Link
          to="/challenge/new"
          className="bg-indigo-600 text-white px-8 py-4 rounded-xl text-lg font-medium hover:bg-indigo-500 inline-block"
        >
          Start a Challenge
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">{challenge.title}</h1>
          <p className="text-gray-400 mt-1">
            <span className="capitalize">{challenge.difficulty}</span> mode
          </p>
        </div>
        <div className="text-right">
          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
            challenge.status === 'active' ? 'bg-green-500/20 text-green-400' :
            challenge.status === 'completed' ? 'bg-blue-500/20 text-blue-400' :
            'bg-red-500/20 text-red-400'
          }`}>
            {challenge.status.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Stats */}
      {dashboard && <StatsBar dashboard={dashboard} />}

      {/* Main grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Progress ring */}
        <div className="bg-gray-900 rounded-2xl p-6 border border-gray-800 flex flex-col items-center justify-center">
          {dashboard && <ProgressRing dashboard={dashboard} />}
        </div>

        {/* Today's checklist */}
        <div className="lg:col-span-2 bg-gray-900 rounded-2xl p-6 border border-gray-800">
          <h2 className="text-xl font-semibold text-white mb-4">
            Day {dashboard?.current_day || 1} of {dashboard?.total_days || 75}
          </h2>
          {todayLog ? (
            <TodayChecklist todayLog={todayLog} />
          ) : (
            <p className="text-gray-400">Loading today&apos;s tasks...</p>
          )}
        </div>
      </div>
    </div>
  );
}
