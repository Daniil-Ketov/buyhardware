/* eslint-disable default-case */
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import Navbar from "../components/Navbar-simple";

export default function Forgot() {
  const [forgotForm, setForgotForm] = useState({
    email: "",
    new_password: "",
  });
  let navigate = useNavigate();

  const onChangeForm = (label, event) => {
    switch (label) {
      case "email":
        setForgotForm({ ...forgotForm, email: event.target.value });
        break;
      case "new_password":
        setForgotForm({ ...forgotForm, new_password: event.target.value });
        break;
    }
  };

  //   submit handler
  const onSubmitHandler = async (event) => {
    event.preventDefault();
    console.log(forgotForm);
    await axios
      .post("http://localhost:8888/auth/forgot_password", forgotForm)
      .then((response) => {
        toast.success(response.data.detail);
        setTimeout(() => {
          navigate("/");
        }, 1000);
      })
      .catch((error) => {
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
              Забыли пароль ?
            </h1>
            <p className="w-80 text-center text-sm mb-8 font-semibold text-gray-700 tracking-wide cursor-pointer mx-auto">
              Обновите его!
            </p>
          </div>
          <form onSubmit={onSubmitHandler}>
            <div className="space-y-4">
              <input
                type="email"
                placeholder="Email"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("email", event);
                }}
              />
              <input
                type="password"
                placeholder="Новый пароль"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("new_password", event);
                }}
              />
            </div>
            <div className="text-center mt-6">
              <button
                type="submit"
                className="py-3 w-64 text-xl text-white bg-red-400 rounded-2xl hover:bg-red-300 active:bg-red-500 outline-none">
                Обновить пароль
              </button>
              <p className="mt-4 text-sm">
                Уже есть акаунт?{" "}
                <Link to="/login">
                  <span className="underline cursor-pointer">Войти</span>
                </Link>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
