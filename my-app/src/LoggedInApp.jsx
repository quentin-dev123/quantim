import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'
import {login} from "./redux/reducers/authSlice";
import { useState} from "react";

function Login() {
  const [password, setPassword] = useState("")
  const key = useSelector(state => state.auth.key)
  const dispatch = useDispatch()
  return <>
  <h1>Enter password</h1>
  <input onChange={(e) => setPassword(e.target.value)}/>
  <button onClick={() => dispatch(login(password))}>Submit</button>
  <p>{key}</p>
  </>;
}

function Contact() {
  const key = useSelector(state => state.auth.key)
  return <h1>Contact Page, {key}</h1>;
}

export default function LoggedInApp() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
    </BrowserRouter>
  );
}