// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginUsuario from "./paginas/LoginUsuario";
import LoginMedico from "./paginas/medico/LoginMedico";
import MedicoRouter from "./routes/MedicoRouter";
import AgendarCitas from "./paginas/medico/AgendaCitas"
import DatosPaciente from "./paginas/medico/DatosPaciente"
import RegistrarConsulta from "./paginas/medico/RegistrarConsulta"

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
        <Route path="/" element={<RegistrarConsulta />} />

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
