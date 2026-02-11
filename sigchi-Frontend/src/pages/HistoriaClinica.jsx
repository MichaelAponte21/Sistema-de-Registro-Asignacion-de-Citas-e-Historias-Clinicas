import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";

export default function HistoriaClinica() {
  const navigate = useNavigate();
  const usuario = JSON.parse(localStorage.getItem("usuarioActual"));

  const historia = JSON.parse(localStorage.getItem("historiaClinica")) || {};

  return (
    <>
      <Navbar title="Historia Clínica" />
      <div className="container">
        <h2>Historia Clínica</h2>

        {historia[usuario.correo]?.length > 0 ? (
          historia[usuario.correo].map((item, i) => (
            <div className="card" key={i}>
              <p><strong>Fecha:</strong> {item.fecha}</p>
              <p><strong>Diagnóstico:</strong> {item.diagnostico}</p>
            </div>
          ))
        ) : (
          <p>No hay registros médicos disponibles.</p>
        )}

        <button onClick={() => navigate("/menu")}>Menú Principal</button>
      </div>
    </>
  );
}
