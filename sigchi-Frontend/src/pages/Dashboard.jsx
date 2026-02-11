import { Link, useNavigate } from "react-router-dom";

export default function Dashboard() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("auth");
    navigate("/");
  };

  return (
    <div className="container">
      <h2>Menú Paciente</h2>
      <ul>
        <li><Link to="/agendar">Agendar Cita</Link></li>
        <li><Link to="/mis-citas">Mis Citas</Link></li>
        <li><Link to="/historia">Historia Clínica</Link></li>
      </ul>
      <button onClick={logout}>Cerrar Sesión</button>
    </div>
  );
}
