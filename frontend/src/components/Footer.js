import React from "react";
import styles from "../styles/componentStyles/Footer.module.css";

const Footer = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.footer__content_wrapper}>
        <div className={styles.footer__logo}>
          <span>some image</span>
          <h3>BotGame</h3>
        </div>
        <div className={styles.footer__sections}>
          <div className={styles.footer__contact}>
            <h4 className={styles.footer__section_title}>Contact</h4>
            <ul className={styles.footer__link_list}>
              <li className={styles.footer__link_item}>
                <a href="" className={styles.footer__link}>
                  Support
                </a>
              </li>
              <li className={styles.footer__link_item}>
                <a href="" className={styles.footer__link}>
                  Discord
                </a>
              </li>
              <li className={styles.footer__link_item}>
                <a href="" className={styles.footer__link}>
                  X
                </a>
              </li>
              <li className={styles.footer__link_item}>
                <a href="" className={styles.footer__link}>
                  TikTok
                </a>
              </li>
            </ul>
          </div>
          <div className={styles.footer__developer}>
            <h4 class={styles.footer__section_title}>Dev Stuff</h4>
            <ul className={styles.footer__link_list}>
              <li className={styles.footer__link_item}>
                <a href="" className={styles.footer__link}>
                  GitHub
                </a>
              </li>
              <li className={styles.footer__link_item}>
                <a href="" className={styles.footer__link}>
                  Bug report
                </a>
              </li>
            </ul>
          </div>
          <div className={styles.footer__legal}>
            <h4 className={styles.footer__section_title}>Legal</h4>
            <ul className={styles.footer__link_list}>
              <li className={styles.footer__link_item}>
                <a href="" className={styles.footer__link}>
                  Privacy
                </a>
              </li>
              <li className={styles.footer__link_item}>
                <a href="" className={styles.footer__link}>
                  Terms
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <span className={styles.footer__credits}>
        © {new Date().getFullYear()} BuraYu
      </span>
    </footer>
  );
};

export default Footer;
