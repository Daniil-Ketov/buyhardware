import axios from "axios";
import React, { useState, useEffect } from "react";
import { AiOutlineSearch } from "react-icons/ai";
import { Link } from "react-router-dom";
import { useCart } from "react-use-cart";

function Hardware() {
  // content
  const [hardwareData, setHardwareData] = useState([]);
  const [type, setType] = useState([]);
  const { addItem, inCart } = useCart();
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
        if (!sessionStorage.getItem("headline")) {
          sessionStorage.setItem(
            "headline",
            JSON.stringify(response.data.result.content.slice(0, 3))
          );
        }
      })
      .catch((error) => {
        console.log(error);
      });
    axios.get("http://localhost:8888/hardware/type/").then((response) => {
      setType(response.data.result);
    });
  }, []);

  // capitalize first letter
  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  // modifiedTable td
  const tdTable = (data) => {
    const td_list = [];
    for (const [key, value] of Object.entries(data)) {
      td_list.push(<td key={key}>{capitalizeFirstLetter(value)}</td>);
    }
    return td_list;
  };

  // onClick render pagination
  const renderPagination = async (page) => {
    const url = `http://localhost:8888/hardware?page=${page}&limit=${pageSize}&columns=${selectedColumn}&sort=${sortedColumn}&filter=${filteredColumn}`;
    await axios
      .get(url)
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
  };

  // pagination
  const pageRows = () => {
    const rows = [];
    for (let index = 1; index <= totalPages; index++) {
      rows.push(
        <button
          key={index}
          onClick={() => {
            renderPagination(index);
          }}
          className={`btn ${
            pageNumber === index
              ? "bg-neutral"
              : "bg-base-200 text-red hover:text-white"
          }`}>
          {index}
        </button>
      );
    }
    return rows;
  };

  //  onChange pageOption
  const onChangePageLimit = async (pageLimit) => {
    const url = `http://localhost:8888/hardware?page=${pageNumber}&limit=${pageLimit}&columns=${selectedColumn}&sort=${sortedColumn}&filter=${filteredColumn}`;
    await axios
      .get(url)
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
  };

  // dropdown sort column
  const dropdownSortColumn = () => {
    const list = [];
    for (const [key, value] of Object.entries(sortColumn)) {
      list.push(
        <li key={key}>
          <label className="flex justify-between label cursor-pointer">
            <span className="label-text">{capitalizeFirstLetter(key)}</span>
            {value === true ? (
              <input
                onChange={() => {
                  setSortColumn({ ...sortColumn, [key]: false });
                }}
                type="checkbox"
                className="checkbox"
                checked
              />
            ) : (
              <input
                onChange={() => {
                  setSortColumn({ ...sortColumn, [key]: true });
                }}
                type="checkbox"
                className="checkbox"
              />
            )}
          </label>
        </li>
      );
    }
    return list;
  };

  // chose selecetd column
  const choseSortedColumnHandler = async () => {
    // filter value if true in sort
    const true_keys = Object.keys(sortColumn).filter((key) => sortColumn[key]);
    let sorts = true_keys.join("-");

    setSortedColumn(sorts);
    let url = `http://localhost:8888/hardware?page=${pageNumber}&limit=${pageSize}&columns=${selectedColumn}&sort=${sorts}&filter=${filteredColumn}`;
    await axios
      .get(url)
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
  };

  // search handler
  const onSearchHandler = async (data) => {
    // we just filter column name
    const filter = `name*${data}`;
    setFilteredColumn(filter);
    let url = `http://localhost:8888/hardware?page=${pageNumber}&limit=${pageSize}&columns=${selectedColumn}&sort=${sortedColumn}&filter=${filter}`;
    await axios
      .get(url)
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
  };

  // Filter type
  const filterType = (hwtype) => {
    setHardwareData(
      hardwareData.filter((item) => {
        return item.type in hwtype;
      })
    );
  };

  const headlineCards = JSON.parse(sessionStorage.getItem("headline"));

  return (
    <div>
      {/* Headline Cards */}
      <div className="max-w-[1640px] mx-auto p-4 py-12 grid md:grid-cols-3 gap-6">
        {/* Cards */}
        {headlineCards &&
          headlineCards.map((item, index) => (
            <div key={"hl:" + index} className="rounded-xl relative">
              {/* Overlay */}
              <div className="absolute w-full h-full bg-black/50 rounded-xl text-white">
                <p className="font-bold text-2xl px-2 pt-4">{item.name}</p>
                <p className="px-2">{item.short_description}</p>

                {!inCart(item.id) ? (
                  <button
                    onClick={() =>
                      addItem({
                        id: item.id,
                        name: item.name,
                        price: item.price,
                        quantity: 1,
                      })
                    }
                    className=" border-white bg-white text-black mx-2 absolute bottom-4 rounded-lg p-2">
                    Заказать
                  </button>
                ) : (
                  <Link
                    to={"/cart"}
                    className=" border-white bg-white text-black mx-2 absolute bottom-4 rounded-lg p-2">
                    В корзину
                  </Link>
                )}
              </div>
              <img
                className="max-h-[160px] md:max-h-[200px] w-full object-cover rounded-xl"
                src={item.image}
                alt={item.name}
              />
            </div>
          ))}
      </div>
      <div className="max-w-[1640px] m-auto px-4 py-12">
        <h1 className="text-red-500 font-bold text-4xl text-center">
          Компьютерное оборудование
        </h1>
        {/* Filter row */}
        <div className="flex flex-col mt-4 lg:flex-row justify-between lg:h-[50px]">
          {/* Filter price */}
          {/* <div>
          <p className="font-bold text-gray-700">Цена</p>
          <div className="flex justify-between max-w-[240px]">
            <button className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
              Подороже
            </button>
            <button className="border-2 border-red-500 text-red-500 rounded-xl p-1 m-1 hover:bg-red-500 hover:text-white">
              Подешевле
            </button>
          </div>
        </div> */}
          {/* Search */}
          <div className="bg-gray-200 rounded-full flex items-center px-2 w-[100px] sm:w-[200px] lg:w-[300px]">
            <AiOutlineSearch size={25} />
            <input
              className="bg-transparent p-2 focus:outline-none w-full"
              type="text"
              placeholder="Поиск"
              onChange={(e) => {
                onSearchHandler(e.target.value);
              }}
            />
          </div>

          {/* Filter type */}
          <div className="flex flex-row">
            <p className="font-bold text-gray-700 self-center mr-2">Тип</p>
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

          {/* sort column */}
          <div className="dropdown dropdown-bottom">
            <label tabIndex={0} className="btn m-1">
              Сортировка
            </label>
            <ul
              tabIndex={0}
              className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
              {dropdownSortColumn()}
              <li>
                <button
                  onClick={choseSortedColumnHandler}
                  className="btn bg-base-200 text-black hover:text-white">
                  Выбрать
                </button>
              </li>
            </ul>
          </div>
        </div>
        {/* Display hardware */}
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-6 pt-4 mt-12">
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
                    <span className="text-gray-800 rounded-lg">
                      {item.type}
                    </span>
                  </p>
                </div>
                <div className="flex justify-between px-2 py-4 pt-0">
                  <p className="font-bold text-lg">{item.name}</p>
                  <p>
                    {!inCart(item.id) ? (
                      <button
                        onClick={() =>
                          addItem({
                            id: item.id,
                            name: item.name,
                            price: item.price,
                            quantity: 1,
                          })
                        }
                        className=" text-black rounded-full p-2 mr-4 hover:text-white hover:bg-red-500">
                        Заказать
                      </button>
                    ) : (
                      <Link
                        to={"/cart"}
                        className=" text-black rounded-full p-2 mr-4 hover:text-white hover:bg-red-500">
                        В корзину
                      </Link>
                    )}
                    <span className="text-xl mr-4 p-2">{item.price}</span>
                  </p>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}

export default Hardware;
