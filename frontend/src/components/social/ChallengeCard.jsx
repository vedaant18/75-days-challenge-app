export default function ChallengeCard({ challenge, wide }) {
  const c = challenge;
  const pct = c.total_days > 0 ? Math.round((c.completed_days / c.total_days) * 100) : 0;

  const statusColors = {
    active: 'bg-green-500/20 text-green-400 border-green-500/30',
    completed: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    failed: 'bg-red-500/20 text-red-400 border-red-500/30',
    stale: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  };

  const difficultyColors = {
    hard: 'text-red-400',
    medium: 'text-yellow-400',
    soft: 'text-green-400',
  };

  return (
    <div className={`border border-gray-700 rounded-lg p-4 hover:border-gray-500 transition ${wide ? '' : ''}`}>
      <div className="flex items-start justify-between mb-2">
        <h3 className="text-sm font-semibold text-indigo-400 hover:underline cursor-pointer truncate pr-3">
          {c.title}
        </h3>
        <span className={`text-xs px-2 py-0.5 rounded-full border shrink-0 ${statusColors[c.status]}`}>
          {c.status.charAt(0).toUpperCase() + c.status.slice(1)}
        </span>
      </div>

      {c.description && (
        <p className="text-xs text-gray-400 mb-3 line-clamp-2">{c.description}</p>
      )}

      <div className="flex items-center gap-4 text-xs text-gray-400">
        <span className="flex items-center gap-1">
          <span className={`w-2.5 h-2.5 rounded-full ${
            c.difficulty === 'hard' ? 'bg-red-400' :
            c.difficulty === 'medium' ? 'bg-yellow-400' : 'bg-green-400'
          }`} />
          <span className={difficultyColors[c.difficulty]}>
            {c.difficulty.charAt(0).toUpperCase() + c.difficulty.slice(1)}
          </span>
        </span>
        <span>Day {c.current_day}/{c.total_days}</span>
        <span>{pct}% done</span>
      </div>

      {/* Mini progress bar */}
      <div className="mt-3 h-1 bg-gray-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${
            c.status === 'completed' ? 'bg-blue-500' :
            c.status === 'active' ? 'bg-green-500' : 'bg-gray-600'
          }`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
