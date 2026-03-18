export default function ProgressRing({ dashboard }) {
  const pct = dashboard.progress_pct || 0;
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (pct / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      <svg width="180" height="180" className="-rotate-90">
        <circle
          cx="90" cy="90" r={radius}
          stroke="#1f2937" strokeWidth="10" fill="none"
        />
        <circle
          cx="90" cy="90" r={radius}
          stroke="#6366f1" strokeWidth="10" fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="transition-all duration-700"
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center" style={{ marginTop: '50px' }}>
        <span className="text-3xl font-bold text-white">{pct}%</span>
        <span className="text-xs text-gray-400">complete</span>
      </div>
      <div className="mt-4 text-center">
        <p className="text-2xl font-bold text-white">
          Day {dashboard.current_day}
          <span className="text-gray-500 text-lg font-normal"> / {dashboard.total_days}</span>
        </p>
      </div>
    </div>
  );
}
