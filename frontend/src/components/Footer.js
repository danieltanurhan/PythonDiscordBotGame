import React from "react";

const Footer = () => {
  return (
    <footer>
      <div className="footer__content-wrapper">
        <div className="footer__logo">
          <span>some image</span>
          <h3>BotGame</h3>
        </div>
        <div className="footer__sections">
          <div className="footer__contact">
            <h4 className="footer__section-title">Contact</h4>
            <ul className="footer__link-list">
              <li className="footer__link-item">
                <a href="" className="footer__link">
                  Support
                </a>
              </li>
              <li className="footer__link-item">
                <a href="" className="footer__link">
                  Discord
                </a>
              </li>
              <li className="footer__link-item">
                <a href="" className="footer__link">
                  X
                </a>
              </li>
              <li className="footer__link-item">
                <a href="" className="footer__link">
                  TikTok
                </a>
              </li>
            </ul>
          </div>
          <div className="footer__developer">
            <h4 class="footer__section-title">Dev Stuff</h4>
            <ul className="footer__link-list">
              <li className="footer__link-item">
                <a href="" className="footer__link">
                  GitHub
                </a>
              </li>
              <li className="footer__link-item">
                <a href="" className="footer__link">
                  Bug report
                </a>
              </li>
            </ul>
          </div>
          <div className="footer__legal">
            <h4 className="footer__section-title">Legal</h4>
            <ul className="footer__link-list">
              <li className="footer__link-item">
                <a href="" className="footer__link">
                  Privacy
                </a>
              </li>
              <li className="footer__link-item">
                <a href="" className="footer__link">
                  Terms
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <span className="footer__credits">
        © {new Date().getFullYear()} BuraYu
      </span>
    </footer>
  );
};

export default Footer;
