import { Navigate, useLocation } from "react-router-dom";

function checkForAuthCookie() {
    
}

function RequireAuth({ children }) {
  const isAuthenticated = checkForAuthCookie(); // Your auth check logic

  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect to login page and save current location so user can be redirected back after login
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return children; // Render the protected content if authenticated
}