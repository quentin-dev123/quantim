import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import "./style/hide.css";
import useImportCSS from './modules/useImportCSS.js';
import Home from "./pages/home.jsx";
import Login from "./pages/login.jsx";
import Register from "./pages/register.jsx";
import LoginPronote from "./pages/login_pronote.jsx";
import NotFound from "./pages/NotFound.jsx";
import Agenda from './pages/agenda.jsx';
import RequireAuth from './modules/loginMangement.jsx';


function About() {
  return <h1>About Page</h1>;
}

function Contact() {
  return <h1>Contact Page</h1>;
}

export default function App() {
  useImportCSS("https://fonts.googleapis.com/icon?family=Material+Icons");
  useImportCSS(
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
    "sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==",
    "anonymous",
    "no-referrer"
  );
  return (
    <BrowserRouter>
      {/* Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/fetch_pronote" element={<LoginPronote />} />
        <Route path="/agenda" element={<RequireAuth><Agenda /></RequireAuth>} />
        <Route path="*" element={<NotFound />} /> {/* Catch-all route for undefined paths */}
      </Routes>
    </BrowserRouter>
  );
}