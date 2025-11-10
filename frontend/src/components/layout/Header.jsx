import React from "react";
import ContrastIcon from "../../assets/icons/contrast.svg";
import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header className="flex justify-between items-center bg-gray-950 px-6 py-4 h-16 fixed top-0 left-0 w-full md:hidden z-100 border-b border-gray-800">
      <Link
        to="/"
        className="font-bold text-2xl bg-linear-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent"
      >
        Atividade AV2
      </Link>
      <button className="text-white">
        <img src={ContrastIcon} alt="Toggle Contrast" className="h-6 w-6" />
      </button>
    </header>
  );
}
