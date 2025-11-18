import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ correo: "", clave: "" });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleLogin = () => {
  if (!form.correo || !form.clave) {
    alert("Todos los campos son obligatorios");
    return;
  }

  const storedUsers = JSON.parse(localStorage.getItem("pacientes")) || [];
  const user = storedUsers.find(
    u => u.correo === form.correo && u.clave === form.clave
  );

  if (!user) return alert("Credenciales incorrectas");

  localStorage.setItem("usuarioActual", JSON.stringify(user));
  navigate("/menu");
};


  return (
    <>
      <Navbar title="Inicio de Sesión" />
      <div className="container">
        <h2>Ingresar</h2>
        <input name="correo" placeholder="Correo" onChange={handleChange} />
        <input type="password" name="clave" placeholder="Clave" onChange={handleChange} />
        <button onClick={handleLogin}>Ingresar</button>
        <button onClick={() => navigate("/register")}>
          Registrarse
        </button>
      </div>
    </>
  );
}
