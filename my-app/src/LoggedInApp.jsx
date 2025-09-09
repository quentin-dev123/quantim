import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux'
import {login} from "./redux/reducers/authSlice";

function Login() {
  const dispatch = useDispatch()
  return <>
  <h1>Enter password</h1>
  <input onChange={(e) => {dispatch(login(e.target.value))}}/>
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