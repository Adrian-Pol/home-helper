import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";
import styles from "../styles/Layout.module.css"

const Layout = ({ extraClass =""}) => {
    return (
        
            <div className={`${styles.layoutBody} ${extraClass}`}>      
                
                <Navbar>
                    <p>No tak</p>
                </Navbar>
                <main style={{padding: "20px"}}>
                    <Outlet /> {}
                </main>
                <Footer />
            </div>
        
    );
};

export default Layout;