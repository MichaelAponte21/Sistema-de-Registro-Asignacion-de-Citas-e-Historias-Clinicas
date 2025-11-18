// src/pages/medico/RegistrarConsulta.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const RegistrarConsulta = () => {
  const navigate = useNavigate();

  // Estado del formulario
  const [form, setForm] = useState({
    motivo: "",
    sintomas: "",
    diagnostico: "",
    tratamiento: "",
    observaciones: "",
  });

  // Manejar cambios en los inputs
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  // Simulación de submit (más adelante lo conectamos al backend)
  const handleSubmit = (e) => {
    e.preventDefault();

    console.log("Consulta registrada:", form);

    alert("Consulta registrada correctamente (modo demo)");

    // Regresa a DatosPaciente o a AgendarCitas
    navigate("/medico/agendar-citas");
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Registrar Consulta</h2>

      <form style={styles.form} onSubmit={handleSubmit}>
        <label style={styles.label}>Motivo de consulta:</label>
        <textarea
          name="motivo"
          value={form.motivo}
          onChange={handleChange}
          required
          style={styles.textarea}
        />

        <label style={styles.label}>Síntomas:</label>
        <textarea
          name="sintomas"
          value={form.sintomas}
          onChange={handleChange}
          required
          style={styles.textarea}
        />

        <label style={styles.label}>Diagnóstico:</label>
        <textarea
          name="diagnostico"
          value={form.diagnostico}
          onChange={handleChange}
          required
          style={styles.textarea}
        />

        <label style={styles.label}>Tratamiento:</label>
        <textarea
          name="tratamiento"
          value={form.tratamiento}
          onChange={handleChange}
          required
          style={styles.textarea}
        />

        <label style={styles.label}>Observaciones:</label>
        <textarea
          name="observaciones"
          value={form.observaciones}
          onChange={handleChange}
          style={styles.textarea}
        />

        <div style={styles.buttons}>
          <button
            type="button"
            style={styles.btnSecondary}
            onClick={() => navigate(-1)}
          >
            ← Volver
          </button>

          <button type="submit" style={styles.btnPrimary}>
            Guardar Consulta
          </button>
        </div>
      </form>
    </div>
  );
};

// ====== ESTILOS SIMPLES EN JS ======

const styles = {
  container: {
    padding: "30px",
    maxWidth: "700px",
    margin: "auto",
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  label: {
    fontWeight: "bold",
  },
  textarea: {
    minHeight: "80px",
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    resize: "vertical",
  },
  buttons: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "20px",
  },
  btnPrimary: {
    background: "#0d6efd",
    color: "#fff",
    padding: "10px 20px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
  btnSecondary: {
    background: "#ccc",
    padding: "10px 20px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
};

export default RegistrarConsulta;
