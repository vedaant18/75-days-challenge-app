import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { socialService } from '../services/social';
import useAuthStore from '../store/authStore';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ProfileSidebar from '../components/social/ProfileSidebar';
import ChallengeCard from '../components/social/ChallengeCard';
import ActivityHeatmap from '../components/social/ActivityHeatmap';
import ActivityFeed from '../components/social/ActivityFeed';

export default function Profile() {
  const { username } = useParams();
  const { user: currentUser } = useAuthStore();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState('overview');

  const isOwnProfile = currentUser?.username === username;

  useEffect(() => {
    loadProfile();
  }, [username]);

  const loadProfile = async () => {
    setLoading(true);
    try {
      const res = await socialService.getProfile(username);
      setData(res.data);
    } catch {
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!data) {
    return (
      <div className="text-center py-20">
        <h1 className="text-2xl font-bold text-white">User not found</h1>
        <p className="text-gray-400 mt-2">This profile doesn&apos;t exist or is private.</p>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'challenges', label: 'Challenges', count: data.stats.total_challenges },
    { id: 'activity', label: 'Activity' },
  ];

  return (
    <div>
      {/* Tab bar */}
      <div className="border-b border-gray-800 mb-6">
        <div className="flex gap-6">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`pb-3 text-sm font-medium border-b-2 transition ${
                tab === t.id
                  ? 'border-indigo-500 text-white'
                  : 'border-transparent text-gray-400 hover:text-gray-300'
              }`}
            >
              {t.label}
              {t.count != null && (
                <span className="ml-1.5 bg-gray-800 text-gray-400 text-xs px-2 py-0.5 rounded-full">
                  {t.count}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Layout */}
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Sidebar */}
        <div className="lg:w-80 shrink-0">
          <ProfileSidebar
            user={data.user}
            profile={data.profile}
            stats={data.stats}
            isOwnProfile={isOwnProfile}
          />
        </div>

        {/* Main content */}
        <div className="flex-1 min-w-0">
          {tab === 'overview' && (
            <div className="space-y-6">
              {/* Challenges grid */}
              {data.challenges.length > 0 && (
                <div>
                  <h2 className="text-sm font-medium text-gray-400 mb-3">
                    {isOwnProfile ? 'Your challenges' : 'Challenges'}
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {data.challenges.slice(0, 6).map((c) => (
                      <ChallengeCard key={c.id} challenge={c} />
                    ))}
                  </div>
                </div>
              )}

              {/* Heatmap */}
              <ActivityHeatmap heatmap={data.heatmap} challenges={data.challenges} />

              {/* Recent activity */}
              {data.activity.length > 0 && (
                <ActivityFeed activity={data.activity} />
              )}
            </div>
          )}

          {tab === 'challenges' && (
            <div className="space-y-4">
              {data.challenges.length === 0 ? (
                <p className="text-gray-500 text-center py-12">No challenges yet.</p>
              ) : (
                data.challenges.map((c) => (
                  <ChallengeCard key={c.id} challenge={c} wide />
                ))
              )}
            </div>
          )}

          {tab === 'activity' && (
            <ActivityFeed activity={data.activity} full />
          )}
        </div>
      </div>
    </div>
  );
}
