import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    nombre: "",
    correo: "",
    clave: ""
  });

  const handleRegister = () => {
    let pacientes = JSON.parse(localStorage.getItem("pacientes")) || [];
    pacientes.push(form);
    localStorage.setItem("pacientes", JSON.stringify(pacientes));
    alert("Paciente registrado");
    navigate("/");
  };
  if (!form.nombre || !form.correo || !form.clave) {
  alert("Todos los campos son obligatorios");
  return;
}

const usuarios = JSON.parse(localStorage.getItem("pacientes")) || [];
const existe = usuarios.some(u => u.correo === form.correo);

if (existe) {
  alert("Este correo ya está registrado");
  return;
}


  return (
    <>
      <Navbar title="Registro" />
      <div className="container">
        <h2>Crear Cuenta</h2>
        <input placeholder="Nombre" onChange={(e)=>setForm({ ...form, nombre: e.target.value })} />
        <input placeholder="Correo" onChange={(e)=>setForm({ ...form, correo: e.target.value })}/>
        <input type="password" placeholder="Contraseña" onChange={(e)=>setForm({ ...form, clave: e.target.value })}/>
        <button onClick={handleRegister}>Registrar</button>
      </div>
    </>
  );
  
}
