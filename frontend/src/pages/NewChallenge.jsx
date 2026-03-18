import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useChallengeStore from '../store/challengeStore';

const CATEGORIES = [
  'health', 'spiritual', 'career', 'relationships',
  'social_life', 'financial', 'personal_growth', 'family',
];

const DIFFICULTY_INFO = {
  hard: { label: 'Hard', desc: 'No skips. Proof for all tasks.', color: 'text-red-400' },
  medium: { label: 'Medium', desc: '1 skip allowed. Proof for 3+ tasks.', color: 'text-yellow-400' },
  soft: { label: 'Soft', desc: '3 skips allowed. Proof for 1+ task.', color: 'text-green-400' },
};

const emptyTask = { title: '', category: 'health', description: '' };

export default function NewChallenge() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [difficulty, setDifficulty] = useState('medium');
  const [tasks, setTasks] = useState([{ ...emptyTask }, { ...emptyTask }, { ...emptyTask }, { ...emptyTask }, { ...emptyTask }]);
  const { createChallenge, loading, error } = useChallengeStore();
  const navigate = useNavigate();

  const updateTask = (index, field, value) => {
    const updated = [...tasks];
    updated[index] = { ...updated[index], [field]: value };
    setTasks(updated);
  };

  const addTask = () => {
    if (tasks.length < 8) setTasks([...tasks, { ...emptyTask }]);
  };

  const removeTask = (index) => {
    if (tasks.length > 5) setTasks(tasks.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createChallenge({ title, description, difficulty, tasks });
      navigate('/dashboard');
    } catch {
      // error in store
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-8">Start Your Challenge</h1>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg mb-6 text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Title */}
        <div>
          <label className="block text-sm text-gray-400 mb-1">Challenge Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g., Become the Best Version of Myself"
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-indigo-500"
            required
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm text-gray-400 mb-1">Description (optional)</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={2}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-indigo-500 resize-none"
          />
        </div>

        {/* Difficulty */}
        <div>
          <label className="block text-sm text-gray-400 mb-3">Difficulty</label>
          <div className="grid grid-cols-3 gap-3">
            {Object.entries(DIFFICULTY_INFO).map(([key, info]) => (
              <button
                key={key}
                type="button"
                onClick={() => setDifficulty(key)}
                className={`p-4 rounded-xl border text-left transition ${
                  difficulty === key
                    ? 'border-indigo-500 bg-indigo-500/10'
                    : 'border-gray-700 bg-gray-800 hover:border-gray-600'
                }`}
              >
                <span className={`font-semibold ${info.color}`}>{info.label}</span>
                <p className="text-xs text-gray-400 mt-1">{info.desc}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Tasks */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <label className="text-sm text-gray-400">
              Daily Tasks ({tasks.length}/8) — min 5 required
            </label>
            {tasks.length < 8 && (
              <button type="button" onClick={addTask} className="text-sm text-indigo-400 hover:text-indigo-300">
                + Add Task
              </button>
            )}
          </div>
          <div className="space-y-3">
            {tasks.map((task, i) => (
              <div key={i} className="flex gap-3 items-start">
                <div className="flex-1 space-y-2">
                  <input
                    type="text"
                    value={task.title}
                    onChange={(e) => updateTask(i, 'title', e.target.value)}
                    placeholder={`Task ${i + 1} — e.g., Run 5km`}
                    className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-indigo-500"
                    required
                  />
                  <select
                    value={task.category}
                    onChange={(e) => updateTask(i, 'category', e.target.value)}
                    className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-gray-300 text-sm focus:outline-none focus:border-indigo-500"
                  >
                    {CATEGORIES.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
                      </option>
                    ))}
                  </select>
                </div>
                {tasks.length > 5 && (
                  <button
                    type="button"
                    onClick={() => removeTask(i)}
                    className="text-red-400 hover:text-red-300 mt-2 text-sm"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Warning */}
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 text-sm text-yellow-400">
          Once started, your challenge <strong>cannot be edited or canceled</strong>. Tasks are locked for 75 days.
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 text-white py-4 rounded-xl font-medium text-lg hover:bg-indigo-500 disabled:opacity-50"
        >
          {loading ? 'Creating...' : 'Start 75-Day Challenge'}
        </button>
      </form>
    </div>
  );
}
