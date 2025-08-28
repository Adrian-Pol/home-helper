import { useState } from 'react'

import viteLogo from '../assets/react.svg';
//mport './App.css'//
import "../styles/Tiles.css"

import Tiles from '../components/Tiles.jsx';


export default function App({ listUrl, manageUrl }) {
  return <Tiles listUrl={listUrl} manageUrl={manageUrl} />;
}
