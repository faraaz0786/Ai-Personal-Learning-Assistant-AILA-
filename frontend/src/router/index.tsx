import { BrowserRouter, Route, Routes } from "react-router-dom";

import { AppBootstrap } from "../app/AppBootstrap";
import { AppShell } from "../app/AppShell";
import { HomePage } from "../pages/HomePage";
import { LearnPage } from "../pages/LearnPage";
import { QuizPage } from "../pages/QuizPage";
import { QuizResultsPage } from "../pages/QuizResultsPage";
import { LibraryPage } from "../pages/LibraryPage";
import { CoursesPage } from "../pages/CoursesPage";

export function AppRouter() {
  return (
    <BrowserRouter>
      <AppBootstrap>
        <AppShell>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/learn" element={<LearnPage />} />
            <Route path="/quiz" element={<QuizPage />} />
            <Route path="/quiz/results" element={<QuizResultsPage />} />
            <Route path="/library" element={<LibraryPage />} />
            <Route path="/courses" element={<CoursesPage />} />
          </Routes>
        </AppShell>
      </AppBootstrap>
    </BrowserRouter>
  );
}
