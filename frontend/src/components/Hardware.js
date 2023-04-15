import axios from "axios";
import React, { useState, useEffect } from "react";

function Hardware() {
  const [data, setData] = useState(null);
  const [displayData, setDisplayData] = useState(null);
  const [type, setType] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [displayOrder, setDisplayOrder] = useState("default");

  // For fetching data

  // Filter type
  const filterType = (hwtype) => {
    setDisplayData(
      data.filter((item) => {
        return item.type === hwtype;
      })
    );
  };

  // Filter price
  const filterPrice = (order) => {
    if (order === "asc" && order !== displayOrder) {
      setDisplayOrder("asc");
      setDisplayData(
        data.sort((a, b) => {
          return a.price > b.price;
        })
      );
    } else if (order === "desc" && order !== displayOrder) {
      setDisplayOrder("desc");
      setDisplayData(
        data.sort((a, b) => {
          return a.price < b.price;
        })
      );
    } else {
      setDisplayOrder("default");
      setDisplayData(
        data.sort((a, b) => {
          return a.id > b.id;
        })
      );
    }
  };
  // Fetching data
  useEffect(() => {
    const getData = async () => {
      try {
        const response = await axios.get(`http://localhost:8888/hardware`);
        setData(response.data);
        setDisplayData(response.data);
        setError(null);
      } catch (err) {
        setError(err.message);
        setData(null);
      } finally {
        setLoading(false);
      }
    };
    const getType = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/hardware/type`);
        setType(response.data);
        setError(null);
      } catch (err) {
        setError(err.message);
        setType(null);
      } finally {
        setLoading(false);
      }
    };
    getData();
    getType();
  }, []);
  return (
    <div className="max-w-[1640px] m-auto px-4 py-12">
      <h1 className="text-red-500 font-bold text-4xl text-center">
        Компьютерное оборудование
      </h1>
      {/* Filter row */}
      <div className="flex flex-col lg:flex-row justify-between">
        {/* Filter type */}
        <div>
          <p className="font-bold text-gray-700">Тип</p>
          <div className="flex justify-between flex-wrap">
            <button
              onClick={() => setDisplayData(data)}
              className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
              Все
            </button>
            {type &&
              type.map(({ type, description }) => (
                <button
                  onClick={() => {
                    filterType(type);
                  }}
                  className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
                  {type}
                </button>
              ))}
          </div>
        </div>

        {/* Filter price */}
        <div>
          <p className="font-bold text-gray-700">Цена</p>
          <div className="flex justify-between max-w-[240px]">
            <button
              onClick={() => filterPrice("desc")}
              className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
              Подороже
            </button>
            <button
              onClick={() => filterPrice("asc")}
              className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
              Подешевле
            </button>
          </div>
        </div>
        {/* Display hardware */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 pt-4">
          {displayData &&
            displayData.map((item, index) => (
              <div
                key={index}
                className="border shadow-lg hover:scale-105 duration-300 rounded-lg">
                <img
                  src={item.pic}
                  alt={item.name}
                  className="w-full h-[200px] object-cover rounded-t-lg"
                />
                <div className="flex px-2">
                  <p>
                    <span className="bg-gray-200 rounded-lg px-2">
                      {item.type}
                    </span>
                  </p>
                </div>
                <div className="flex justify-between px-2 py-4 pt-0">
                  <p className="font-bold">{item.name}</p>
                  <p>
                    <span className="bg-gray-200 rounded-full p-1">
                      {item.price}
                    </span>
                  </p>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}

{
  /*  <div>
        {loading && <div>Подождите...</div>}
        {error && <div>{`Проблема с загрузкой данных - ${error}`}</div>}
        <ul>
          {data &&
            data.map(({ id, name, short_desc, price, pic }) => (
              <li>
                <h3>{name}</h3>
              </li>
            ))}
        </ul>
      </div> */
}

export default Hardware;
