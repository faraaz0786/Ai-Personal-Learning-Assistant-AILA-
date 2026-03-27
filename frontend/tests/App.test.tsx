import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import { HomePage } from "../src/pages/HomePage";

test("renders landing headline", () => {
  render(
    <MemoryRouter>
      <HomePage />
    </MemoryRouter>
  );

  expect(screen.getByText("Learn anything, faster.")).toBeTruthy();
});
