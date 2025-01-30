import React from "react";
import styles from "./Navbar.module.css";

const Navbar = () => {
  return (
    <nav className={styles.nav}>
      <a className={styles.link} href="/">
        Home
      </a>
      <a className={styles.link} href="/basicGuide">
        Basic Guide
      </a>
      <a className={styles.link} href="/command">
        Commads
      </a>
      <a className={styles.link} href="/donate">
        Donate
      </a>
      <a className={styles.link} href="/officialServer">
        Official Server
      </a>
      <a className={styles.link} href="/privacyPolicy">
        Privacy Policy
      </a>
    </nav>
  );
};

export default Navbar;
