import { Navigate, useLocation } from "react-router-dom";

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function checkForAuthCookie() {
    const cookie = getCookie("authenticated")
    console.log(cookie)
    console.log(typeof(cookie))
    return cookie === "true";
}

export default function RequireAuth({ children }) {
  const isAuthenticated = checkForAuthCookie(); // Your auth check logic

  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect to login page and save current location so user can be redirected back after login
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children; // Render the protected content if authenticated
}