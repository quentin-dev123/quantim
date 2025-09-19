import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Home from "./pages/home.jsx";
import Login from "./pages/login.jsx";
import Register from "./pages/register.jsx";
import LoginPronote from "./pages/login_pronote.jsx";
import NotFound from "./pages/NotFound.jsx";


function About() {
  return <h1>About Page</h1>;
}

function Contact() {
  return <h1>Contact Page</h1>;
}

export default function App() {
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
        <Route path="*" element={<NotFound />} /> {/* Catch-all route for undefined paths */}
      </Routes>
    </BrowserRouter>
  );
}