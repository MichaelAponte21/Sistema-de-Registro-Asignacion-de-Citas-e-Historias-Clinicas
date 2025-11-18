import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function AgendarCita() {
  const navigate = useNavigate();
  const [cita, setCita] = useState({
    fecha: "",
    hora: "",
    tipo: ""
  });

  const handleAgendar = () => {
    const citas = JSON.parse(localStorage.getItem("citas")) || [];
    citas.push(cita);
    localStorage.setItem("citas", JSON.stringify(citas));
    alert("Cita Agendada");
  };




  return (
    <>
      <Navbar title="Agendar Cita" />
      <div className="container">
        <h2>Nueva Cita</h2>
        <input type="date" onChange={(e)=>setCita({ ...cita, fecha: e.target.value })} />
        <input type="time" onChange={(e)=>setCita({ ...cita, hora: e.target.value })} />
        <select onChange={(e)=>setCita({ ...cita, tipo: e.target.value })}>
          <option value="">Seleccione tipo</option>
          <option>General</option>
          <option>Odontológica</option>
          <option>Exámenes</option>
        </select>
        <button onClick={handleAgendar}>Agendar</button>
        <button onClick={() => navigate("/menu")}>Menú Principal</button>
        
      </div>
    </>
  );
}
