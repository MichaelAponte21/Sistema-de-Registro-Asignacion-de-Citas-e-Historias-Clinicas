import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import PatientMenu from "./pages/PatientMenu";
import AgendarCita from "./pages/AgendarCita";
import MisCitas from "./pages/MisCitas";
import HistoriaClinica from "./pages/HistoriaClinica";
import "./index.css";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/menu" element={<PatientMenu />} />
        <Route path="/agendar" element={<AgendarCita />} />
        <Route path="/citas" element={<MisCitas />} />
        <Route path="/historia" element={<HistoriaClinica />} />
      </Routes>
    </BrowserRouter>
  );
}
