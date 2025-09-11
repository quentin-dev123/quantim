import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Login from "./pages/login.jsx";

function Home() {
  return <>
  <h1>Home Page</h1>
  <Link to="/login">Login</Link>
  <p> Hello</p>
  </>;
}

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
      </Routes>
    </BrowserRouter>
  );
}