// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginUsuario from "./paginas/LoginUsuario";
import LoginMedico from "./paginas/medico/LoginMedico";
import MedicoRouter from "./routes/MedicoRouter";

// Ruta protegida real del backend
function ProtectedRoute({ children, allow }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role"); // "admin" | "doctor" | "patient"

  if (!token) return <Navigate to="/" replace />;

  // Si se exige un rol específico
  if (allow && !allow.includes(role)) return <Navigate to="/" replace />;

  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Login general */}
        <Route path="/" element={<LoginUsuario />} />

        {/* Dashboard médico */}
        <Route
          path="/medico"
          element={
            <ProtectedRoute allow={["doctor"]}>
              <LoginMedico />
            </ProtectedRoute>
          }
        />

        {/* Subrutas reales del médico */}
        <Route
          path="/medico/*"
          element={
            <ProtectedRoute allow={["doctor"]}>
              <MedicoRouter />
            </ProtectedRoute>
          }
        />

        {/* Rutas inválidas */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
