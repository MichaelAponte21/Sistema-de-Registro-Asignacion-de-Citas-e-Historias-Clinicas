import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiPrivate from "../../api/api"; // ⬅️ IMPORTANTE: conectar al backend

const RegistrarConsulta = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    motivo: "",
    sintomas: "",
    diagnostico: "",
    tratamiento: "",
    observaciones: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // 📌 Enviar la consulta al backend
      const res = await apiPrivate.post("/consultas", form);

      alert("Consulta registrada correctamente");
      navigate("/medico/citas");
    } catch (error) {
      console.error("Error registrando consulta:", error);
      alert("Error al registrar la consulta");
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2 style={styles.title}>Registrar Consulta</h2>

        <form style={styles.form} onSubmit={handleSubmit}>
          <FormField
            label="Motivo de consulta"
            name="motivo"
            value={form.motivo}
            onChange={handleChange}
          />

          <FormField
            label="Síntomas"
            name="sintomas"
            value={form.sintomas}
            onChange={handleChange}
          />

          <FormField
            label="Diagnóstico"
            name="diagnostico"
            value={form.diagnostico}
            onChange={handleChange}
          />

          <FormField
            label="Tratamiento"
            name="tratamiento"
            value={form.tratamiento}
            onChange={handleChange}
          />

          <FormField
            label="Observaciones"
            name="observaciones"
            value={form.observaciones}
            onChange={handleChange}
            required={false}
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
    </div>
  );
};

// -------- COMPONENTE CAMPO --------
const FormField = ({ label, name, value, onChange, required = true }) => (
  <div style={{ display: "flex", flexDirection: "column" }}>
    <label style={styles.label}>{label}</label>
    <textarea
      name={name}
      value={value}
      onChange={onChange}
      required={required}
      style={styles.textarea}
    />
  </div>
);

// -------- ESTILOS --------
const styles = {
  page: {
    minHeight: "100vh",
    background: "#e9f0fb",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "30px",
  },
  card: {
    width: "100%",
    maxWidth: "700px",
    background: "white",
    padding: "30px",
    borderRadius: "12px",
    boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
    color: "#1a1a1a",
  },
  title: {
    textAlign: "center",
    marginBottom: "25px",
    color: "#0d47a1",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },
  label: {
    fontWeight: "bold",
    marginBottom: "5px",
    color: "#0d47a1",
  },
  textarea: {
    minHeight: "90px",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #b0bec5",
    resize: "vertical",
    fontSize: "15px",
    color: "#1a1a1a",
    background: "#f7f9fc",
  },
  buttons: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "15px",
  },
  btnPrimary: {
    background: "#0d47a1",
    color: "white",
    padding: "12px 25px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: "bold",
    transition: "0.2s",
  },
  btnSecondary: {
    background: "#cfd8dc",
    color: "#1a1a1a",
    padding: "12px 25px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    transition: "0.2s",
  },
};

export default RegistrarConsulta;
