import { create } from "zustand";

import type { QuizAttemptResponse, QuizResponse } from "../types/api";

type QuizState = {
  currentQuiz: QuizResponse | null;
  answers: Record<number, number>;
  revealedQuestionIds: number[];
  currentQuestionIndex: number;
  attemptResult: QuizAttemptResponse | null;
  setQuiz: (quiz: QuizResponse) => void;
  selectAnswer: (questionId: number, answerIndex: number) => void;
  revealQuestion: (questionId: number) => void;
  nextQuestion: () => void;
  previousQuestion: () => void;
  setAttemptResult: (result: QuizAttemptResponse) => void;
  restartQuiz: () => void;
  resetQuiz: () => void;
};

const initialState = {
  currentQuiz: null,
  answers: {},
  revealedQuestionIds: [],
  currentQuestionIndex: 0,
  attemptResult: null
};

export const useQuizStore = create<QuizState>((set) => ({
  ...initialState,
  setQuiz: (quiz) =>
    set({
      currentQuiz: quiz,
      answers: {},
      revealedQuestionIds: [],
      currentQuestionIndex: 0,
      attemptResult: null
    }),
  selectAnswer: (questionId, answerIndex) =>
    set((state) => ({
      answers: { ...state.answers, [questionId]: answerIndex }
    })),
  revealQuestion: (questionId) =>
    set((state) => ({
      revealedQuestionIds: state.revealedQuestionIds.includes(questionId)
        ? state.revealedQuestionIds
        : [...state.revealedQuestionIds, questionId]
    })),
  nextQuestion: () =>
    set((state) => ({
      currentQuestionIndex:
        state.currentQuiz && state.currentQuestionIndex < state.currentQuiz.questions.length - 1
          ? state.currentQuestionIndex + 1
          : state.currentQuestionIndex
    })),
  previousQuestion: () =>
    set((state) => ({
      currentQuestionIndex:
        state.currentQuestionIndex > 0 ? state.currentQuestionIndex - 1 : 0
    })),
  setAttemptResult: (result) => set({ attemptResult: result }),
  restartQuiz: () =>
    set((state) => ({
      currentQuiz: state.currentQuiz,
      answers: {},
      revealedQuestionIds: [],
      currentQuestionIndex: 0,
      attemptResult: null
    })),
  resetQuiz: () => set(initialState)
}));
