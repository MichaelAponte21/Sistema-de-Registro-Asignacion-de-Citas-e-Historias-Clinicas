// src/paginas/LoginUsuario.jsx
import { useState } from "react";
import api from "../api/api";
import { useNavigate } from "react-router-dom";

export default function LoginUsuario() {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const manejarLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const params = new URLSearchParams();
      params.append("username", correo);
      params.append("password", password);

      const res = await api.post("/api/auth/token", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      // guardar token
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("rol", res.data.role);

      // redirección
      if (res.data.role === "doctor") navigate("/medico");
      else navigate("/usuario");

    } catch (err) {
      console.log(err);
      setError("Credenciales incorrectas");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#e3f2fd",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "20px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "420px",
          background: "white",
          padding: "35px",
          borderRadius: "15px",
          boxShadow: "0px 4px 20px rgba(0,0,0,0.15)",
        }}
      >
        <h1
          style={{
            textAlign: "center",
            fontSize: "28px",
            fontWeight: "bold",
            marginBottom: "25px",
            color: "#0d47a1",
          }}
        >
          Iniciar Sesión
        </h1>

        <form
          onSubmit={manejarLogin}
          style={{ display: "flex", flexDirection: "column", gap: "18px" }}
        >
          <div>
            <label style={{ color: "#0d47a1", fontWeight: "bold" }}>
              Correo
            </label>
            <input
              type="email"
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              placeholder="usuario@ejemplo.com"
              style={{
                width: "100%",
                boxSizing: "border-box",
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #90caf9",
              }}
              required
            />
          </div>

          <div>
            <label style={{ color: "#0d47a1", fontWeight: "bold" }}>
              Contraseña
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Ingrese su contraseña"
              style={{
                width: "100%",
                boxSizing: "border-box",
                padding: "12px",
                borderRadius: "8px",
                border: "1px solid #90caf9",
              }}
              required
            />
          </div>

          {error && (
            <p
              style={{
                color: "red",
                textAlign: "center",
                fontWeight: "bold",
              }}
            >
              {error}
            </p>
          )}

          <button
            type="submit"
            style={{
              background: "#0d47a1",
              color: "white",
              padding: "14px",
              border: "none",
              borderRadius: "10px",
              fontSize: "18px",
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            Entrar
          </button>
        </form>
      </div>
    </div>
  );
}
