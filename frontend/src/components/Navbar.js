import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  AiOutlineClose,
  AiOutlineInfoCircle,
  AiOutlineMenu,
  AiOutlineSearch,
} from "react-icons/ai";
import { CiLogin } from "react-icons/ci";
import { BsBoxSeam, BsPerson } from "react-icons/bs";
import { TbTruckDelivery } from "react-icons/tb";

export default function Navbar() {
  const [nav, setNav] = useState(false);
  const [token, setToken] = useState();

  useEffect(() => {
    const auth = localStorage.getItem("auth_token");
    setToken(auth);
  }, [token]);

  return (
    <div className="max-w-[1640px] mx-auto flex justify-between items-center p-4">
      {/* Left side */}
      <div className="flex items-center">
        <div onClick={() => setNav(!nav)} className="cursor-pointer">
          <AiOutlineMenu size={30} />
        </div>
        <h1 className="text-2xl sm:text-3xl lg:text-4xl px-2">
          buy<span className="font-bold">hardware</span>
        </h1>
      </div>
      {/* Search input */}
      <div className="bg-gray-200 rounded-full flex items-center px-2 w-[100px] sm:w-[200px] lg:w-[300px]">
        <AiOutlineSearch size={25} />
        <input
          className="bg-transparent p-2 focus:outline-none w-full"
          type="text"
          placeholder="Поиск"
        />
      </div>
      {/* Profile link */}
      {token ? (
        <Link to="/profile">
          <span className="hidden md:flex items-center p-2 rounded-xl hover:text-red-500">
            <BsPerson size={20} className="mr-2" />
            Профиль
          </span>
        </Link>
      ) : (
        <Link to="/login">
          <span className="hidden md:flex items-center p-2 rounded-xl hover:text-red-500">
            <CiLogin size={20} className="mr-2" />
            Войти
          </span>
        </Link>
      )}

      {/* Order button */}
      <button className=" hidden md:flex items-center p-2 rounded-xl hover:text-red-500">
        <BsBoxSeam size={20} className="mr-2" />
        Заказ
      </button>
      {/* Mobile menu */}
      {/* Overlay */}
      {nav ? (
        <div
          className="bg-black/80 fixed w-full h-screen z-10 top-0 left-0"
          onClick={() => setNav(!nav)}></div>
      ) : (
        ""
      )}

      {/* Side drawer menu */}
      <div
        className={
          nav
            ? "fixed top-0 left-0 w-[300px] h-screen bg-white z-10 duration-300"
            : "fixed top-0 left-[-100%] w-[300px] h-screen bg-white z-10 duration-300"
        }>
        <AiOutlineClose
          size={30}
          onClick={() => setNav(!nav)}
          className="absolute right-4 top-4 cursor-pointer"
        />
        <h2 className="text-2xl p-4">
          buy<span className="font-bold">hardware</span>
        </h2>
        <nav>
          <ul className="flex flex-col p-4 text-gray-800">
            <li className="text-xl py-4 flex">
              <TbTruckDelivery size={25} className="mr-4" />
              Поставки
            </li>
            <li className="text-xl py-4 flex">
              <AiOutlineInfoCircle size={25} className="mr-4" />О компании
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
}
