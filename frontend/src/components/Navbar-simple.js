import React, { useState, useEffect } from "react";
import {
  AiOutlineClose,
  AiOutlineInfoCircle,
  AiOutlineMenu,
} from "react-icons/ai";
import { TbTruckDelivery } from "react-icons/tb";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const [nav, setNav] = useState(false);
  var navigate = useNavigate();
  return (
    <div className="max-w-[1640px] bg-white mx-auto flex justify-between items-center p-4">
      {/* Left side */}
      <div className="flex items-center">
        <div onClick={() => setNav(!nav)} className="cursor-pointer">
          <AiOutlineMenu size={30} />
        </div>
        <h1
          onClick={() => {
            navigate("/");
          }}
          className="text-2xl sm:text-3xl lg:text-4xl px-2 cursor-pointer">
          buy<span className="font-bold">hardware</span>
        </h1>
      </div>
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
