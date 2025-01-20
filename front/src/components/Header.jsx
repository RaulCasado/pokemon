import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="bg-yellow-400 text-gray-800 shadow-lg p-4 border-b-4 border-red-600">
      <nav className="container mx-auto flex justify-between items-center">
        <h1 className="text-3xl font-bold flex items-center space-x-2">
          <Link to="/" className="flex items-center hover:opacity-90 transition">
            <img
              src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"
              alt="Poké Ball"
              className="w-8 h-8 mr-2"
            />
            <span>Quiz Pokémon</span>
          </Link>
        </h1>
        <ul className="flex space-x-6">
          <li>
            <Link
              to="/"
              className="hover:bg-red-600 text-white px-4 py-2 rounded-full bg-red-500 transition font-medium"
            >
              Home
            </Link>
          </li>
          <li>
            <Link
              to="/solo"
              className="hover:bg-red-600 text-white px-4 py-2 rounded-full bg-red-500 transition font-medium"
            >
              Modo Solitario
            </Link>
          </li>
          <li>
            <Link
              to="/multiplayer"
              className="hover:bg-red-600 text-white px-4 py-2 rounded-full bg-red-500 transition font-medium"
            >
              Modo Multijugador
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
