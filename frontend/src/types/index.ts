export interface Evidence {
  document: string;
  section: string | null;
  page: number | null;
  text: string;
  relevance_score?: number;
}

export interface Citation {
  id: string;
  document: string;
  section: string | null;
  page: number | null;
}

export interface Conflict {
  evidence_a: string;
  citation_a: Citation;
  evidence_b: string;
  citation_b: Citation;
  reason: string;
}

export interface QueryResponse {
  state: 'SUPPORTED' | 'NOT_FOUND' | 'CONTRADICTION';
  answer: string;
  evidence: Evidence[];
  citations: Citation[];
  conflicts?: Conflict[];
  query_analysis?: {
    topic: string;
    entities: string[];
    conditions: string[];
  };
  reasoning?: string;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'system';
  question?: string;
  response?: QueryResponse;
  timestamp: Date;
  isLoading?: boolean;
  error?: string;
}
