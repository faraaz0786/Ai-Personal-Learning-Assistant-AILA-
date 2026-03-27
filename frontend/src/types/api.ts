export type ExplainRequest = {
  topic: string;
  subject?: "Mathematics" | "Science" | "History" | "Technology" | "General";
};

export type SessionResponse = {
  id: string;
  created_at: string;
  last_active_at: string;
};

export type HealthResponse = {
  status: string;
  detail?: string;
};

export type ExplainResponse = {
  topic_id: string;
  normalized_topic: string;
  explanation: {
    definition: string;
    mechanism: string;
    example: string;
  };
  summary: string;
  cached: boolean;
  response_ms: number;
};

export type QuizRequest = {
  topic_id: string;
  count?: number;
  difficulty?: "easy" | "medium" | "hard";
};

export type QuizQuestion = {
  id: number;
  question: string;
  options: [string, string, string, string] | string[];
  correct_index: number;
  explanation: string;
};

export type QuizResponse = {
  quiz_id: string;
  topic_id: string;
  questions: QuizQuestion[];
};

export type QuizAttemptRequest = {
  answers: number[];
};

export type QuizAttemptResult = {
  question_id: number;
  correct: boolean;
  your_answer: number;
  correct_index: number;
};

export interface QuizInsight {
  strengths: string;
  weaknesses: string;
  what_to_improve: string;
  recommendation: string;
}

export type QuizAttemptResponse = {
  attempt_id: string;
  score: number;
  max_score: number;
  percentage: number;
  results: QuizAttemptResult[];
  analytics?: DashboardSummary;
  insights?: QuizInsight;
};

export type TopicListItem = {
  topic_id: string;
  normalized_topic: string;
  subject: string | null;
};

export type ProgressSummary = {
  topics_studied: number;
  average_score: number;
  streak_days: number;
  progress_percent: number;
};

export type ProgressHistoryItem = {
  topic: string;
  score: number;
  attempted_at: string;
};

export type PerformanceTrendItem = {
  date: string;
  score: number;
};

export type TopTopicItem = {
  topic: string;
  score: number;
};

export type DashboardSummary = {
  total_topics: number;
  total_questions: number;
  accuracy: number;
  avg_score: number;
  streak: number;
  recent_activity: ProgressHistoryItem[];
  performance_trend: PerformanceTrendItem[];
  top_topics: TopTopicItem[];
};

export type ProgressRecommendation = {
  topic: string;
  reason: string;
  type: "prerequisite" | "related" | "advanced";
};

export type ApiErrorResponse = {
  error: {
    code: string;
    message: string;
    details: Record<string, unknown>;
  };
};

export type SummaryUiState = {
  wordCount: number;
  copied: boolean;
};
