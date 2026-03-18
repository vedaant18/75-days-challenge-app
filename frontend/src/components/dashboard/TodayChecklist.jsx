import { useState } from 'react';
import useChallengeStore from '../../store/challengeStore';
import ProofUpload from '../proofs/ProofUpload';

export default function TodayChecklist({ todayLog }) {
  const { completeTask } = useChallengeStore();
  const [completing, setCompleting] = useState(null);

  const handleComplete = async (tcId) => {
    setCompleting(tcId);
    try {
      await completeTask(tcId);
    } catch {
      // error in store
    } finally {
      setCompleting(null);
    }
  };

  if (!todayLog?.task_completions) {
    return <p className="text-gray-400">No tasks loaded.</p>;
  }

  return (
    <div className="space-y-3">
      {todayLog.task_completions.map((tc) => (
        <div
          key={tc.id}
          className={`flex items-center gap-4 p-4 rounded-xl border transition ${
            tc.is_completed
              ? 'bg-green-500/5 border-green-500/30'
              : 'bg-gray-800/50 border-gray-700'
          }`}
        >
          <button
            onClick={() => handleComplete(tc.id)}
            disabled={tc.is_completed || completing === tc.id}
            className={`w-6 h-6 rounded-md border-2 flex items-center justify-center shrink-0 transition ${
              tc.is_completed
                ? 'bg-green-500 border-green-500 text-white'
                : 'border-gray-600 hover:border-indigo-500'
            }`}
          >
            {tc.is_completed && (
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>
          <div className="flex-1">
            <span className={`text-sm ${tc.is_completed ? 'text-gray-400 line-through' : 'text-white'}`}>
              {tc.task?.title || `Task #${tc.task_id}`}
            </span>
            {tc.task?.category && (
              <span className="ml-2 text-xs bg-gray-800 text-gray-500 px-2 py-0.5 rounded">
                {tc.task.category.replace('_', ' ')}
              </span>
            )}
          </div>
          <ProofUpload taskCompletionId={tc.id} hasProof={!!tc.proof} />
        </div>
      ))}

      {/* Summary */}
      <div className="pt-3 border-t border-gray-800 flex justify-between text-sm text-gray-400">
        <span>
          {todayLog.tasks_completed}/{todayLog.tasks_total} tasks done
        </span>
        <span>
          {todayLog.proofs_submitted} proofs uploaded
        </span>
      </div>
    </div>
  );
}
