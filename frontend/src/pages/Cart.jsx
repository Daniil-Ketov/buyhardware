import { React, useState, useEffect } from "react";
import { useCart } from "react-use-cart";
import { AiOutlinePlus, AiOutlineMinus, AiOutlineClose } from "react-icons/ai";
import Navbar from "../components/Navbar";
import { Link } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import ru from "date-fns/locale/ru";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";
import DatePicker from "react-datepicker";
import { registerLocale, setDefaultLocale } from "react-datepicker";

registerLocale("ru", ru);

function Cart() {
  const {
    isEmpty,
    totalUniqueItems,
    items,
    updateItemQuantity,
    removeItem,
    emptyCart,
    cartTotal,
  } = useCart();

  const [date, setDate] = useState(new Date());

  const sendCartToServer = async () => {
    function cartReformat(item) {
      const id = item.id;
      const volume = item.quantity;
      return { id, volume };
    }
    const cartData = items.map(cartReformat);

    const auth_token = localStorage.getItem("auth_token");
    const auth_token_type = localStorage.getItem("auth_token_type");
    const token = auth_token_type + " " + auth_token;

    await axios
      .post(
        "http://localhost:8888/orders",
        {
          items: cartData,
          shipment_deadline: date.toISOString().split("T")[0],
        },
        {
          headers: { Authorization: token },
        }
      )
      .then((response) => {
        console.log(response);
        emptyCart();

        // add successfully notif
        toast.success(response.data.detail);
        // reload page after success login
        setTimeout(() => {}, 1000);
      })
      .catch((error) => {
        // add error notif

        console.log(error);
        toast.error(error.response.data.detail);
      });
  };

  return (
    <div>
      <Navbar />
      {!isEmpty ? (
        <div className="max-w-[1240px] mt-8 m-auto grid grid-cols-3 h-[600px]">
          <div className="col-span-2 mr-8 mt-4 bg-gray-50  rounded-3xl">
            <div className="ml-12">
              <h1 className="mt-8 text-gray-800 text-3xl font-bold">Корзина</h1>
              <p>Товаров {totalUniqueItems}</p>
            </div>
            <div className="mx-12 mt-4">
              <ul>
                {items.map((item) => (
                  <li
                    key={item.id}
                    className="flex flex-row align-middle bg-gray-100 mb-2 p-4 justify-between rounded-full">
                    <span className="m-2 text-xl">{item.name}</span>
                    <span>
                      <button
                        onClick={() =>
                          updateItemQuantity(item.id, item.quantity - 1)
                        }
                        className="rounded-full bg-gray-100 hover:bg-gray-500 hover:cursor-pointer hover:text-white p-2 m-2">
                        <AiOutlineMinus />
                      </button>
                      <span className="m-2">{item.quantity}</span>
                      <button
                        onClick={() =>
                          updateItemQuantity(item.id, item.quantity + 1)
                        }
                        className="rounded-full bg-gray-100 hover:bg-gray-500 hover:cursor-pointer hover:text-white p-2 m-2">
                        <AiOutlinePlus />
                      </button>
                      <button
                        onClick={() => removeItem(item.id)}
                        className="rounded-full bg-gray-100 hover:bg-red-500 hover:cursor-pointer hover:text-white p-2 m-2">
                        <AiOutlineClose />
                      </button>
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="flex items-end mt-4 col-span-1 ml-8 bg-gray-200 rounded-3xl">
            <div className="flex flex-col">
              <div className="ml-8 mb-8">
                <p className="text-xl mb-1">Срок поставки</p>
                <DatePicker
                  className="flex p-2 text-center text-sm rounded-lg border outline-none focus:ring focus:outline-none focus:ring-red-400"
                  dateFormat="yyyy-MM-dd"
                  placeholderText="Срок поставки"
                  locale="ru"
                  selected={date}
                  onChange={setDate}
                />
              </div>
              <div className="mb-4 ml-8 text-3xl"> Итого: {cartTotal}</div>
              <button
                onClick={() => {
                  sendCartToServer();
                }}
                className="py-4 px-36 mb-6 mx-2 rounded-full text-xl text-white bg-red-500 hover:bg-red-400">
                Заказать
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="min-h-[500px] mt-24 mx-auto max-w-[1240px] bg-gray-200 rounded-3xl flex items-center">
          <div className="flex flex-col mx-auto">
            <h1 className="text-6xl mb-12">Корзина пуста</h1>
            <Link
              to={"/"}
              className="bg-gray-100 mx-auto p-4 rounded-full text-xl hover:bg-red-400 hover:text-white">
              К покупкам
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

export default Cart;
