import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar-simple";
function Contract(order_id) {
  const [contractData, setContractData] = useState();
  useEffect(() => {
    // get token from local storage
    const auth_token = localStorage.getItem("auth_token");
    const auth_token_type = localStorage.getItem("auth_token_type");
    const token = auth_token_type + " " + auth_token;

    //  fetch data from get user api
    axios
      .get("http://localhost:8888/contracts/" + order_id, {
        headers: { Authorization: token },
      })
      .then((response) => {
        console.log(response);
        setContractData(response.data.result);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  return contractData;
}

export default Contract;
