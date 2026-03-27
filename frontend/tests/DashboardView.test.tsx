import { screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import { DashboardView } from "../src/modules/dashboard/DashboardView";
import { renderWithProviders } from "./test-utils";

vi.mock("../src/api/progress", () => ({
  getProgressSummary: vi.fn(async () => ({
    topics_studied: 2,
    average_score: 84,
    streak_days: 3
  })),
  getProgressHistory: vi.fn(async () => [
    {
      topic: "Photosynthesis",
      score: 80,
      attempted_at: "2026-03-20T00:00:00+00:00"
    }
  ]),
  getProgressRecommendations: vi.fn(async () => [
    {
      topic: "Advanced Photosynthesis",
      reason: "You are ready for a deeper follow-up topic.",
      type: "advanced"
    }
  ])
}));

describe("DashboardView", () => {
  test("renders dashboard data when progress exists", async () => {
    renderWithProviders(<DashboardView />);

    await waitFor(() => {
      expect(screen.getByText("Total Topics Studied")).toBeTruthy();
      expect(screen.getByText("Advanced Photosynthesis")).toBeTruthy();
    });
  });
});
