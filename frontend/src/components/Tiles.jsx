import React from "react";
import "../styles/Tiles.css";

export default function Tiles({ listUrl, manageUrl }) {
  return (
    <div className="tiles-grid">
      {/* Kafelek = link <a> */}
      <a className="tile" href={listUrl} aria-label="Zobacz listę pomiarów">
        <span className="tile-icon">📊</span>
        <span className="tile-title">Zobacz pomiary</span>
        
      </a>

      <a className="tile" href={manageUrl} aria-label="Dodaj lub usuń pomiar">
        <span className="tile-icon">➕</span>
        <span className="tile-title">Dodaj / Usuń</span>
        
      </a>
    </div>
  );
}
