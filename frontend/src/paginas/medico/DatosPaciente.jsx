
import React from "react";
import { useNavigate } from "react-router-dom";

const DatosPaciente = () => {
  const navigate = useNavigate();

  //actualmente colocamos esto simulando un paciente

  const pacienteMock = {
    nombre: "Juan Pérez",
    cedula: "123456789",
    edad: 29,
    telefono: "3001234567",
    correo: "juan.perez@example.com",
    direccion: "Calle 45 # 12 - 31",
    eps: "Sanitas",
    antecedentes: "Sin antecedentes relevantes.",
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Datos del Paciente</h2>

      <div style={styles.card}>
        <p><strong>Nombre:</strong> {pacienteMock.nombre}</p>
        <p><strong>Cédula:</strong> {pacienteMock.cedula}</p>
        <p><strong>Edad:</strong> {pacienteMock.edad} años</p>
        <p><strong>Teléfono:</strong> {pacienteMock.telefono}</p>
        <p><strong>Correo:</strong> {pacienteMock.correo}</p>
        <p><strong>Dirección:</strong> {pacienteMock.direccion}</p>
        <p><strong>EPS:</strong> {pacienteMock.eps}</p>
        <p><strong>Antecedentes:</strong> {pacienteMock.antecedentes}</p>
      </div>

      <div style={styles.buttons}>
        <button style={styles.btn} onClick={() => navigate(-1)}>
          ← Volver
        </button>
        <button
          style={styles.btnPrimary}
          onClick={() => navigate("/medico/registrar-consulta")}
        >
          Registrar Consulta →
        </button>
      </div>
    </div>
  );
};

// ==== ESTILOS EN JS PARA SIMPLICIDAD ====

const styles = {
  container: {
    padding: "30px",
    maxWidth: "600px",
    margin: "auto",
    color: "#333",
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
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

export default DatosPaciente;
