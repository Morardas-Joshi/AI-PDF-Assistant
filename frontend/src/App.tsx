import { Navigate, Route, Routes } from "react-router-dom";

import { DashboardPage } from "./pages/DashboardPage";
import { AppShell } from "./layouts/AppShell";

export function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<DashboardPage />} />
        <Route path="documents" element={<DashboardPage />} />
        <Route path="chat" element={<DashboardPage />} />
        <Route path="search" element={<DashboardPage />} />
        <Route path="settings" element={<DashboardPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

