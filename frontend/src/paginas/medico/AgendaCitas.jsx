import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AgendarCitas() {
  const navigate = useNavigate();
  const [citas, setCitas] = useState([]);
  const [form, setForm] = useState({
    pacienteId: "",
    fecha: "",
    hora: "",
    motivo: "",
  });

  // --------------------------
  // Cargar citas (simulado)
  // --------------------------
  useEffect(() => {
    // fetch("http://localhost:8000/citas")
    setCitas([
      { id: 1, paciente: "Carlos López", fecha: "2025-01-20", hora: "10:00 AM", motivo: "Chequeo general" },
      { id: 2, paciente: "Ana Torres", fecha: "2025-01-22", hora: "02:00 PM", motivo: "Dolor de cabeza" },
    ]);
  }, []);

  // --------------------------
  // Manejar cambios del form
  // --------------------------
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  // --------------------------
  // Crear cita
  // --------------------------
  const crearCita = async (e) => {
    e.preventDefault();

    if (!form.pacienteId || !form.fecha || !form.hora || !form.motivo) {
      alert("Por favor complete todos los campos");
      return;
    }

    const nueva = {
      id: citas.length + 1,
      paciente: `Paciente #${form.pacienteId}`,
      fecha: form.fecha,
      hora: form.hora,
      motivo: form.motivo,
    };

    setCitas([...citas, nueva]);

    // Vaciar form
    setForm({
      pacienteId: "",
      fecha: "",
      hora: "",
      motivo: "",
    });

    alert("Cita creada con éxito");
  };

  // --------------------------
  // Cancelar cita
  // --------------------------
  const cancelarCita = (id) => {
    const filtradas = citas.filter(c => c.id !== id);
    setCitas(filtradas);
  };

  return (
    <div style={{ padding: "40px" }}>

      <h1 style={{ color: "#1565c0" }}>Agendar Citas</h1>
      <p>Desde aquí puede crear, consultar y cancelar citas.</p>

      {/* ---------------------- FORMULARIO ---------------------- */}
      <div style={{
        background: "#f4f9ff",
        padding: "20px",
        borderRadius: "10px",
        border: "1px solid #d0e3ff",
        width: "400px",
        marginBottom: "30px"
      }}>
        <h3 style={{ marginBottom: "15px", color: "#0d47a1" }}>Crear nueva cita</h3>

        <form onSubmit={crearCita}>
          <label>ID Paciente:</label>
          <input
            type="text"
            name="pacienteId"
            value={form.pacienteId}
            onChange={handleChange}
            style={{ width: "100%", marginBottom: 10, padding: 8 }}
          />

          <label>Fecha:</label>
          <input
            type="date"
            name="fecha"
            value={form.fecha}
            onChange={handleChange}
            style={{ width: "100%", marginBottom: 10, padding: 8 }}
          />

          <label>Hora:</label>
          <input
            type="time"
            name="hora"
            value={form.hora}
            onChange={handleChange}
            style={{ width: "100%", marginBottom: 10, padding: 8 }}
          />

          <label>Motivo:</label>
          <input
            type="text"
            name="motivo"
            value={form.motivo}
            onChange={handleChange}
            style={{ width: "100%", marginBottom: 15, padding: 8 }}
          />

          <button
            type="submit"
            style={{
              width: "100%",
              padding: "10px",
              background: "#1e88e5",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer"
            }}
          >
            Crear cita
          </button>
        </form>
      </div>

      {/* ---------------------- LISTADO DE CITAS ---------------------- */}
      <h3 style={{ color: "#0d47a1", marginBottom: "10px" }}>Citas programadas</h3>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#e3f2fd", textAlign: "left" }}>
            <th style={{ padding: 10 }}>Paciente</th>
            <th style={{ padding: 10 }}>Fecha</th>
            <th style={{ padding: 10 }}>Hora</th>
            <th style={{ padding: 10 }}>Motivo</th>
            <th style={{ padding: 10 }}>Acciones</th>
          </tr>
        </thead>

        <tbody>
          {citas.map(cita => (
            <tr key={cita.id} style={{ borderBottom: "1px solid #ddd" }}>
              <td style={{ padding: 10 }}>{cita.paciente}</td>
              <td style={{ padding: 10 }}>{cita.fecha}</td>
              <td style={{ padding: 10 }}>{cita.hora}</td>
              <td style={{ padding: 10 }}>{cita.motivo}</td>

              <td style={{ padding: 10, display: "flex", gap: "8px" }}>
                <button
                  onClick={() => navigate(`/medico/registrar-consulta?id=${cita.id}`)}
                  style={{
                    padding: "5px 10px",
                    background: "#2e7d32",
                    color: "white",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer"
                  }}
                >
                  Registrar
                </button>

                <button
                  onClick={() => cancelarCita(cita.id)}
                  style={{
                    padding: "5px 10px",
                    background: "#c62828",
                    color: "white",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer"
                  }}
                >
                  Cancelar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  );
}
