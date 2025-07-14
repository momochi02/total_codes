import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Compare from "./pages/Compare";
import About from "./pages/About";
import Sidebar from "./components/Sidebar/Sidebar";

function App() {
  return (
    <Router>
      <div style={{ display: "flex" }}>
        <Sidebar />
        <div style={{ marginLeft: "2px", padding: "10px", width: "100%" }}>
          <Routes>
//            <Route path="/" element={<Home />} />
            <Route path="/compare" element={<Compare />} />
//            <Route path="/about" element={<About />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
