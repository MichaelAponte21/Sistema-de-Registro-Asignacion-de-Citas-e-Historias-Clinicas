// src/routes/MedicoRouter.jsx
import { Routes, Route, Navigate } from "react-router-dom";

import AgendarCitas from "../paginas/medico/AgendaCitas";
import DatosPaciente from "../paginas/medico/DatosPaciente";
import RegistrarConsulta from "../paginas/medico/RegistrarConsulta";

export default function MedicoRouter() {
  return (
    <Routes>
      <Route path="citas" element={<AgendarCitas />} />
      <Route path="datos-paciente" element={<DatosPaciente />} />
      <Route path="registrar-consulta" element={<RegistrarConsulta />} />

      {/* Ruta por defecto */}
      <Route path="*" element={<Navigate to="/medico" />} />
    </Routes>
  );
}
