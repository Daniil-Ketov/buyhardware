import "./App.css";
import React, { useState, useEffect } from "react";
import Forgot from "./form/Forgot";
import Login from "./form/Login";
import Register from "./form/Register";
import Profile from "./pages/Profile";
import Home from "./pages/Home";
import { Route, Routes } from "react-router-dom";

function App() {
  const [token, setToken] = useState();

  useEffect(() => {
    const auth = localStorage.getItem("auth_token");
    setToken(auth);
  }, [token]);

  return (
    <Routes>
      <Route exact path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/forgot" element={<Forgot />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={<Profile />} />
    </Routes>
  );
}

export default App;
