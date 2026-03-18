import { useState, useEffect } from 'react';
import { socialService } from '../services/social';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function Feed() {
  const [updates, setUpdates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);

  useEffect(() => {
    loadFeed();
  }, [page]);

  const loadFeed = async () => {
    setLoading(true);
    try {
      const res = await socialService.getFeed(page);
      setUpdates(res.data);
    } catch {
      setUpdates([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-white mb-6">Feed</h1>

      {updates.length === 0 ? (
        <div className="text-center py-16 text-gray-500">
          <p className="text-lg mb-2">No updates yet</p>
          <p className="text-sm">Follow other users to see their progress here.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {updates.map((update) => (
            <div key={update.id} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {update.user?.username?.[0]?.toUpperCase() || '?'}
                </div>
                <div>
                  <span className="text-white text-sm font-medium">{update.user?.username}</span>
                  <span className="text-gray-500 text-xs ml-2">
                    {update.update_type.replace('_', ' ')}
                  </span>
                </div>
              </div>
              {update.day_number && (
                <span className="text-xs bg-gray-800 text-gray-400 px-2 py-1 rounded mb-2 inline-block">
                  Day {update.day_number}
                </span>
              )}
              {update.content && <p className="text-gray-300 text-sm">{update.content}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
