import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api"; // RUTA CORRECTA A api.js

export default function AgendarCitas() {
  const navigate = useNavigate();
  const [citas, setCitas] = useState([]);
  const [form, setForm] = useState({
    patient_id: "",
    fecha: "",
    hora: "",
    motivo: "",
  });

  // ===============================================
  // 1. CARGAR CITAS DEL MÉDICO LOGUEADO
  // ===============================================
  const cargarCitas = async () => {
    try {
      const res = await api.get("/appointments/");
      setCitas(res.data);
    } catch (err) {
      console.error("Error cargando citas:", err);
      alert("⚠️ No se pudieron cargar las citas.");
    }
  };

  useEffect(() => {
    cargarCitas();
  }, []);

  // ===============================================
  // Manejo del formulario
  // ===============================================
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  // ===============================================
  // 2. CREAR CITA
  // ===============================================
  const crearCita = async (e) => {
    e.preventDefault();

    if (!form.patient_id || !form.fecha || !form.hora) {
      alert("⚠️ Complete todos los campos obligatorios.");
      return;
    }

    const scheduled_at = `${form.fecha}T${form.hora}:00`;

    try {
      const body = {
        patient_id: Number(form.patient_id),
        scheduled_at,
        reason: form.motivo,
      };

      await api.post("/appointments/", body);

      alert("✅ Cita creada correctamente");

      setForm({
        patient_id: "",
        fecha: "",
        hora: "",
        motivo: "",
      });

      cargarCitas();
    } catch (err) {
      console.error("Error creando cita:", err);
      alert("⚠️ Error al crear la cita.");
    }
  };

  // ===============================================
  // 3. CANCELAR CITA
  // ===============================================
  const cancelarCita = async (id) => {
    if (!confirm("¿Seguro que deseas cancelar esta cita?")) return;

    try {
      await api.post(`/appointments/${id}/cancel`);
      alert("✅ Cita cancelada");
      cargarCitas();
    } catch (err) {
      console.error("Error cancelando cita:", err);
      alert("⚠️ No se pudo cancelar la cita.");
    }
  };

  // ===============================================
  // Render
  // ===============================================
  return (
    <div style={{ padding: "40px" }}>
      <h1 style={{ color: "#1565c0" }}>Agendar Citas</h1>
      <p>Puedes crear, consultar y cancelar citas.</p>

      {/* Formulario */}
      <div
        style={{
          background: "#f4f9ff",
          padding: "20px",
          borderRadius: "10px",
          border: "1px solid #d0e3ff",
          width: "420px",
          marginBottom: "30px",
        }}
      >
        <h3 style={{ marginBottom: "15px", color: "#0d47a1" }}>
          Crear nueva cita
        </h3>

        <form onSubmit={crearCita}>
          <label>ID Paciente:</label>
          <input
            type="text"
            name="patient_id"
            value={form.patient_id}
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
              cursor: "pointer",
            }}
          >
            Crear cita
          </button>
        </form>
      </div>

      {/* Listado */}
      <h3 style={{ color: "#0d47a1", marginBottom: "10px" }}>
        Citas programadas
      </h3>

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
          {citas.map((cita) => {
            const fecha = cita.scheduled_at?.split("T")[0];
            const hora = cita.scheduled_at?.split("T")[1]?.substring(0, 5);

            return (
              <tr key={cita.id} style={{ borderBottom: "1px solid #ddd" }}>
                <td style={{ padding: 10 }}>{cita.patient_id}</td>
                <td style={{ padding: 10 }}>{fecha}</td>
                <td style={{ padding: 10 }}>{hora}</td>
                <td style={{ padding: 10 }}>{cita.reason}</td>

                <td style={{ padding: 10, display: "flex", gap: "8px" }}>
                  <button
                    onClick={() =>
                      navigate(`/medico/registrar-consulta?id=${cita.id}`)
                    }
                    style={{
                      padding: "5px 10px",
                      background: "#2e7d32",
                      color: "white",
                      border: "none",
                      borderRadius: "5px",
                      cursor: "pointer",
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
                      cursor: "pointer",
                    }}
                  >
                    Cancelar
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
