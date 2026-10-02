const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export const analyzeQuery = async (queryText) => {
  const response = await fetch(`${API_BASE}/analysis`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: queryText }),
  });

  const data = await response.json();
  if (!response.ok || !data.success) {
    throw new Error(data.error || 'Failed to analyze student query');
  }
  return data.data;
};

export const fetchHistory = async (limit = 50) => {
  const response = await fetch(`${API_BASE}/analysis?limit=${limit}`);
  const data = await response.json();
  if (!response.ok || !data.success) {
    throw new Error(data.error || 'Failed to fetch analysis history');
  }
  return data.data || [];
};

export const fetchAnalysisById = async (id) => {
  const response = await fetch(`${API_BASE}/analysis/${id}`);
  const data = await response.json();
  if (!response.ok || !data.success) {
    throw new Error(data.error || 'Failed to retrieve analysis');
  }
  return data.data;
};

export const deleteAnalysisById = async (id) => {
  const response = await fetch(`${API_BASE}/analysis/${id}`, {
    method: 'DELETE',
  });
  const data = await response.json();
  if (!response.ok || !data.success) {
    throw new Error(data.error || 'Failed to delete record');
  }
  return data;
};

export const clearAllHistory = async () => {
  const response = await fetch(`${API_BASE}/analysis`, {
    method: 'DELETE',
  });
  const data = await response.json();
  if (!response.ok || !data.success) {
    throw new Error(data.error || 'Failed to clear history');
  }
  return data;
};

export const fetchIntents = async () => {
  const response = await fetch(`${API_BASE}/intents`);
  const data = await response.json();
  if (!response.ok || !data.success) {
    throw new Error(data.error || 'Failed to load intent catalog');
  }
  return data.data || [];
};

export const fetchHealth = async () => {
  const response = await fetch(`${API_BASE}/health`);
  return await response.json();
};
