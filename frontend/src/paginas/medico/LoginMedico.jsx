// src/paginas/medico/LoginMedico.jsx
import { useNavigate } from "react-router-dom";

export default function LoginMedico() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("rol");
    navigate("/");
  };

  return (
    <div style={{ padding: "30px", background: "#f4f8ff", minHeight: "100vh" }}>
      {/* Header */}
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "10px 20px",
          background: "#0d47a1",
          color: "white",
          borderRadius: "8px",
        }}
      >
        <h2>Panel del Médico</h2>

        <button
          onClick={logout}
          style={{
            background: "#e53935",
            color: "white",
            border: "none",
            padding: "10px 15px",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Cerrar sesión
        </button>
      </header>

      {/* Opciones */}
      <div style={{ marginTop: "40px" }}>
        <h3>Bienvenido Doctor</h3>
        <p>Seleccione la opción que desea realizar:</p>

        <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
          <button
            onClick={() => navigate("/medico/citas")}
            style={{
              background: "#1565c0",
              color: "white",
              padding: "15px 20px",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
            }}
          >
            📅 Agendar / Ver Citas
          </button>

          <button
            onClick={() => navigate("/medico/registrar-consulta")}
            style={{
              background: "#1976d2",
              color: "white",
              padding: "15px 20px",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
            }}
          >
            📝 Registrar Consulta
          </button>

          <button
            onClick={() => navigate("/medico/datos-paciente")}
            style={{
              background: "#1e88e5",
              color: "white",
              padding: "15px 20px",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
            }}
          >
            👤 Datos del Paciente
          </button>
        </div>
      </div>
    </div>
  );
}
