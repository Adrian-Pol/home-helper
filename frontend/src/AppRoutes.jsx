import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import routes from "./routes/Index";

function AppRoutes() {
  const renderRoutes = (routesArray) =>
    routesArray.map((r) => (
      <Route key={r.path || "home"} path={r.path} element={r.element}>
        {r.children && renderRoutes(r.children)}
      </Route>
    ));

  return (
    <Router>
      <Routes>{renderRoutes(routes)}</Routes>
    </Router>
  );
}

export default AppRoutes;
