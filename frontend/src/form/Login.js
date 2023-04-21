/* eslint-disable default-case */
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import Navbar from "../components/Navbar-simple";

export default function Login() {
  const [loginForm, setLoginform] = useState({
    username: "",
    password: "",
  });

  let navigate = useNavigate();

  const onChangeForm = (label, event) => {
    switch (label) {
      case "username":
        setLoginform({ ...loginForm, username: event.target.value });
        break;
      case "password":
        setLoginform({ ...loginForm, password: event.target.value });
        break;
    }
  };

  const onSubmitHandler = async (event) => {
    event.preventDefault();
    console.log(loginForm);
    // call api login
    await axios
      .post("http://localhost:8888/auth/login", loginForm)
      .then((response) => {
        console.log(response);
        // Save token to local storage
        localStorage.setItem("auth_token", response.data.result.access_token);
        localStorage.setItem(
          "auth_token_type",
          response.data.result.token_type
        );

        // add successfully notif
        toast.success(response.data.detail);
        // reload page after success login
        setTimeout(() => {
          if (window.location.pathname === "/") {
            window.location.reload();
          } else {
            navigate("/");
          }
        }, 1000);
      })
      .catch((error) => {
        // add error notif

        console.log(error);
        toast.error(error.response.data.detail);
      });
  };

  return (
    <div className="min-h-screen bg-red-400">
      <Navbar />
      <div className="mt-12 flex justify-center items-center">
        <div className="py-12 px-12 bg-white rounded-2xl shadow-xl z-20">
          <div>
            <h1 className="text-3xl font-bold text-center mb-4 cursor-pointer">
              Добро пожаловать в buyhardware!
            </h1>
            <p className="w-80 text-center text-sm mb-8 font-semibold text-gray-700 tracking-wide cursor-pointer mx-auto">
              Пожалуйста войдите в акаунт!
            </p>
          </div>
          <form onSubmit={onSubmitHandler}>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Логин"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("username", event);
                }}
              />
              <input
                type="password"
                placeholder="Пароль"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("password", event);
                }}
              />
            </div>
            <div className="text-center mt-6">
              <button
                type="submit"
                className="py-3 w-64 text-xl text-white bg-red-400 rounded-2xl hover:bg-red-300 active:bg-red-500 outline-none">
                Войти
              </button>
              <p className="mt-4 text-sm">
                У вас нет акаунта?{" "}
                <Link to="/register">
                  <span className="underline cursor-pointer">Регистрация</span>
                </Link>{" "}
                или{" "}
                <Link to="/forgot">
                  <span className="underline cursor-pointer">
                    Забыли пароль?
                  </span>
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
