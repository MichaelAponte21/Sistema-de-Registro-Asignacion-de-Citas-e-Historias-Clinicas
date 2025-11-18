import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

const LoginUsuario = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const iniciarSesion = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await api.post("/auth/login", {
        username: form.username,
        password: form.password,
      });

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("rol", res.data.rol);

      // REDIRECCIÓN SEGÚN ROL
      if (res.data.rol === "MEDICO") {
        navigate("/medico");
      } else if (res.data.rol === "ADMIN") {
        navigate("/admin");
      } else {
        navigate("/usuario");
      }

    } catch (error) {
      console.log(error);
      setError("Credenciales incorrectas");
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Iniciar Sesión</h2>

      <form onSubmit={iniciarSesion}>
        <input
          type="text"
          name="username"
          placeholder="Usuario"
          onChange={handleChange}
        />
        <br />
        <input
          type="password"
          name="password"
          placeholder="Contraseña"
          onChange={handleChange}
        />
        <br />
        <button type="submit">Ingresar</button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default LoginUsuario;
