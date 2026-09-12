import { QueryResponse } from '../types';

// For local development, proxy takes care of /api routing
const BASE_URL = '';

export const apiClient = {
  async query(question: string): Promise<QueryResponse> {
    try {
      const response = await fetch(`${BASE_URL}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error in query API:', error);
      throw error;
    }
  },

  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${BASE_URL}/api/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
};
