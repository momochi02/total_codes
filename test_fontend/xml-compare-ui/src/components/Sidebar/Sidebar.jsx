import React from "react";
import { Link } from "react-router-dom";
import "./Sidebar_css.css"; // <- import file CSS

function Sidebar() {
  return (
    <div className="sidebar">
      <h3>Menu</h3>
      <ul>
{/*         <li><Link to="/">Trang chủ</Link></li> */}
        <li><Link to="/compare">Compare XML</Link></li>
{/*         <li><Link to="/about">Giới thiệu</Link></li> */}
      </ul>
    </div>
  );
}

export default Sidebar;
