/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar-simple";

export default function Profile() {
  const [user, setUser] = useState({});
  let navigate = useNavigate();

  useEffect(() => {
    // get token from local storage
    const auth_token = localStorage.getItem("auth_token");
    const auth_token_type = localStorage.getItem("auth_token_type");
    const token = auth_token_type + " " + auth_token;

    //  fetch data from get user api
    axios
      .get("http://localhost:8888/users/", {
        headers: { Authorization: token },
      })
      .then((response) => {
        console.log(response);
        setUser(response.data.result);
      })
      .catch((error) => {
        console.log(error);
        if (error.response.data.detail === "Токен истёк") {
          // remove token form local storage
          localStorage.removeItem("auth_token");
          localStorage.removeItem("auth_token_type");
          navigate("/");
          toast.warning("Токен истёк. Войдите снова.");
        } else {
          toast.error(error.response.data.detail);
        }
      });
  }, []);

  const onClickHandler = (event) => {
    event.preventDefault();

    // remove token form local storage
    localStorage.removeItem("auth_token");
    localStorage.removeItem("auth_token_type");

    // notif
    toast("See You !", {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
    });

    // reload page
    setTimeout(() => {
      navigate("/");
    }, 1500);
  };

  return (
    <div className=" h-screen w-full">
      <Navbar />
      <div className="grid grid-cols-4 mt-4 max-w-[1240px] m-auto min-h-[600px] justify-between">
        <div className="col-span-1 mr-4 mt-8 rounded-3xl bg-gray-100">
          <Link
            className="rounded-full mt-12 bg-gray-50 border-gray-500 border-[2px] flex p-4 m-4 hover:bg-gray-300 hover:cursor-pointer text-center text-xl font-semibold"
            to={"/profile"}>
            Профиль
          </Link>
          <Link
            className="rounded-full bg-gray-50 flex p-4 m-4 hover:bg-gray-300 hover:cursor-pointertext-center text-xl font-semibold"
            to={"/orders"}>
            Заказы
          </Link>
        </div>
        <div className="col-span-3 mr-4 mt-8 bg-gray-50  rounded-3xl">
          <div className="font-sans">
            <div className="m-auto mt-36 rounded-3xl card w-96 mx-auto my-auto bg-white shadow-xl hover:shadow">
              <div className="text-center mt-2 text-3xl font-medium">
                {user.name}
              </div>
              <div className="text-center mt-2 font-light text-sm">
                @{user.username}
              </div>
              <div className="text-center font-normal text-lg">
                {user.email}
              </div>
              <hr className="mt-8"></hr>
              <div className="flex p-4">
                <div className="w-1/2 text-center">
                  <span className="font-bold">{user.phone_number}</span>
                </div>
              </div>
              <hr className="mt-3"></hr>
              <div className="flex p-2">
                <div className="w-full text-center">
                  <button
                    onClick={onClickHandler}
                    className="rounded-3xl py-3 w-64 text-xl text-black outline-none bg-gray-50 hover:bg-gray-100 active:bg-gray-200">
                    Выйти
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
