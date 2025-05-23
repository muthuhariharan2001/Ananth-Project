import React from "react";
import ImageUpload from "./Components/ImageUpload";
import { Route, Routes, Link, NavLink } from "react-router-dom";
import MatchCheck from "./Components/MatchCheck";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Toaster, toast } from 'react-hot-toast';

function App() {
  return (
    <div className="App">

      <Routes>
        <Route path="/image" element={<ImageUpload />} />
        <Route path="/match-check" element={<MatchCheck />} />

        {/* Add other routes here */}
      </Routes>
       <Toaster />

      <ToastContainer />
    </div>
  );
}
export default App;
