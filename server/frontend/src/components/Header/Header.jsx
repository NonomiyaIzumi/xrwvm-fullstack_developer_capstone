import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { logout as apiLogout } from "../../api.js";

export default function Header({ user, setUser }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await apiLogout();
    setUser({ isAuthenticated: false, username: "" });
    navigate("/");
  };

  return (
    <header className="navbar">
      <Link className="brand" to="/">Cars Dealership</Link>
      <nav>
        <Link to="/">Home</Link>
        <a href="/static/About.html">About Us</a>
        <a href="/static/Contact.html">Contact Us</a>
        {user.isAuthenticated ? (
          <>
            <span data-testid="logged-in-username">Hi, {user.username}</span>
            <a href="#logout" onClick={(event) => { event.preventDefault(); handleLogout(); }}>
              Logout
            </a>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Sign Up</Link>
          </>
        )}
      </nav>
    </header>
  );
}
