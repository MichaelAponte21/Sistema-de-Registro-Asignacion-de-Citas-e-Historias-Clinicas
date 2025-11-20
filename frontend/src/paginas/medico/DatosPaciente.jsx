import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../../api/api"; // ✔ Ruta correcta a api.js

export default function DatosPaciente() {
  const navigate = useNavigate();
  const location = useLocation();
  const query = new URLSearchParams(location.search);

  const patientId = query.get("id"); // ID del paciente desde la URL

  const [paciente, setPaciente] = useState(null);
  const [cargando, setCargando] = useState(true);

  // ===============================================
  // 1. Cargar datos reales del paciente
  // ===============================================
  const cargarPaciente = async () => {
    try {
      const res = await api.get(`/patients/${patientId}`);
      setPaciente(res.data);
    } catch (err) {
      console.error("Error cargando paciente:", err);
      alert("⚠️ No se pudieron cargar los datos del paciente.");
      navigate("/medico/citas"); // volver si falla
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    if (patientId) cargarPaciente();
  }, [patientId]);

  // ===============================================
  // Render: Cargando
  // ===============================================
  if (cargando) {
    return <p style={{ textAlign: "center", marginTop: "40px" }}>Cargando datos...</p>;
  }

  // ===============================================
  // Render: Si no existe paciente
  // ===============================================
  if (!paciente) {
    return (
      <div style={{ textAlign: "center", marginTop: "40px" }}>
        <h3>No se encontró el paciente</h3>
        <button onClick={() => navigate(-1)}>Volver</button>
      </div>
    );
  }

  // ===============================================
  // Render final con datos reales
  // ===============================================
  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Datos del Paciente</h2>

      <div style={styles.card}>
        <p><strong>Nombre:</strong> {paciente.name}</p>
        <p><strong>Cédula:</strong> {paciente.document_number}</p>
        <p><strong>Edad:</strong> {paciente.age} años</p>
        <p><strong>Teléfono:</strong> {paciente.phone}</p>
        <p><strong>Correo:</strong> {paciente.email}</p>
        <p><strong>Dirección:</strong> {paciente.address}</p>
        <p><strong>EPS:</strong> {paciente.eps}</p>
        <p><strong>Antecedentes:</strong> {paciente.medical_history || "No registrados"}</p>
      </div>

      <div style={styles.buttons}>
        <button style={styles.btn} onClick={() => navigate(-1)}>
          ← Volver
        </button>

        <button
          style={styles.btnPrimary}
          onClick={() =>
            navigate(`/medico/registrar-consulta?patient_id=${paciente.id}`)
          }
        >
          Registrar Consulta →
        </button>
      </div>
    </div>
  );
}

// =====================================================
// ESTILOS
// =====================================================

const styles = {
  container: {
    padding: "30px",
    maxWidth: "650px",
    margin: "auto",
    color: "#333",
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
    color: "#0d47a1",
  },
  card: {
    background: "#fff",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)",
    marginBottom: "20px",
    lineHeight: "1.7",
  },
  buttons: {
    display: "flex",
    justifyContent: "space-between",
  },
  btn: {
    background: "#ccc",
    padding: "10px 20px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
  btnPrimary: {
    background: "#0d6efd",
    color: "#fff",
    padding: "10px 20px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
};
