import { Link } from 'react-router-dom';

export default function ProfileSidebar({ user, profile, stats, isOwnProfile }) {
  const initials = (profile.display_name || user.username || '?')
    .split(' ')
    .map((w) => w[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  return (
    <div className="space-y-4">
      {/* Avatar */}
      <div className="relative">
        {profile.avatar_url ? (
          <img
            src={profile.avatar_url}
            alt={user.username}
            className="w-72 h-72 rounded-full border-2 border-gray-700 object-cover mx-auto lg:mx-0"
          />
        ) : (
          <div className="w-72 h-72 rounded-full border-2 border-gray-700 bg-gray-800 flex items-center justify-center mx-auto lg:mx-0">
            <span className="text-6xl font-bold text-gray-500">{initials}</span>
          </div>
        )}
      </div>

      {/* Name */}
      <div>
        {profile.display_name && (
          <h1 className="text-2xl font-bold text-white leading-tight">{profile.display_name}</h1>
        )}
        <p className="text-xl text-gray-400">{user.username}</p>
      </div>

      {/* Bio */}
      {profile.bio && (
        <p className="text-sm text-gray-300">{profile.bio}</p>
      )}

      {/* Edit profile */}
      {isOwnProfile && (
        <button className="w-full border border-gray-600 text-gray-300 text-sm font-medium py-1.5 rounded-md hover:bg-gray-800 transition">
          Edit profile
        </button>
      )}

      {/* Follow button */}
      {!isOwnProfile && (
        <button className="w-full bg-gray-700 text-white text-sm font-medium py-1.5 rounded-md hover:bg-gray-600 transition">
          Follow
        </button>
      )}

      {/* Followers / Following */}
      <div className="flex items-center gap-4 text-sm">
        <span className="text-gray-400">
          <span className="text-white font-semibold">{stats.followers}</span> followers
        </span>
        <span className="text-gray-400">
          <span className="text-white font-semibold">{stats.following}</span> following
        </span>
      </div>

      {/* Stats */}
      <div className="border-t border-gray-800 pt-4 space-y-2">
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span>
            <span className="text-white font-medium">{stats.total_completed_days}</span> days completed
          </span>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>
            <span className="text-white font-medium">{stats.completed_challenges}</span> challenges completed
          </span>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
          </svg>
          <span>
            <span className="text-white font-medium">{profile.longest_streak}</span> longest streak
          </span>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
          </svg>
          <span>
            <span className="text-white font-medium">{profile.current_streak}</span> current streak
          </span>
        </div>
        {stats.active_challenge && (
          <div className="flex items-center gap-2 text-sm">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400">Active challenge</span>
          </div>
        )}
      </div>

      {/* Joined date */}
      <div className="border-t border-gray-800 pt-4">
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Joined {user.created_at ? new Date(user.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) : 'recently'}
        </div>
      </div>
    </div>
  );
}
