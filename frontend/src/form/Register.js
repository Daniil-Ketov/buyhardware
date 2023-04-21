/* eslint-disable default-case */
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import Navbar from "../components/Navbar-simple";

export default function Register() {
  const navigate = useNavigate();

  // Register Form
  const [formRegister, setFormRegister] = useState({
    name: "",
    username: "",
    email: "",
    phone_number: "",
    password: "",
    address: "",
    postal_address: "",
    tin: "",
  });

  const onChangeForm = (label, event) => {
    switch (label) {
      case "name":
        setFormRegister({ ...formRegister, name: event.target.value });
        break;
      case "username":
        setFormRegister({ ...formRegister, username: event.target.value });
        break;
      case "email":
        // email validation
        const email_validation = /\S+@\S+\.\S+/;
        if (email_validation.test(event.target.value)) {
          setFormRegister({ ...formRegister, email: event.target.value });
        }
        break;
      case "phone_number":
        setFormRegister({ ...formRegister, phone_number: event.target.value });
        break;
      case "password":
        setFormRegister({ ...formRegister, password: event.target.value });
        break;
      case "address":
        setFormRegister({ ...formRegister, address: event.target.value });
        break;
      case "postal_address":
        setFormRegister({
          ...formRegister,
          postal_address: event.target.value,
        });
        break;
      case "tin":
        setFormRegister({ ...formRegister, tin: event.target.value });
        break;
      default:
        break;
    }
  };

  //   Submit handler

  const onSubmitHandler = async (event) => {
    event.preventDefault();
    console.log(formRegister);
    // Post to register API
    await axios
      .post("http://localhost:8888/auth/register_client", formRegister)
      .then((response) => {
        // move to sign in page
        navigate("/?signin");

        // add successfully notif
        toast.success(response.data.detail);
        // reload page
        setTimeout(() => {
          window.location.reload();
        }, 1000);

        console.log(response);
      })
      .catch((error) => {
        console.log(error);
        // add error notif
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
              Создайте акаунт
            </h1>
            <p className="w-80 text-center text-sm mb-8 font-semibold text-gray-700 tracking-wide cursor-pointer mx-auto">
              Добро пожаловать в buyhardware!
            </p>
          </div>
          <form onSubmit={onSubmitHandler}>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Имя компании"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("name", event);
                }}
              />
              <input
                type="text"
                placeholder="Логин"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("username", event);
                }}
              />
              <input
                type="text"
                placeholder="Номер телефона"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("phone_number", event);
                }}
              />
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
                placeholder="Пароль"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("password", event);
                }}
              />
              <input
                type="text"
                placeholder="Адрес"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("address", event);
                }}
              />
              <input
                type="text"
                placeholder="Почтовый адрес"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("postal_address", event);
                }}
              />
              <input
                type="text"
                placeholder="ИНН"
                className="block text-sm py-3 px-4 rounded-lg w-full border outline-none focus:ring focus:outline-none focus:ring-red-400"
                onChange={(event) => {
                  onChangeForm("tin", event);
                }}
              />
            </div>
            <div className="text-center mt-6">
              <button
                type="submit"
                className="py-3 w-64 text-xl text-white bg-red-400 rounded-2xl hover:bg-red-300 active:bg-red-500 outline-none">
                Создать акаунт
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
