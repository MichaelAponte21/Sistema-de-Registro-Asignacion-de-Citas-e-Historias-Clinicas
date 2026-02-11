import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

export default function MisCitas() {
  const navigate = useNavigate();
  const [citas, setCitas] = useState([]);

  useEffect(() => {
    setCitas(JSON.parse(localStorage.getItem("citas")) || []);
  }, []);

  const cancelarCita = (index) => {
    const updated = citas.filter((_, i) => i !== index);
    setCitas(updated);
    localStorage.setItem("citas", JSON.stringify(updated));
    alert("Cita cancelada");
  };

  return (
    <>
      <Navbar title="Mis Citas" />
      <div className="container">
        <h2>Listado de Citas</h2>
        {citas.length === 0 ? (
          <p>No tienes citas aún</p>
        ) : (
          citas.map((c, i) => (
            <div className="card" key={i}>
              <p>{c.fecha} - {c.hora} - {c.tipo}</p>
              <button onClick={() => cancelarCita(i)}>Cancelar</button>
            </div>
          ))
        )}
        <button onClick={() => navigate("/menu")}>Menú Principal</button>
      </div>
    </>
  );
}
