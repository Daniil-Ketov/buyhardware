import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar-simple";
import Contract from "./Contract";
import PrintButton from "../components/PrintButton";
import ReactToPrint from "react-to-print";

function Orders() {
  const [ordersData, setOrdersData] = useState([]);
  useEffect(() => {
    // get token from local storage
    const auth_token = localStorage.getItem("auth_token");
    const auth_token_type = localStorage.getItem("auth_token_type");
    const token = auth_token_type + " " + auth_token;

    //  fetch data from get user api
    axios
      .get("http://localhost:8888/orders", {
        headers: { Authorization: token },
      })
      .then((response) => {
        console.log(response);
        setOrdersData(response.data.result);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <Navbar />
      <div className="max-w-[1240px] mt-8 m-auto grid grid-cols-4 h-[600px]">
        <div className="col-span-1 mr-4 mt-4 rounded-3xl bg-gray-100">
          <Link
            className="rounded-full mt-12 bg-gray-50 flex p-4 m-4 hover:bg-gray-300 hover:cursor-pointer text-center text-xl font-semibold"
            to={"/profile"}>
            Профиль
          </Link>
          <Link
            className="rounded-full bg-gray-50 border-gray-500 border-[2px] flex p-4 m-4 hover:bg-gray-300 hover:cursor-pointertext-center text-xl font-semibold"
            to={"/orders"}>
            Заказы
          </Link>
        </div>
        <div className="col-span-3 mr-4 mt-4 bg-gray-50  rounded-3xl">
          <div className="ml-12">
            <h1 className="ml-4 mb-12 mt-12 text-gray-800 text-3xl font-bold">
              Ваши заказы
            </h1>
          </div>
          <div className="mx-12 mt-4">
            <ul>
              {ordersData.map((item) => (
                <li
                  key={item.id}
                  className="flex flex-row align-middle bg-gray-100 mb-8 p-4 justify-between rounded-full">
                  <div className="flex flex-row justify-between p-4">
                    <div className="mx-4">
                      <span className="font-bold">Заказ</span>
                      <p className="">{item.id}</p>
                    </div>
                    <div className="mx-4">
                      <span className="font-bold">Дата создания</span>
                      <p className="mr-4">{item.created_at.split("T")[0]}</p>
                    </div>
                    <div className="mx-4">
                      <span className="font-bold">Срок поставки</span>
                      <p>{item.shipment_deadline}</p>
                    </div>
                    <div className="mx-4">
                      <span className="font-bold">Стоимость</span>
                      <p>{item.total}</p>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Orders;
