import React, { useState } from "react";
// Import the styles from the CSS file
import classes from "./NavBar.module.css";
import { Link } from "react-router-dom";
import icon from "../../image/RentConnect_Logo.jpg"

function Navbar() {

    const [hamburgerOpen, setHamburgerOpen] = useState(false);

    return (
      <>
        <div className={classes.desktop}>
          <div className={classes.navbar}>
            <Link className={classes.link} to="/"><div className={classes.brandContainer}>

              <img src={icon} alt="icon"></img>

              <div className={classes.brandSet}>
                <div className={classes.brand}>RentConnect</div>
                <div className={classes.slogan}>Connecting Homes, Building Relationships</div>
              </div>
            </div></Link>
            
            <div className={classes.pagesContainer}>
              <div className={classes.button}><Link className={classes.link} to="/">Home</Link></div>
              <div className={classes.button}><Link className={classes.link} to="/features">Features</Link></div>
              <div className={classes.button}><Link className={classes.link} to="/purchase">Purchase</Link></div>
              <div className={classes.button}><Link className={classes.link} to="/contact">Contact Us</Link></div>
            </div>

          </div>
        </div>
        <div className={classes.mobile}>
          <div className={classes.navbar}>
            <Link className={classes.link} to="/">
              <div className={classes.brandContainer}>

                <img src={icon} alt="icon"></img>

                <div className={classes.brandSet}>
                  <div className={classes.brand}>RentConnect</div>
                  <div className={classes.slogan}>Connecting Homes, Building Relationships</div>
                </div>

              </div>
            </Link>

            <div className={classes.hamburger} onClick={() => setHamburgerOpen((prev) => (!prev))}>
              <div className={classes.hamburgerIcon} >
                <div className={classes.bar + `${hamburgerOpen ? ' ' + classes.burger1 : '' }`}></div>
                <div className={classes.bar + `${hamburgerOpen ? ' ' + classes.burger2 : '' }`}></div>
                <div className={classes.bar + `${hamburgerOpen ? ' ' + classes.burger3 : '' }`}></div>
              </div>

              <div className={`${hamburgerOpen ? classes.pagesContainer : classes.closeContainer}`}>
                <Link className={classes.link + ' ' + classes.button} to="/">Home</Link>
                <Link className={classes.link + ' ' + classes.button} to="/features">Features</Link>
                <Link className={classes.link + ' ' + classes.button} to="/purchase">Purchase</Link>
                <Link className={classes.link + ' ' + classes.button} to="/contact">Contact Us</Link>
              </div>
            </div>

          </div>
        </div>
      </>
    );
  }

export default Navbar;