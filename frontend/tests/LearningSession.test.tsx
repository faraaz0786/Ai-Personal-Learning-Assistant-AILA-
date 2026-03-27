import { fireEvent, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import { LearningSession } from "../src/components/organisms/LearningSession";
import { useQuizStore } from "../src/store/quizStore";
import { renderWithProviders } from "./test-utils";

vi.mock("../src/api/learning", () => ({
  explainTopic: vi.fn(async () => ({
    topic_id: "topic-1",
    normalized_topic: "Photosynthesis",
    explanation: {
      definition: "Plants convert light into usable energy through photosynthesis.",
      mechanism:
        "Chlorophyll captures sunlight and supports reactions that transform water and carbon dioxide into glucose and oxygen.",
      example:
        "A sunflower leaf uses sunlight, water, and carbon dioxide to create glucose for growth."
    },
    summary:
      "Photosynthesis allows plants to turn sunlight into stored energy. It happens mainly in chloroplasts, where water and carbon dioxide are transformed into glucose and oxygen. This process supports plant growth and contributes oxygen to the atmosphere. It is a core biology concept for understanding energy in living systems.",
    cached: false,
    response_ms: 1200
  })),
  generateQuiz: vi.fn(async () => ({
    quiz_id: "quiz-1",
    topic_id: "topic-1",
    questions: []
  }))
}));

describe("LearningSession", () => {
  beforeEach(() => {
    useQuizStore.getState().resetQuiz();
  });

  test("shows inline validation for short topic input", async () => {
    renderWithProviders(<LearningSession />);

    fireEvent.change(screen.getByPlaceholderText("Enter a topic or question..."), {
      target: { value: "AI" }
    });
    fireEvent.click(screen.getByText("Explain This"));

    expect(screen.getByText("Please enter at least 3 characters.")).toBeTruthy();
  });

  test("renders explanation and summary after successful submission", async () => {
    renderWithProviders(<LearningSession />);

    fireEvent.change(screen.getByPlaceholderText("Enter a topic or question..."), {
      target: { value: "Photosynthesis" }
    });
    fireEvent.click(screen.getByText("Explain This"));

    await waitFor(() => {
      expect(screen.getByText("Photosynthesis")).toBeTruthy();
      expect(screen.getByText(/Revision summary/i)).toBeTruthy();
    });
  });
});
