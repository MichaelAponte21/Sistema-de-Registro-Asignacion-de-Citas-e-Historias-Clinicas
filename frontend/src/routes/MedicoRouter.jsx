import { Routes, Route, Navigate } from "react-router-dom";

import AgendarCitas from "../paginas/medico/AgendaCitas";
import DatosPaciente from "../paginas/medico/DatosPaciente";
import RegistrarConsulta from "../paginas/medico/RegistrarConsulta";

// Validación de autenticación
const isAuthenticated = () => {
  return (
    localStorage.getItem("token") !== null &&
    localStorage.getItem("rol") === "MEDICO"
  );
};

// Protege rutas del médico
const RutaProtegidaMedico = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/" replace />;
};

export default function MedicoRouter() {
  return (
    <Routes>
      <Route
        path="citas"
        element={
          <RutaProtegidaMedico>
            <AgendarCitas />
          </RutaProtegidaMedico>
        }
      />

      <Route
        path="datos-paciente"
        element={
          <RutaProtegidaMedico>
            <DatosPaciente />
          </RutaProtegidaMedico>
        }
      />

      <Route
        path="registrar-consulta"
        element={
          <RutaProtegidaMedico>
            <RegistrarConsulta />
          </RutaProtegidaMedico>
        }
      />

      {/* Si la ruta no existe */}
      <Route path="*" element={<Navigate to="/medico" />} />
    </Routes>
  );
}
