import { useState, useRef } from 'react';
import { proofService } from '../../services/proofs';
import useChallengeStore from '../../store/challengeStore';

export default function ProofUpload({ taskCompletionId, hasProof }) {
  const [uploading, setUploading] = useState(false);
  const [done, setDone] = useState(hasProof);
  const fileRef = useRef(null);
  const { fetchToday } = useChallengeStore();

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      await proofService.upload(file, taskCompletionId);
      setDone(true);
      fetchToday();
    } catch {
      // TODO: show error
    } finally {
      setUploading(false);
    }
  };

  if (done) {
    return <span className="text-xs text-green-400">Proof uploaded</span>;
  }

  return (
    <>
      <input
        ref={fileRef}
        type="file"
        accept="image/png,image/jpeg"
        onChange={handleUpload}
        className="hidden"
      />
      <button
        onClick={() => fileRef.current?.click()}
        disabled={uploading}
        className="text-xs bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg hover:bg-gray-600 disabled:opacity-50"
      >
        {uploading ? 'Uploading...' : 'Add Proof'}
      </button>
    </>
  );
}
