import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "../pages/Home/Home";
import Login from "../pages/Login/Login";
import Register from "../pages/Register/Register";
import Dashboard from "../pages/Dashboard/Dashboard";
import UploadDocuments from "../pages/UploadDocuments/UploadDocuments";
import Recommendations from "../pages/Recommendations/Recommendations";
import AIProcessing from "../pages/AIProcessing/AIProcessing";
import ApplicationReview from "../pages/ApplicationReview/ApplicationReview";
import Notifications from "../pages/Notifications/Notifications";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route
  path="/upload-documents"
  element={<UploadDocuments />}
/>

<Route
  path="/recommendations"
  element={<Recommendations />}
/>
<Route
    path="/processing"
    element={<AIProcessing />}
/>
<Route
  path="/application-review"
  element={<ApplicationReview />}
/>
<Route
  path="/notifications"
  element={<Notifications />}
/>

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;