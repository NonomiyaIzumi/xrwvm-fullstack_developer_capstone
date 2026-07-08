import React, { useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Header from "./components/Header/Header.jsx";
import Footer from "./components/Footer/Footer.jsx";
import Home from "./components/Home/Home.jsx";
import Dealers from "./components/Dealers/Dealers.jsx";
import Dealer from "./components/Dealer/Dealer.jsx";
import PostReview from "./components/PostReview/PostReview.jsx";
import Login from "./components/Login/Login.jsx";
import Register from "./components/Register/Register.jsx";
import { getCurrentUser } from "./api.js";

export default function App() {
  const [user, setUser] = useState(getCurrentUser());

  return (
    <BrowserRouter>
      <Header user={user} setUser={setUser} />
      <main className="content">
        <Routes>
          <Route path="/" element={<Home user={user} />} />
          <Route path="/dealers" element={<Dealers user={user} />} />
          <Route path="/dealers/:state" element={<Dealers user={user} />} />
          <Route path="/dealer/:id" element={<Dealer user={user} />} />
          <Route path="/postreview/:id" element={<PostReview />} />
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register setUser={setUser} />} />
        </Routes>
      </main>
      <Footer />
    </BrowserRouter>
  );
}
