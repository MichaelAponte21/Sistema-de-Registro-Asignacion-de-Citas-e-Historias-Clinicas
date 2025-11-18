import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function PatientMenu() {
  const navigate = useNavigate();

  return (
    <>
      <Navbar title="Menú Paciente" />
      <div className="container">
        <button onClick={() => navigate("/agendar")}>Agendar Cita</button>
        <button onClick={() => navigate("/citas")}>Mis Citas</button>
        <button onClick={() => navigate("/historia")}>Historia Clínica</button>
      </div>
    </>
  );
}
