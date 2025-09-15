import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Login from "./pages/login.jsx";
import Home from "./pages/home.jsx";
import NotFound from "./pages/404.jsx";


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
        <Route path="/home" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<NotFound />} /> {/* Catch-all route for undefined paths */}
      </Routes>
    </BrowserRouter>
  );
}