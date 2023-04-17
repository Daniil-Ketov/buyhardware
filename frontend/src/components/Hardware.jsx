import axios from "axios";
import React, { useState, useEffect } from "react";

function Hardware() {
  // content
  const [hardwareData, setHardwareData] = useState([]);
  const [type, setType] = useState([]);
  // page_number
  const [pageNumber, setPageNumber] = useState([]);
  // page_size
  const [pageSize, setPageSize] = useState([]);
  // total_pages
  const [totalPages, setTotalPages] = useState([]);
  // total_record
  const [totalRecord, setTotalRecord] = useState([]);

  // selected column
  const [selectedColumn, setSelectedColumn] = useState("all");
  // sorted column
  const [sortedColumn, setSortedColumn] = useState(null);
  // filtered column
  const [filteredColumn, setFilteredColumn] = useState(null);

  // sort column
  const [sortColumn, setSortColumn] = useState({
    name: false,
    price: false,
  });

  useEffect(() => {
    axios
      .get("http://localhost:8888/hardware")
      .then((response) => {
        setHardwareData(response.data.result.content);
        setPageNumber(response.data.result.page_number);
        setPageSize(response.data.result.page_size);
        setTotalPages(response.data.result.total_pages);
        setTotalRecord(response.data.result.total_record);
      })
      .catch((error) => {
        console.log(error);
      });
    axios.get("http://localhost:8888/hardware/type/").then((response) => {
      console.log(response);
      setType(response.data.result);
    });
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
            <button className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
              Все
            </button>
            {type &&
              type.map((item) => (
                <button
                  key={item.name}
                  className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
                  {item.name}
                </button>
              ))}
          </div>
        </div>

        {/* Filter price */}
        <div>
          <p className="font-bold text-gray-700">Цена</p>
          <div className="flex justify-between max-w-[240px]">
            <button className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
              Подороже
            </button>
            <button className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
              Подешевле
            </button>
          </div>
        </div>
      </div>
      {/* Display hardware */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-6 pt-4">
        {hardwareData &&
          hardwareData.map((item, index) => (
            <div
              key={index}
              className="border shadow-lg hover:scale-105 duration-300 rounded-lg">
              <img
                src={item.image}
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
  );
}

export default Hardware;
