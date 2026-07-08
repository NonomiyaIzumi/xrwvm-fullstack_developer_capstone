import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../api.js";

export default function Login({ setUser }) {
  const navigate = useNavigate();
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    const result = await login(userName, password);
    if (result.status === "Authenticated") {
      setUser({ isAuthenticated: true, username: result.userName });
      navigate("/");
    } else {
      setError("Invalid username or password.");
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          Username
          <input value={userName} onChange={(event) => setUserName(event.target.value)} required />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
        </label>
        <button type="submit" className="btn-primary">Login</button>
        {error && <p className="error-text">{error}</p>}
      </form>
    </div>
  );
}
