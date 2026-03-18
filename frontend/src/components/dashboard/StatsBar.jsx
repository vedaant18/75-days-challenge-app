export default function StatsBar({ dashboard }) {
  const stats = [
    { label: 'Streak', value: dashboard.streak, color: 'text-orange-400' },
    { label: 'Completed', value: `${dashboard.completed_days}/${dashboard.total_days}`, color: 'text-green-400' },
    { label: 'Skips Used', value: `${dashboard.skips_used}/${dashboard.skips_allowed}`, color: 'text-yellow-400' },
    { label: 'Failures', value: dashboard.failures_count, color: 'text-red-400' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((s) => (
        <div key={s.label} className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
          <p className="text-xs text-gray-400 mt-1">{s.label}</p>
        </div>
      ))}
    </div>
  );
}
