export default function ActivityFeed({ activity, full }) {
  const items = full ? activity : activity.slice(0, 5);

  const typeIcons = {
    milestone: (
      <svg className="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
      </svg>
    ),
    daily_progress: (
      <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    completion: (
      <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
      </svg>
    ),
  };

  if (items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>No activity yet.</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-sm font-medium text-gray-400 mb-3">Activity</h2>
      <div className="relative pl-6 border-l border-gray-800 space-y-4">
        {items.map((item) => (
          <div key={item.id} className="relative">
            {/* Timeline dot */}
            <div className="absolute -left-[25px] top-1 w-3 h-3 bg-gray-800 border-2 border-gray-600 rounded-full" />

            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-1">
                {typeIcons[item.type] || typeIcons.daily_progress}
                <span className="text-xs text-gray-400 capitalize">
                  {item.type.replace('_', ' ')}
                </span>
                {item.day_number && (
                  <span className="text-xs bg-gray-800 text-gray-500 px-1.5 py-0.5 rounded">
                    Day {item.day_number}
                  </span>
                )}
                <span className="text-xs text-gray-600 ml-auto">
                  {item.created_at ? new Date(item.created_at).toLocaleDateString() : ''}
                </span>
              </div>
              {item.content && (
                <p className="text-sm text-gray-300">{item.content}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
