import { fireEvent, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import { QuizInterface } from "../src/modules/quiz/QuizInterface";
import { useQuizStore } from "../src/store/quizStore";
import { renderWithProviders } from "./test-utils";

vi.mock("../src/api/quiz", () => ({
  submitQuizAttempt: vi.fn(async () => ({
    attempt_id: "attempt-1",
    score: 1,
    max_score: 1,
    percentage: 100,
    results: [{ question_id: 1, correct: true, your_answer: 0, correct_index: 0 }]
  }))
}));

describe("QuizInterface", () => {
  beforeEach(() => {
    useQuizStore.setState({
      currentQuiz: {
        quiz_id: "quiz-1",
        topic_id: "topic-1",
        questions: [
          {
            id: 1,
            question: "What is the main purpose of photosynthesis?",
            options: ["Make glucose", "Create plastic", "Break metal", "Move planets"],
            correct_index: 0,
            explanation: "Photosynthesis helps plants make glucose."
          }
        ]
      },
      answers: {},
      revealedQuestionIds: [],
      currentQuestionIndex: 0,
      attemptResult: null
    });
  });

  test("reveals explanation after answer submission", async () => {
    renderWithProviders(<QuizInterface />);

    fireEvent.click(screen.getByText("Make glucose"));
    fireEvent.click(screen.getByText("Submit Answer"));

    await waitFor(() => {
      expect(screen.getByText("Explanation")).toBeTruthy();
      expect(screen.getByText("Photosynthesis helps plants make glucose.")).toBeTruthy();
    });
  });
});
