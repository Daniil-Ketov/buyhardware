import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar-simple";
import Contract from "../pages/Contract";
import ReactToPrint from "react-to-print";
const ComponentToPrint = ({ html }) => (
  <div dangerouslySetInnerHTML={{ __html: html }} />
);
const PrintButton = ({ html }) => {
  const componentRef = useRef();

  return (
    <>
      <ReactToPrint
        trigger={() => <button>Распечатать</button>}
        content={() => componentRef.current}
      />
      <div style={{ display: "none" }}>
        <ComponentToPrint ref={componentRef} html={html} />
      </div>
    </>
  );
};

export default PrintButton;
