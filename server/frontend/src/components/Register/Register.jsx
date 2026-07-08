import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../../api.js";

export default function Register({ setUser }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    userName: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const result = await register(form);
    if (result.status === "Authenticated") {
      setUser({ isAuthenticated: true, username: result.userName });
      navigate("/");
    } else {
      setError(result.error || "Registration failed.");
    }
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          Username
          <input name="userName" value={form.userName} onChange={handleChange} required />
        </label>
        <label>
          First Name
          <input name="firstName" value={form.firstName} onChange={handleChange} required />
        </label>
        <label>
          Last Name
          <input name="lastName" value={form.lastName} onChange={handleChange} required />
        </label>
        <label>
          Email
          <input type="email" name="email" value={form.email} onChange={handleChange} required />
        </label>
        <label>
          Password
          <input type="password" name="password" value={form.password} onChange={handleChange} required />
        </label>
        <button type="submit" className="btn-primary">Register</button>
        {error && <p className="error-text">{error}</p>}
      </form>
    </div>
  );
}
