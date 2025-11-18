// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginUsuario from "./LoginUsuario";
import LoginMedico from "./paginas/medico/LoginMedico";
import MedicoRouter from "./routes/MedicoRouter";

// Protege rutas según token + rol
function ProtectedRoute({ children, rol }) {
  const token = localStorage.getItem("token");
  const userRol = localStorage.getItem("rol");

  if (!token) return <Navigate to="/" />;
  if (rol && rol !== userRol) return <Navigate to="/" />;

  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Login principal */}
        <Route path="/" element={<LoginUsuario />} />

        {/* Dashboard del médico */}
        <Route
          path="/medico"
          element={
            <ProtectedRoute rol="MEDICO">
              <LoginMedico />
            </ProtectedRoute>
          }
        />

        {/* Subrutas del médico */}
        <Route
          path="/medico/*"
          element={
            <ProtectedRoute rol="MEDICO">
              <MedicoRouter />
            </ProtectedRoute>
          }
        />

        {/* Cualquier ruta inválida */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}
