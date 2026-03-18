import { useMemo } from 'react';

export default function ActivityHeatmap({ heatmap, challenges }) {
  const challenge = challenges?.[0];

  const { grid, totalCompleted } = useMemo(() => {
    if (!challenge) return { grid: [], totalCompleted: 0 };

    const start = new Date(challenge.start_date);
    const days = [];

    for (let i = 0; i < challenge.total_days; i++) {
      const d = new Date(start);
      d.setDate(d.getDate() + i);
      const dateStr = d.toISOString().split('T')[0];
      days.push({
        date: dateStr,
        dayNumber: i + 1,
        data: heatmap[dateStr] || null,
      });
    }

    const totalCompleted = days.filter(
      (d) => d.data?.status === 'completed'
    ).length;

    // 75 days into columns of 7
    const grid = [];
    for (let i = 0; i < days.length; i += 7) {
      grid.push(days.slice(i, i + 7));
    }

    return { grid, totalCompleted };
  }, [heatmap, challenge]);

  const getCellColor = (day) => {
    if (!day.data) return 'bg-[#161b22]';
    const { status, tasks_completed, tasks_total } = day.data;
    if (status === 'completed') {
      if (tasks_total === 0) return 'bg-[#161b22]';
      const ratio = tasks_completed / tasks_total;
      if (ratio >= 1) return 'bg-[#39d353]';
      if (ratio >= 0.75) return 'bg-[#26a641]';
      if (ratio >= 0.5) return 'bg-[#006d32]';
      return 'bg-[#0e4429]';
    }
    if (status === 'missed') return 'bg-red-900/40';
    return 'bg-[#161b22]';
  };

  const getTooltip = (day) => {
    if (!day.data) return `Day ${day.dayNumber} (${day.date})`;
    const { tasks_completed, tasks_total, status } = day.data;
    return `Day ${day.dayNumber}: ${tasks_completed}/${tasks_total} tasks — ${status}`;
  };

  if (!challenge) {
    return (
      <div className="border border-gray-800 rounded-lg p-4">
        <p className="text-sm text-gray-500">No challenge data to display.</p>
      </div>
    );
  }

  return (
    <div className="border border-gray-800 rounded-lg p-5">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <p className="text-sm text-gray-400">
          <span className="text-white font-semibold">{totalCompleted}</span> of{' '}
          <span className="text-white font-semibold">{challenge.total_days}</span> days completed
          {challenge.status === 'active' && (
            <span className="text-green-400 ml-2">— Day {challenge.current_day}</span>
          )}
        </p>
        <span className={`text-xs px-2 py-0.5 rounded-full ${
          challenge.status === 'active' ? 'bg-green-500/20 text-green-400' :
          challenge.status === 'completed' ? 'bg-blue-500/20 text-blue-400' :
          'bg-red-500/20 text-red-400'
        }`}>
          {challenge.title}
        </span>
      </div>

      {/* Week labels */}
      <div className="flex w-full mb-1">
        {grid.map((_, i) => (
          <div key={i} className="flex-1 text-center">
            <span className="text-[10px] text-gray-600">
              {i === 0 || (i + 1) % 2 === 0 ? `W${i + 1}` : ''}
            </span>
          </div>
        ))}
      </div>

      {/* Grid — 7 rows, each row stretches full width */}
      {Array.from({ length: 7 }).map((_, row) => (
        <div key={row} className="flex w-full gap-[3px] mb-[3px]">
          {grid.map((week, col) => {
            const day = week[row];
            if (!day) {
              return <div key={col} className="flex-1 aspect-square rounded-sm" />;
            }
            return (
              <div
                key={col}
                className={`flex-1 aspect-square rounded-sm ${getCellColor(day)} hover:ring-1 hover:ring-gray-400 cursor-pointer transition-all`}
                title={getTooltip(day)}
              />
            );
          })}
        </div>
      ))}

      {/* Legend */}
      <div className="flex items-center justify-end gap-1.5 mt-4">
        <span className="text-[10px] text-gray-500">Less</span>
        <div className="w-3 h-3 rounded-sm bg-[#161b22]" />
        <div className="w-3 h-3 rounded-sm bg-[#0e4429]" />
        <div className="w-3 h-3 rounded-sm bg-[#006d32]" />
        <div className="w-3 h-3 rounded-sm bg-[#26a641]" />
        <div className="w-3 h-3 rounded-sm bg-[#39d353]" />
        <span className="text-[10px] text-gray-500">More</span>
      </div>
    </div>
  );
}
